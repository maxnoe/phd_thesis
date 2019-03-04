from fact.io import read_h5py
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, r2_score
import numpy as np
from argparse import ArgumentParser


def accuracy(series):
    return accuracy_score(
        np.sign(series.true_disp),
        np.sign(series.disp_prediction),
    )


def r2(series):
    return r2_score(
        np.abs(series.true_disp),
        np.abs(series.disp_prediction),
    )


parser = ArgumentParser()
parser.add_argument('gamma_dl3')
parser.add_argument('outputfile')
parser.add_argument('--threshold', default=0.8, type=float)
args = parser.parse_args()


df = read_h5py(args.gamma_dl3, key='events')

edges = 10**np.arange(2.5, 4.8, 0.2)

df['bin_idx'] = np.digitize(df['corsika_event_header_total_energy'], edges)


# discard under and overflow
df = df[(df['bin_idx'] != 0) & (df['bin_idx'] != len(edges))]


performance = {}

binned = pd.DataFrame({
    'e_center': 0.5 * (edges[1:] + edges[:-1]),
    'e_low': edges[:-1],
    'e_high': edges[1:],
    'e_width': np.diff(edges),
}, index=pd.Series(np.arange(1, len(edges)), name='bin_idx'))

binned['accuracy'] = df.groupby('bin_idx').apply(accuracy)
binned['r2_score'] = df.groupby('bin_idx').apply(r2)

selected = df.query(f'gamma_prediction > {args.threshold}').copy()
binned['accuracy_selected'] = selected.groupby('bin_idx').apply(accuracy)
binned['r2_score_selected'] = selected.groupby('bin_idx').apply(r2)


df = df.query('gamma_prediction > 0.8').copy()

fig, axs = plt.subplots(2, 1, sharex=True)

ax1, ax2 = axs

ax1.errorbar(
    binned.e_center, binned.accuracy, xerr=binned.e_width / 2, ls='',
    label='All Events',
)
ax1.errorbar(
    binned.e_center, binned.accuracy_selected, xerr=binned.e_width / 2, ls='',
    label=rf'Events with $\param{{gamma\_prediction}} > \num{{{args.threshold}}}',
)
ax1.legend(loc='lower center', bbox_to_anchor=[0.5, 1.025], ncol=2)
ax1.set_ylabel(r'\strut Accuracy for $\sgn \param{disp}$')

ax2.errorbar(binned.e_center, binned.r2_score, xerr=binned.e_width / 2, ls='')
ax2.errorbar(binned.e_center, binned.r2_score_selected, xerr=binned.e_width / 2, ls='')
ax2.set_ylabel(r'\strut $r^2$ score for $\abs{\param{disp}}$')


ax2.set_xlabel(r'$E_{\text{true}} \mathbin{/} \si{\GeV}$')
ax2.set_xscale('log')
ax1.set_ylim(0.5, 1.0)
ax2.set_ylim(None, 1.0)


fig.tight_layout(pad=0, h_pad=0.2)
fig.savefig(args.outputfile)
