import matplotlib.pyplot as plt
from argparse import ArgumentParser
import numpy as np

from eventio import IACTFile

parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('-e', '--event', type=int, default=0)
parser.add_argument('-t', '--telescope', type=int)
parser.add_argument('-n', '--n-bins', type=int, default=500)
parser.add_argument('-r', '--radius', type=float)
parser.add_argument('-m', '--max-percentile', type=float, default=99)
parser.add_argument('-o', '--outputfile')


def main():
    args = parser.parse_args()

    with IACTFile(args.inputfile) as f:
        it = iter(f)
        event = next(it)
        for i in range(args.event):
            event = next(it)

        if args.telescope:
            photons = [event.photon_bunches[args.telescope]]
            positions = [f.telescope_positions[args.telescope]]
        else:
            photons = list(event.photon_bunches.values())
            positions = f.telescope_positions

        if args.radius is None:
            args.radius = f.telescope_positions['r'][0] / 100

        edges = np.linspace(-args.radius, args.radius, args.n_bins + 1)
        area = np.diff(edges)[0]**2

        hists = []
        for pos, tel_photons in zip(positions, photons):
            hist, _, _ = np.histogram2d(
                (tel_photons['x'] + pos[0]) / 100,
                (tel_photons['y'] + pos[1]) / 100,
                edges,
            )
            hists.append(hist)
        img = np.sum(hists, axis=0) / area

        fig, ax = plt.subplots()

        ax.set_aspect(1)
        ax.set_facecolor('k')
        ax.set_xlabel(r'$x \mathbin{/} \si{\meter}$')
        ax.set_ylabel(r'$y \mathbin{/} \si{\meter}$')

        vmax = np.percentile(img[img > 0], args.max_percentile)
        img = ax.pcolormesh(edges, edges, img, cmap='gray', vmin=0, vmax=vmax)
        img.set_rasterized(True)
        fig.colorbar(
            img,
            ax=ax,
            label=r'Photons / m²',
            orientation='horizontal',
        )
        fig.tight_layout(pad=0)

        if args.outputfile:
            fig.savefig(args.outputfile, dpi=300, bbox_inches='tight')
        else:
            plt.show()


if __name__ == '__main__':
    main()
