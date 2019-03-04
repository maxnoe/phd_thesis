from fact.io import read_h5py
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_auc_score
import numpy as np
from argparse import ArgumentParser


def roc_auc(series):
    return roc_auc_score(
        series.label,
        series.gamma_prediction,
    )


parser = ArgumentParser()
parser.add_argument('gamma_dl3')
parser.add_argument('proton_dl3')
parser.add_argument('outputfile')
args = parser.parse_args()


columns = [
    'gamma_prediction',
    'gamma_energy_prediction',
    'corsika_event_header_total_energy',
]
gammas = read_h5py(args.gamma_dl3, key='events', columns=columns).sample(1_000_000)
protons = read_h5py(args.proton_dl3, key='events', columns=columns).sample(1_000_000)

gammas['label'] = 1
protons['label'] = 0

edges = 10**np.arange(2.7, 4.8, 0.1)
df = pd.concat([gammas, protons], ignore_index=True, axis='index')
df['bin_idx'] = np.digitize(df['gamma_energy_prediction'], edges)

# discard under and overflow
df = df[(df['bin_idx'] != 0) & (df['bin_idx'] != len(edges))]

binned = pd.DataFrame({
    'e_center': 0.5 * (edges[1:] + edges[:-1]),
    'e_low': edges[:-1],
    'e_high': edges[1:],
    'e_width': np.diff(edges),
}, index=pd.Series(np.arange(1, len(edges)), name='bin_idx'))

binned['roc_auc'] = df.groupby('bin_idx').apply(roc_auc)
print(binned)

fig, ax = plt.subplots(1, 1, sharex=True)


ax.errorbar(
    binned.e_center, binned.roc_auc, xerr=binned.e_width / 2, ls='',
    label='All Events',
)

ax.set_ylabel(r'$A_{\text{ROC}}$')

ax.set_xlabel(r'$E_{\text{est}} \mathbin{/} \si{\GeV}$')
ax.set_xscale('log')
ax.set_ylim(None, 1.0)

fig.tight_layout(pad=0)
fig.savefig(args.outputfile)
