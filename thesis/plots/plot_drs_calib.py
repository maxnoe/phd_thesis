import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()

pixel = 102

f = fits.open('../data/drscalib.fits.gz')

raw_data = f[1].data['Data'][0]
calibrated = f[1].data['DataCalibrated'][0]

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()

l1, = ax1.plot(np.arange(0, 290) / 2, raw_data[pixel * 300 + 10:(pixel + 1) * 300])

l2, = ax2.plot(
    np.arange(0, 290) / 2, calibrated[pixel * 300 + 10:(pixel + 1) * 300],
    color='C1',
)

ax1.legend((l1, l2), ['Raw Data', 'After DRS4 Calibration'])

ax1.set_xlabel(r'$t \mathbin{/} \si{\nano\second}$')
ax1.set_ylabel(r'$\mathrm{ADC\,Counts}', color='C0')
ax2.set_ylabel(r'$U \mathbin{/} \si{\milli\volt}$', color='C1')
ax1.set_title(r'Run 20130102\_060, EventID 11, Pixel 104')

fig.tight_layout(pad=0)
fig.savefig(args.outputfile)
