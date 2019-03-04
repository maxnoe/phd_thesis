import numpy as np
from tqdm import tqdm
import pandas as pd

from fact.io import read_h5py
from fact.analysis import li_ma_significance
import click
import matplotlib.pyplot as plt

columns = [
    'gamma_prediction',
    'theta_deg',
    'theta_deg_off_1',
    'theta_deg_off_2',
    'theta_deg_off_3',
    'theta_deg_off_4',
    'theta_deg_off_5',
]


@click.command()
@click.argument('data_path')
@click.argument('outputfile')
@click.argument('sig_file')
@click.argument('theta2_cut_file')
@click.argument('threshold_file')
def main(data_path, outputfile, sig_file, theta2_cut_file, threshold_file):

    events = read_h5py(data_path, key='events', columns=columns)

    theta2_step = 0.002
    threshold_step = 0.01

    theta2_cuts = np.arange(0.1, 0.0, -theta2_step)
    thresholds = np.arange(0.5, 1, threshold_step)

    significance = np.full((len(thresholds), len(theta2_cuts)), np.nan)

    selected = events
    for i, threshold in enumerate(tqdm(thresholds)):
        selected = selected.query('gamma_prediction >= {}'.format(threshold))

        theta2_on = selected.theta_deg**2
        theta2_off = pd.concat([
            selected['theta_deg_off_{}'.format(i)]
            for i in range(1, 6)
        ])**2

        for j, theta2_cut in enumerate(theta2_cuts):
            theta2_on = theta2_on[theta2_on <= theta2_cut]
            theta2_off = theta2_off[theta2_off <= theta2_cut]

            n_on = len(theta2_on)
            n_off = len(theta2_off)

            sig = li_ma_significance(n_on, n_off, 0.2)
            significance[i, j] = sig

    idx = np.argmax(significance)
    i, j = np.unravel_index(idx, significance.shape)
    best_threshold = thresholds[i]
    best_theta2_cut = theta2_cuts[j]
    max_significance = significance[i, j]

    with open(sig_file, 'w') as f:
        f.write(f'{max_significance:.1f}')

    with open(threshold_file, 'w') as f:
        f.write(f'{best_threshold:.2f}')

    with open(theta2_cut_file, 'w') as f:
        f.write(f'{best_theta2_cut:.3f}')

    theta2_edges = np.append(theta2_cuts + theta2_step / 2, theta2_cuts[-1] - theta2_step / 2)
    threshold_edges = np.append(thresholds - threshold_step / 2, thresholds[-1] + threshold_step / 2)

    plt.plot(
        best_theta2_cut,
        best_threshold,
        marker='o',
        color='k',
        markerfacecolor='none',
        markersize=10,
    )
    plt.title((
        r'$S_{\max}= '
        rf'{max_significance:.1f}\,\sigma,'
        rf't_p={best_threshold:.2f},'
        r' \theta_{\max}^2 ='
        rf' {best_theta2_cut:.3f}\,'
        r'\si{deg\squared}$'
    ))
    plt.pcolormesh(
        theta2_edges, threshold_edges, significance,
        cmap='inferno', vmax=60, vmin=30,
        rasterized=True,
    )
    plt.colorbar(label='Significance / σ')
    plt.xlabel(r'$\theta^2_{\mathrm{max}} \,\, / \,\, \mathrm{deg}^2$')
    plt.ylabel(r'$t_p$')

    plt.tight_layout(pad=0)
    plt.savefig(outputfile)


if __name__ == '__main__':
    main()
