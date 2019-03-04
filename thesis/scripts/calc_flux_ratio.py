from fact.analysis.statistics import (
    power_law_integral,
    PDG_COSMIC_RAY_FLUX, PDG_COSMIC_RAY_INDEX, PDG_COSMIC_RAY_E_REF,
    log_parabola, POINT_SOURCE_FLUX_UNIT
)
import numpy as np

from scipy.integrate import quad
import astropy.units as u


MAGIC_CRAB_FLUX = u.Quantity(3.23e-11, 1 / (u.TeV * u.cm**2 * u.s))
MAGIC_CRAB_A = -2.47
MAGIC_CRAB_B = -0.24
MAGIC_E_REF = 1.0 * u.TeV


solid_angle = 2 * np.pi * (1 - np.cos(2.25 * u.deg)) * u.sr


E_MIN = u.Quantity(100, u.GeV)
E_MAX = u.Quantity(200, u.TeV)


cr_flux = power_law_integral(
    PDG_COSMIC_RAY_FLUX,
    PDG_COSMIC_RAY_INDEX,
    E_MIN, E_MAX,
    PDG_COSMIC_RAY_E_REF
) * solid_angle


def crab(E):
    E = u.Quantity(E, u.GeV, copy=False)
    return log_parabola(
        E, MAGIC_CRAB_FLUX, MAGIC_CRAB_A, MAGIC_CRAB_B, e_ref=MAGIC_E_REF,
    ).to_value(POINT_SOURCE_FLUX_UNIT)


crab_flux, crab_error = quad(
    crab,
    E_MIN.to_value(u.GeV),
    E_MAX.to_value(u.GeV)
) * (POINT_SOURCE_FLUX_UNIT * u.GeV)

print(cr_flux / crab_flux)


crab_flux, crab_error = (quad(
    crab,
    40,
    np.inf,
) * (POINT_SOURCE_FLUX_UNIT * u.GeV)).to(1 / u.d / u.m**2)
print(crab_flux)
