import astropy.units as u
from irf.sensitivity import calculate_sensitivity
from fact.io import read_h5py
from fact.analysis.statistics import li_ma_significance
from argparse import ArgumentParser
import numpy as np


parser = ArgumentParser()
parser.add_argument('datafile')
parser.add_argument('threshold', type=float)
parser.add_argument('theta2_cut', type=float)
parser.add_argument('outputfile')


E_TRUE = 'corsika_event_header_total_energy'


def main():
    args = parser.parse_args()

    bins = 10**np.arange(2.7, 4.4, 0.2)
    e_min = u.Quantity(bins[0], u.GeV)
    e_max = u.Quantity(bins[-1], u.GeV)
    n_bins = len(bins) - 1

    events = read_h5py(args.datafile, key='events')
    runs = read_h5py(args.datafile, key='runs')
    obstime = runs.ontime.sum() * u.s

    sensitivity = calculate_sensitivity(
        events.query(f'gamma_prediction >= {args.threshold}'),
        theta2_cut=args.theta2_cut,
        e_min=e_min,
        e_max=e_max,
        n_bins=n_bins,
        t_obs=obstime,
        t_ref=50 * u.hour,
        n_bootstrap=100,
    )
    sensitivity['significance'] = li_ma_significance(
        sensitivity['n_on_weighted'], sensitivity['n_off_weighted'],
        0.2
    )

    sensitivity.to_csv(args.outputfile, index=False)


if __name__ == '__main__':
    main()
