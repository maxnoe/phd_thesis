import click
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, SkyOffsetFrame
import astropy.units as u
import numpy as np

from fact.io import read_h5py

columns = [
    'ra_prediction',
    'dec_prediction',
]


@click.command()
@click.argument('data_path')
@click.argument('threshold', type=float)
@click.argument('theta2cut', type=float)
def main(data_path, threshold, theta2cut):
    '''
    Plot a 2d histogram of the origin of the air showers in the
    given hdf5 file in ra, dec.
    '''
    if threshold > 0.0:
        columns.append('gamma_prediction')

    crab = SkyCoord(ra="83.63308333°", dec="22.0145°")

    events = read_h5py(data_path, key='events', columns=columns)
    events = events.query(f'gamma_prediction > {threshold}')

    pointing_positions = read_h5py(
        data_path, key='runs',
        columns=['right_ascension', 'declination'],
    ).drop_duplicates()
    pointing_positions = SkyCoord(
        pointing_positions['right_ascension'].to_numpy() * u.hourangle,
        pointing_positions['declination'].to_numpy() * u.deg,
    )

    fig, ax = plt.subplots(1, 1)
    ax.set_aspect(1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.05)

    ra = crab.ra.deg
    dec = crab.dec.deg
    hist, ra_bins, dec_bins, img = ax.hist2d(
        events['ra_prediction'] * 15,
        events['dec_prediction'], bins=100,
        range=[[ra - 3, ra + 3], [dec - 3, dec + 3]],
        cmap='inferno',
        vmin=0,
    )
    img.set_rasterized(True)
    fig.colorbar(img, cax=cax, label='Gamma-artige Ereignisse')
    ax.set_xlabel('Rektaszension / Grad')
    ax.set_ylabel('Deklination / Grad')
    fig.tight_layout(pad=0)
    fig.savefig('build/skymap.pdf', dpi=300)

    for pos in pointing_positions:
        ax.plot(
            pos.ra.deg,
            pos.dec.deg,
            marker='x',
            color='C0',
        )
        circle = plt.Circle(
            xy=(pos.ra.deg, pos.dec.deg),
            radius=2.25,
            color='C0', fill=False, linewidth=2,
        )
        ax.add_patch(circle)
        radius = crab.separation(pos)
        source_angle = np.arctan2(crab.dec - pos.dec, crab.ra - pos.ra).rad

        for i in range(1, 6):

            off = SkyCoord(
                ra=pos.ra + radius * np.cos(source_angle + np.pi * i / 3),
                dec=pos.dec + radius * np.sin(source_angle + np.pi * i / 3)
            )

            circle = plt.Circle(
                xy=(off.ra.deg, off.dec.deg),
                radius=np.sqrt(theta2cut),
                color='C5', fill=False, linewidth=1
            )
            ax.add_patch(circle)

    circle = plt.Circle(xy=(ra, dec), radius=np.sqrt(theta2cut), color='C4', fill=False, linewidth=1)
    ax.add_patch(circle)
    fig.savefig('build/skymap_positions.pdf', dpi=300)


if __name__ == '__main__':
    main()
