import h5py
from fact.io import read_h5py, read_simulated_spectrum
from fact.analysis.statistics import calc_weights_logparabola
from fact.analysis import split_on_off_source_independent
import numpy as np
import matplotlib.pyplot as plt
from ruamel.yaml import YAML
import astropy.units as u
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('apa', type=int)
parser.add_argument('outputfile')
args = parser.parse_args()

apa = args.apa
gamma_color = {85: 'C0', 95: 'C1', 100: 'C2'}

magic = YAML(typ='safe').load(open('../configs/magic_jheap2015.yaml'))
theta2_cut = 0.1
threshold = 0.5

crab = read_h5py(f'../build/apa{apa}/crab_dl3.hdf5', key='events')
crab = crab.join(read_h5py(
    f'../build/apa{apa}/crab_precuts.hdf5', key='events',
    columns=['size'],
))
crab = crab.query(f'gamma_prediction > {threshold}')
ontime = read_h5py(
    f'../build/apa{apa}/crab_dl3.hdf5', key='runs', columns=['ontime']
).ontime.sum()
crab['weights'] = 1

limits = np.min(crab['size']), np.nanpercentile(crab['size'], 99.9)
edges = np.linspace(*np.log10(limits), 31)
centers = 0.5 * (edges[:-1] + edges[1:])
width = np.diff(edges)

on, off = split_on_off_source_independent(crab, theta2_cut)
on_hist, _ = np.histogram(np.log10(on['size']), bins=edges, weights=on['weights'])
off_hist, _ = np.histogram(np.log10(off['size']), bins=edges, weights=off['weights'])

plt.errorbar(
    centers,
    on_hist - 0.2 * off_hist,
    yerr=np.sqrt(on_hist + 0.2**2 * off_hist),
    xerr=width / 2,
    color='k',
    linestyle='',
    label='Crab Nebula Observations',
)

sim_spectrum = read_simulated_spectrum('../data/corsika_headers/gamma_headers_corsika76900.hdf5')

f = f'../build/apa{apa}/gamma_test_dl3.hdf5'
gammas = read_h5py(f, key='events')
gammas = gammas.join(read_h5py(
    f'../build/apa{apa}/gamma_test.hdf5', key='events',
    columns=['size'],
))
gamma = gammas.query(f'gamma_prediction > {threshold}')
sample_fraction = h5py.File(f, 'r').attrs.get('sample_fraction', 1)

e = u.Quantity(gammas['corsika_event_header_total_energy'].to_numpy(), u.GeV, copy=False)
gammas['weights'] = calc_weights_logparabola(
    energy=e,
    obstime=u.Quantity(ontime, u.s),
    n_events=sim_spectrum['n_showers'],
    sample_fraction=sample_fraction,
    e_min=sim_spectrum['energy_min'],
    e_max=sim_spectrum['energy_max'],
    simulated_index=sim_spectrum['energy_spectrum_slope'],
    scatter_radius=sim_spectrum['x_scatter'],
    target_a=u.Quantity(magic['a']),
    target_b=u.Quantity(magic['b']),
    e_ref=u.Quantity(**magic['e_ref']),
    flux_normalization=u.Quantity(**magic['phi_0']),
)

on, off = split_on_off_source_independent(gammas, theta2_cut)
on_hist, _ = np.histogram(np.log10(on['size']), bins=edges, weights=on['weights'])
off_hist, _ = np.histogram(np.log10(off['size']), bins=edges, weights=off['weights'])

plt.errorbar(
    centers,
    on_hist - 0.2 * off_hist,
    yerr=np.sqrt(on_hist + 0.2**2 * off_hist),
    xerr=width / 2,
    linestyle='',
    color=gamma_color[apa],
    label=rf'Gammas $\param{{apa}} = \SI{{{apa}}}{{\percent}}',
)

plt.legend()
plt.yscale('log')
plt.xlabel(r'$\log_{10}(\param{size})$')
plt.ylabel('Excess Events')
plt.tight_layout(pad=0)
plt.savefig(args.outputfile)
