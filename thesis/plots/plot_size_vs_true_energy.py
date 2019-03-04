from fact.io import read_h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from numba import njit

columns = ['corsika_event_header_total_energy', 'size', 'leakage1', 'leakage2']
gammas = read_h5py('../build/apa85/gamma_test.hdf5', key='events', columns=columns)
protons = read_h5py('../build/apa85/proton_test.hdf5', key='events', columns=columns)

gammas = gammas.join(read_h5py(
    '../build/apa85/gamma_test_dl3.hdf5',
    key='events',
    columns=['gamma_energy_prediction'],
))

protons = protons.join(read_h5py(
    '../build/apa85/proton_test_dl3.hdf5',
    key='events',
    columns=['gamma_energy_prediction'],
))

labels = ('Gammas', 'Protons')


@njit()
def calc_containment(hist):
    res = np.zeros(hist.shape, dtype=np.float64)
    total = hist.sum()
    n_rows, n_cols = hist.shape

    flat = hist.ravel()

    for i in range(n_rows):
        for j in range(n_cols):
            res[i, j] = flat[flat >= hist[i, j]].sum() / total

    return res


for col, bins in zip(('size', 'gamma_energy_prediction'), [[1.5, 4], [2.5, 5.5]]):
    plt.figure()

    for cmap, df in zip(['Blues_r', 'Reds_r'], (protons, gammas)):
        df['log_e'] = np.log10(df['corsika_event_header_total_energy'].values)
        df['log_' + col] = np.log10(df[col].values)

        hist, xedges, yedges = np.histogram2d(
            df['log_e'],
            df['log_' + col],
            range=[[2.25, 5.5], bins],
            bins=(100, 100),
        )
        xcenter = xedges[:-1] + np.diff(xedges) / 2
        ycenter = yedges[:-1] + np.diff(yedges) / 2

        containment = calc_containment(hist)

        levels = [0.1, 0.25, 0.68, 0.90]
        CS = plt.contour(
            xcenter,
            ycenter,
            containment.T,
            cmap=cmap,
            levels=levels,
            vmin=0,
            vmax=1,
        )
        plt.clabel(CS, fmt=lambda l: f'{l:.0%}', inline_spacing=30, fontsize='small')

    plt.xlabel(r'$\log_{10}(E_\text{true} \mathbin{/} \si{GeV})$')
    if col == 'size':
        plt.ylabel(r'$\log_{10}(\param{size})')
    else:
        plt.ylabel(r'$\log_{10}(E_\text{est} \mathbin{/} \si{GeV})$')

    plt.legend(
        [
            Rectangle((0, 0), 0, 0, color=plt.get_cmap(c)(0.75), fill=False)
            for c in ('Reds', 'Blues')
        ],
        labels,
    )
    plt.tight_layout(pad=0)
    plt.savefig(f'build/plots/{col}_vs_true_energy.pdf')
