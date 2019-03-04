import astropy.units as u
from irf.sensitivity import calculate_sensitivity
from fact.io import read_h5py
from fact.io import read_simulated_spectrum
from fact.analysis.statistics import (
    calc_weights_logparabola,
    calc_weights_cosmic_rays,
    li_ma_significance,
)
from ruamel.yaml import YAML
import h5py
import pandas as pd
from argparse import ArgumentParser
import numpy as np


magic_crab = YAML(typ='safe').load(open('../configs/magic_jheap2015.yaml'))

parser = ArgumentParser()
parser.add_argument('gammafile')
parser.add_argument('gamma_header_file')
parser.add_argument('protonfile')
parser.add_argument('proton_header_file')
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

    gammas = read_h5py(args.gammafile, key='events')
    gamma_spectrum = read_simulated_spectrum(args.gamma_header_file)
    gammas['particle'] = 'gamma'

    with h5py.File(args.gammafile, mode='r') as f:
        gamma_sample_fraction = f.attrs['sample_fraction']

    protons = read_h5py(args.protonfile, key='events')
    proton_spectrum = read_simulated_spectrum(args.proton_header_file)
    proton_spectrum
    protons['particle'] = 'proton'
    with h5py.File(args.protonfile, mode='r') as f:
        proton_sample_fraction = f.attrs['sample_fraction']

    gammas['weight'] = calc_weights_logparabola(
        energy=u.Quantity(gammas[E_TRUE].values, u.GeV, copy=False),
        obstime=50 * u.hour,
        n_events=gamma_spectrum['n_showers'],
        e_min=gamma_spectrum['energy_min'],
        e_max=gamma_spectrum['energy_max'],
        simulated_index=gamma_spectrum['energy_spectrum_slope'].value,
        scatter_radius=gamma_spectrum['x_scatter'],
        target_a=magic_crab['a'],
        target_b=magic_crab['b'],
        flux_normalization=u.Quantity(**magic_crab['phi_0']),
        e_ref=u.Quantity(**magic_crab['e_ref']),
        sample_fraction=gamma_sample_fraction,
    )

    protons['weight'] = calc_weights_cosmic_rays(
        energy=u.Quantity(protons[E_TRUE].values, u.GeV, copy=False),
        obstime=50 * u.hour,
        n_events=proton_spectrum['n_showers'] * proton_spectrum.get('n_reuse', 20),
        e_min=proton_spectrum['energy_min'],
        e_max=proton_spectrum['energy_max'],
        simulated_index=proton_spectrum['energy_spectrum_slope'].value,
        scatter_radius=proton_spectrum['x_scatter'],
        sample_fraction=proton_sample_fraction,
        viewcone=6 * u.deg,
    )

    events = pd.concat([gammas, protons], sort=False, ignore_index=True)

    s = calculate_sensitivity(
        events.query(f'gamma_prediction >= {args.threshold}'),
        theta2_cut=args.theta2_cut,
        e_min=e_min,
        e_max=e_max,
        n_bins=n_bins,
        t_obs=50 * u.hour,
        t_ref=50 * u.hour,
        n_bootstrap=100,
    )
    s['significance'] = li_ma_significance(s['n_on_weighted'], s['n_off_weighted'], 0.2)

    s.to_csv(args.outputfile, index=False)


if __name__ == '__main__':
    main()
