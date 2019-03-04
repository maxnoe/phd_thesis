import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import astropy.units as u
from cycler import cycler
import sys
from numpy.polynomial import Polynomial


def e_to_f(e):
    return u.Quantity(e, u.eV, copy=False).to_value(u.Hz, equivalencies=u.spectral())


def f_to_e(e):
    return u.Quantity(e, u.Hz, copy=False).to_value(u.eV, equivalencies=u.spectral())


# Plot flux points
component = 'nebula'

table = Table.read('../data/crab_mwl.fits.gz')
table = table[table['component'] == 'nebula']
table.sort('energy')


fig, ax = plt.subplots(figsize=(595 / 72.27, 394 / 72.27 * 0.9))

ax.set_prop_cycle(cycler(marker=['.', 'o']) * plt.rcParams['axes.prop_cycle'])

papers = sorted(
    np.unique(table['paper']),
    key=lambda s: table[table['paper'] == s]['energy'].min()
)

flux_unit = u.GeV / (u.m**2 * u.s)

for paper in papers:
    m = table['paper'] == paper

    x = table['energy'][m]

    y = table['energy_flux'][m]
    yerr_lo = table['energy_flux_err_lo'][m]
    yerr_hi = table['energy_flux_err_hi'][m]

    if paper in {'hess', 'magic', 'hegra'}:
        label = paper.upper()
    elif paper.startswith('fermi'):
        label = 'Fermi'
    else:
        label = ''

    ax.errorbar(
        x.quantity.to_value(u.eV),
        y.quantity.to_value(flux_unit),
        yerr=(
            yerr_lo.quantity.to_value(flux_unit),
            yerr_hi.quantity.to_value(flux_unit),
        ),
        label=label + r' \cite{' + paper.replace(r'_', '') + '}',
        linestyle='',
        ms=3,
    )

energy = np.logspace(-3, 2, 100) * u.TeV


def crab_flux(e):
    ''' Meyer et al. Parameterization of the IC component '''
    x = np.log10(e.to_value(u.TeV))
    p = Polynomial([-10.2708, -0.53616, -0.179475, 0.0473174, 0, -0.00449161])

    return u.Quantity(10**p(x), u.erg / u.s / u.cm**2)


ax.plot(
    energy.to_value(u.eV),
    crab_flux(energy).to_value(u.GeV / u.s / u.m**2),
    color='gray',
    marker='',
    lw=2,
)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'$E \mathbin{/} \si{\eV}$')
ax.set_ylabel(
    r'$E^2 \frac{\d{N}}{\d{E}} \mathbin{\bigm/} '
    r'\bigl(\si{\GeV \per\meter\squared\per\second}\bigr)$'
)
ax.set_xticks(10**np.arange(-6, 15.1, 3))
ax.set_xticks(10**np.arange(-6, 15.1, 1), minor=True)
ax.set_xticklabels([], minor=True)

f_ax = ax.secondary_xaxis('top', functions=(e_to_f, f_to_e))
f_ax.set_xlabel(r'$\nu \mathbin{/} \si{\hertz}$')

ax.legend(loc='lower center', ncol=8, bbox_to_anchor=(0.5, 1.12))
ax.grid()
fig.tight_layout()
fig.savefig(sys.argv[1])
