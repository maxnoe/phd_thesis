import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np


pixel = 67

f = fits.open('drscalib.fits.gz')

spike = f[1].data['DataCalibrated'][0]
no_spike = f[1].data['DataCalibratedNoSpikes'][0]

fig, ax = plt.subplots(1, 1)

ax.plot(np.arange(10, 300) / 2, spike[pixel * 300 + 10:(pixel + 1) * 300])
ax.plot(np.arange(10, 300) / 2, no_spike[pixel * 300 + 10:(pixel + 1) * 300])


ax.set_ylabel(r'$U / \si{\milli\volt}$')
ax.set_xlabel(r'$t / \si{\nano\second}$')

fig.tight_layout(pad=0)
fig.savefig('build/plots/spikes.pdf')
