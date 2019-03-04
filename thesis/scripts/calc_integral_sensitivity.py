from irf.sensitivity import relative_sensitivity
from fact.io import read_h5py
from argparse import ArgumentParser
import astropy.units as u
import numpy as np


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('outputfile')
parser.add_argument('threshold', type=float)
parser.add_argument('theta2_cut', type=float)
args = parser.parse_args()


events = read_h5py(args.inputfile, key='events')
runs = read_h5py(args.inputfile, key='runs')
obstime = u.Quantity(runs.ontime.sum(), u.s)

events = events.query(f'gamma_prediction >= {args.threshold}').copy()

n_on = np.count_nonzero(events.theta_deg <= np.sqrt(args.theta2_cut))

n_off = 0
for i in range(1, 6):
    n_off += np.count_nonzero(events[f'theta_deg_off_{i}'] <= np.sqrt(args.theta2_cut))


s = relative_sensitivity(n_on=n_on, n_off=n_off, alpha=0.2, t_obs=obstime)[0]

with open(args.outputfile, 'w') as f:
    f.write(r'\SI{' f'{100 * s:.1f}' r'}{\percent}')
