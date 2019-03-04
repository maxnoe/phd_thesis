import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
from argparse import ArgumentParser
from mpl_toolkits.axes_grid1 import make_axes_locatable

parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()

np.random.seed(0)

print(plt.rcParams['figure.figsize'])

n_signal = 1000
n_background = 1000
y = np.append(np.zeros(n_background), np.ones(n_signal))


rnd = np.random.chisquare(20, n_signal)
rndb = (rnd - rnd.min()) / (rnd.max() - rnd.min())

rnd = np.random.chisquare(20, n_background)
rnds = 1 - (rnd - rnd.min()) / (rnd.max() - rnd.min())


p_rand = np.random.uniform(0, 1, len(y))
p_perf = y
p_real = np.append(rndb, rnds)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes('top', size='5%', pad=0.025)

ax.plot([0, 1], [0, 1], color='lightgray')

for p, label in zip([p_rand, p_perf, p_real], ['Random', 'Perfect', 'Realistic']):
    fpr, tpr, t = roc_curve(y, p, drop_intermediate=False)

    points = np.array([fpr, tpr]).T.reshape((-1, 1, 2))
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    col = LineCollection(segments, zorder=3)
    if p is p_perf:
        col.set_array(np.full_like(t, 0.5))
    else:
        col.set_array(t)
    col.set_clim(0, 1)
    ax.add_collection(col)

ax.text(0.2, 0.15, r'Random guessing: $A_{{\text{{roc}}}} = {:.2f}$'.format(roc_auc_score(y, p_rand)))
ax.text(0, 1.025, r'Perfect classifier: $A_{{\text{{roc}}}} = {:.2f}$'.format(roc_auc_score(y, p_perf)))
ax.text(
    0.14, 0.8,
    'Realistic classifier:\n'
    + r'$A_{{\text{{roc}}}} = {:.2f}$'.format(roc_auc_score(y, p_real)),
    va='top',
)

ax.set_ylim(0, 1.1)
ax.set_xlim(-0.025, 1)
ax.set_aspect(1)
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')

fig.colorbar(col, cax=cax, label='$t_p$', orientation='horizontal')
cax.xaxis.set_label_position('top')
cax.xaxis.tick_top()

fig.tight_layout(pad=0)
fig.savefig(args.outputfile)
