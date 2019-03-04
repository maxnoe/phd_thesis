import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from argparse import ArgumentParser
from mpl_toolkits.axes_grid1 import make_axes_locatable
from fact.io import read_h5py

parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('outputfile')
args = parser.parse_args()

np.random.seed(0)


df = read_h5py(args.inputfile)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.025)

ax.plot([0, 1], [0, 1], color='lightgray')
ax.axvline(0, lw=0.5, color='lightgray')
ax.axhline(1, lw=0.5, color='lightgray')

fpr, tpr, t = roc_curve(df['label'], df['probabilities'], drop_intermediate=False)

nth = 5000
fpr, tpr, t = fpr[::nth], tpr[::nth], t[::nth]

points = np.array([fpr, tpr]).T.reshape((-1, 1, 2))
segments = np.concatenate([points[:-1], points[1:]], axis=1)
col = LineCollection(segments, zorder=3)
col.set_array(t)
col.set_clim(0, 1)
col.set_cmap('inferno')
ax.add_collection(col)

rocs = np.array([
    roc_auc_score(fold['label'], fold['probabilities'])
    for _, fold in df.groupby('cv_fold')
])

ax.set_title(f'ROC-AUC: {rocs.mean():.4f} ± {rocs.std():.4f}')

ax.set_ylim(0, 1.025)
ax.set_xlim(-0.025, 1)
ax.set_aspect(1)
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')

fig.colorbar(col, cax=cax, label='$t_p$')
cax.xaxis.set_label_position('top')
cax.xaxis.tick_top()

fig.tight_layout(pad=0)
fig.savefig(args.outputfile)
