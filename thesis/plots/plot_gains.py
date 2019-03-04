from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser
import pandas as pd
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()

default_gains = np.genfromtxt('../fact-tools/src/main/resources/gain_sorted_20131127.csv')

hdu = fits.open('../fact-tools/src/main/resources/gains_20120503-20171103.fits.gz')
gains = hdu[1].data
print(gains['timestamp'])

timestamp = pd.to_datetime(gains['timestamp'].tolist())


plt.plot(timestamp, np.median(gains['gain'], axis=1), '.', ms=3)
plt.plot(np.datetime64('2013-11-27'), np.median(default_gains), '.', label='Median Gain pre v1.0')
plt.legend()
plt.ylabel(r'gain / \si{\per\milli\volt}')
plt.tight_layout(pad=0)
plt.savefig(args.outputfile)
