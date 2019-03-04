from astropy.io import fits
import matplotlib.pyplot as plt
from fact.plotting import camera
from matplotlib.colors import LogNorm


data = fits.open('../data/aldebaran_pedvar.fits')[1].data

ped_var = data['ped_var'].mean(axis=0)


fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()

cmap = plt.get_cmap('inferno')
cmap.set_bad('k')
pixels = camera(ped_var, cmap=cmap, ax=ax)
pixels.set_norm(LogNorm())
pixels.set_clim(30e3, None)

fig.colorbar(pixels, ax=ax, label='Pedestal Variance / a.u.')

for i in range(11):
    k = f'starsInFOV_{i}_'
    x = data[k + 'x'].mean(axis=0)
    y = data[k + 'y'].mean(axis=0)

    ax.plot(x, y, marker='o', mfc='none', color='lightgray', ms=15, mew=1.5)

fig.savefig('build/plots/star_pedvar.pdf')
