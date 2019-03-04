from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
import numpy as np
from argparse import ArgumentParser
from mpl_toolkits.axes_grid1 import make_axes_locatable


parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()


sources = Table.read('../data/4fgl.fits', hdu='LAT_Point_Source_Catalog')

sources  = sources[['CLASS1', 'RAJ2000', 'DEJ2000', 'GLON', 'GLAT', 'Flux1000']].to_pandas()
sources['CLASS'] = sources['CLASS1'].str.decode('ascii').str.strip()
sources['associated'] = sources['CLASS'].str.islower()
sources['identified'] = sources['CLASS'].str.isupper()
sources['unassociated'] = sources['CLASS'] == ''
sources['class'] = sources['CLASS'].str.upper()

sources['status'] = 'unassociated'
sources.loc[sources['identified'], 'status'] = 'identified'
sources.loc[sources['associated'], 'status'] = 'associated'

classes = pd.read_csv('../data/4fgl_classes.csv').set_index('name')
classes.loc[classes['color'].isna(), 'color'] = None
classes.loc[classes['marker'].isna(), 'marker'] = None


fig = plt.figure()

ax = fig.add_axes([0.01, 0.15, 0.98, 0.8], projection='mollweide', facecolor='k')
cax = fig.add_axes([0.0, 0.1, 1.0, 0.05])

ax.set_xticks([])
ax.set_yticks([])

df = sources.sort_values('Flux1000')
coords = SkyCoord(
    ra=df['RAJ2000'] * u.deg,
    dec=df['DEJ2000'] * u.deg,
    frame='icrs',
)

img = ax.scatter(
    coords.ra.wrap_at('180d').rad,
    coords.dec.rad,
    c=df['Flux1000'] * 1e4,
    s=5,
    linewidth=0,
    norm=LogNorm(),
    cmap='inferno',
    vmin=1e-6,
)

fact_sources = [
    'Mrk 421', 'Mrk 501', 'Crab', '1ES 1959+650',
    '1ES 2344+51.4', '1H0323+342', 'PKS 0736+01',
]
for source in fact_sources:
    color = 'lightgray' if source not in fact_sources else '#7ac143'

    s = SkyCoord.from_name(source)
    x = s.ra.wrap_at('180d').rad
    y = s.dec.rad

    ax.plot(x, y, marker='o', mfc='none', color=color)
    delta_x = -5 if source not in ('1ES 1218+304',) else 5
    ha = 'left' if delta_x > 0 else 'right'
    ax.annotate(
        source, xy=(x, y),
        xytext=(delta_x, 0), textcoords='offset points',
        ha=ha, va='center', color=color,
        family='sans-serif',
    )

plane = SkyCoord(
    l=np.linspace(-62, 296, 250) * u.deg,
    b=np.zeros(250) * u.deg,
    frame='galactic',
)
ax.plot(
    plane.icrs.ra.wrap_at('180d').rad,
    plane.icrs.dec.rad,
    color='gray',
    zorder=-1,
)

fig.colorbar(
    img, cax=cax, orientation='horizontal',
    label=r'$\Phi \,/\, \si{\per\meter\squared\per\second}$'
)

fig.savefig(args.outputfile, transparent=False, bbox_inches=None)
