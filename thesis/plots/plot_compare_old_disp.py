from fact.io import read_h5py
import numpy as np
from argparse import ArgumentParser
from fact.instrument import camera_distance_mm_to_deg
from fact_plots.angular_resolution import plot_angular_resolution
import matplotlib.pyplot as plt


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('dl3_file')
parser.add_argument('threshold')
parser.add_argument('outputfile')
parser.add_argument('--only-correct-sign', action='store_true')


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


def main():
    args = parser.parse_args()

    df = read_h5py(args.inputfile, key='events', columns=[
        'cog_x', 'cog_y', 'delta', 'source_position_x', 'source_position_y',
        'skewness_long', 'width', 'length', 'corsika_event_header_total_energy',
    ])
    df[['gamma_prediction', 'theta_deg', 'disp', 'true_disp']] = read_h5py(args.dl3_file, key='events', columns=['gamma_prediction', 'theta_deg', 'disp_prediction', 'true_disp'])
    df['correct_sign'] = np.sign(df['disp']) == np.sign(df['true_disp'])


    df = df.query(f'gamma_prediction >= {args.threshold}')
    if args.only_correct_sign:
        df = df.query('correct_sign')
    df = df.sample(100000).copy()

    df['old_disp'] = calc_disp(df['width'].values, df['length'].values)
    df['cos_delta_alpha'] = cos_delta_alpha(
        df['cog_x'], df['cog_y'], df['delta'], df['source_position_x'], df['source_position_y']
    )
    m3l = np.cbrt(df['skewness_long'] * df['length']**3)

    df['old_disp'] *= calc_sign(df['cos_delta_alpha'], m3l)

    df['rec_pos_x'], df['rec_pos_y'] = calc_reconstructed_pos(
        df['old_disp'], df['cog_x'], df['cog_y'], df['delta']
    )
    df['old_theta'] = calc_theta(df['source_position_x'], df['source_position_y'], df['rec_pos_x'], df['rec_pos_y'])

    bins = 10**np.arange(2.5, 4.9, 0.2)
    plot_angular_resolution(df, bins=bins, theta_key='old_theta', label=r'\texttt{FACT-Tools v0.17.2 disp}')
    plot_angular_resolution(df, bins=bins, theta_key='theta_deg', label=r'\texttt{aict-tools disp}')
    plt.legend()

    plt.xlabel(r'$E_{\text{true}} \mathbin{/} \si{\GeV}$')
    plt.ylabel(r'$\theta_{\num{0.68}} \mathbin{/} \si{\degree}$')
    plt.tight_layout(pad=0)
    plt.savefig(args.outputfile)


if __name__ == '__main__':
    main()
