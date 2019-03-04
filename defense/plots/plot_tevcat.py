from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
import numpy as np
from argparse import ArgumentParser
from collections import defaultdict


class Dict(dict):
    def __missing__(self, key):
        self[key] = 'Other'
        return self[key]


parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()


df = pd.read_csv('./tevcat.csv')
df['Type'] = pd.Categorical(df['Type'])
coords = SkyCoord(
    ra=Angle(df['RA'], u.hourangle),
    dec=Angle(df['Dec'], u.deg),
)

df['Type'] = df['Type'].map(Dict({
    'HBL': 'Blazar',
    'BL Lac (class unclear)': 'Blazar',
    'AGN (unknown type)': 'AGN',
    'Composite SNR': 'SNR',
    'SNR/Molec. Cloud': 'SNR',
    'IBL': 'Blazar',
    'LBL': 'Blazar',
    'PWN/TeV Halo': 'SNR',
    'PWN': 'SNR',
    'PSR': 'PSR',
    'GRB': 'GRB',
    'Shell': 'SNR',
    'UNID': 'Unbek.',
})).astype('category')
# print(df['Type'])
categories = df['Type'].cat.categories
cmap = ListedColormap([f'C{i}' for i in range(len(categories))])
# print(categories)


fig = plt.figure()
ax = fig.add_axes(
    [0.01, 0.15, 0.98, 0.8],
    projection='mollweide',
    facecolor='k',
)
cax = fig.add_axes([0.0, 0.1, 1.0, 0.05])

ax.set_xticks([])
ax.set_yticks([])

img = ax.scatter(
    coords.ra.wrap_at('180d').rad,
    coords.dec.rad,
    c=df['Type'].cat.codes,
    s=5,
    linewidth=0,
    # norm=LogNorm(),
    cmap=cmap,
    vmin=-0.5,
    vmax=len(df['Type'].cat.categories) - 0.5,
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

cbar = fig.colorbar(
    img, cax=cax, orientation='horizontal',
)
cbar.set_ticks(np.arange(len(categories)))
cbar.set_ticklabels(categories)

fig.savefig(args.outputfile, transparent=False, bbox_inches=None)
