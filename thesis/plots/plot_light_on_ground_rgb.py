import matplotlib.pyplot as plt
from eventio import IACTFile
import numpy as np
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('-o', '--output-file')
parser.add_argument('-b', '--n-bins', default=500, type=int)
parser.add_argument('-r', '--radius', type=float)
parser.add_argument('-m', '--vmax', type=float, default=99)

masses = {
    'Electrons': 0.000511,
    'Muons': 0.105658,
    'Other': None,
}


def main():
    args = parser.parse_args()
    f = IACTFile(args.inputfile)
    event = next(iter(f))

    radius = args.radius or f.telescope_positions['r'][0] / 100

    photons = event.photon_bunches[0]
    emitter = event.emitter[0]

    w, h = plt.rcParams['figure.figsize']
    fig, ax = plt.subplots(1, 1, figsize=(w, w))

    image = np.zeros((args.n_bins, args.n_bins, 3))

    ax.set_title('R: Electrons, G: Muons, B: Other')

    for i, (particle, mass) in enumerate(masses.items()):
        if mass is not None:
            mask = np.isclose(emitter['mass'], mass, rtol=1e-4)
        else:
            mask = emitter['mass'] > 1.1 * masses['Muons']

        hist, edges, edges = np.histogram2d(
            photons['x'][mask] / 100,
            photons['y'][mask] / 100,
            bins=args.n_bins,
            range=[[-radius, radius], [-radius, radius]],
        )
        image[:, :, i] = hist.T[::-1, :]

    width = np.diff(edges)[0]
    area = width * width
    image /= area

    vmax = np.nanpercentile(image[image > 0], args.vmax)
    image = np.clip(image / vmax, 0, 1)

    plt.imshow(image, extent=[-radius, radius, -radius, radius])
    plt.xlabel(r'$x \mathbin{/} \si{\meter}$')
    plt.ylabel(r'$y \mathbin{/} \si{\meter}$')
    plt.tight_layout(pad=0)

    if args.output_file is None:
        plt.show()
    else:
        plt.savefig(args.output_file)


if __name__ == '__main__':
    main()
