import matplotlib.pyplot as plt
import numpy as np
from fact.io import read_h5py
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()


df = read_h5py('../build/apa85/gamma_test.hdf5', key='events', columns=[
    'corsika_event_header_x', 'corsika_event_header_y',
])

df['impact'] = np.sqrt(
    df['corsika_event_header_x']**2
    + df['corsika_event_header_y']**2
)

plt.axvline(300, color='gray', linestyle='--')

plt.xlabel(r'$R \mathbin{/} \si{\meter}$')

plt.hist(df['impact'] / 100, bins=50, range=[0, 350])

ymin, ymax = plt.ylim()
plt.annotate(r'$R_{\max}$', (305, ymax / 2))


plt.tight_layout(pad=0)
plt.savefig(args.outputfile)
