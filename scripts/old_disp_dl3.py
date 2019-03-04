from fact.io import read_h5py, to_h5py
import numpy as np
from argparse import ArgumentParser
from fact.instrument import camera_distance_mm_to_deg
from aict_tools.io import copy_runs_group


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('dl3_file')
parser.add_argument('outputfile')


def calc_disp(width, length):
    return 117.94 * (1 - width / length)


def calc_sign(cos_delta_alpha, m3l):
    sign1 = np.sign(cos_delta_alpha)
    sign2 = np.sign(m3l * sign1 + 200)
    return -sign1 * sign2


def cos_delta_alpha(cog_x, cog_y, delta, source_x, source_y):
    delta_x = cog_x - source_x
    delta_y = cog_y - source_y

    dist = np.sqrt(delta_x**2 + delta_y**2)
    long = np.cos(delta) * delta_x + np.sin(delta) * delta_y

    return long / dist


def calc_reconstructed_pos(disp, cog_x, cog_y, delta):
    x = cog_x + np.cos(delta) * disp
    y = cog_y + np.sin(delta) * disp

    return x, y


def calc_theta(source_x, source_y, rec_x, rec_y):
    return camera_distance_mm_to_deg(np.sqrt(
        (source_x - rec_x)**2 + (source_y - rec_y)**2
    ))


def positions(source_x, source_y, n_off=5):
    r = np.sqrt(source_x**2 + source_y**2)
    phi = np.arctan2(source_y, source_x)

    delta_phi = 2 * np.pi / (n_off + 1)

    for i in range(n_off + 1):
        phi_off = phi + i * delta_phi
        x, y = r * np.cos(phi_off), r * np.sin(phi_off)

        yield x, y


def main():
    args = parser.parse_args()

    df = read_h5py(args.inputfile, key='events', columns=[
        'cog_x', 'cog_y', 'delta', 'source_position_x', 'source_position_y',
        'skewness_long', 'width', 'length', 'night', 'run_id', 'event_num'
    ])
    dl3 = read_h5py(args.dl3_file, key='events', columns=[
        'event_num',
        'gamma_energy_prediction', 'gamma_prediction', 'night',
        'pointing_position_az', 'pointing_position_zd',
        'run_id', 'timestamp'
    ])

    disp = calc_disp(df['width'], df['length'])
    m3l = np.cbrt(df['skewness_long'] * df['length']**3)

    print(dl3.columns)
    for i, (x, y) in enumerate(positions(df['source_position_x'], df['source_position_y'])):
        k = f'_off_{i}' if i > 0 else ''

        df['cos_delta_alpha' + k] = cos_delta_alpha(
            df['cog_x'], df['cog_y'], df['delta'],
            x, y
        )
        df['disp_prediction' + k] = disp * calc_sign(
            df['cos_delta_alpha' + k], m3l
        )
        df['rec_pos_x' + k], df['rec_pos_y' + k] = calc_reconstructed_pos(
            df['disp_prediction' + k], df['cog_x'], df['cog_y'], df['delta']
        )

        dl3['theta_deg' + k] = calc_theta(
            x, y,
            df['rec_pos_x' + k], df['rec_pos_y' + k]
        )


    to_h5py(dl3, args.outputfile, mode='w', key='events')
    copy_runs_group(args.inputfile, args.outputfile)


if __name__ == '__main__':
    main()
