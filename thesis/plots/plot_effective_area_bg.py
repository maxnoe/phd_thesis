from fact.io import read_data, read_simulated_spectrum
import matplotlib.pyplot as plt
import numpy as np
import h5py
import click

from fact_plots.effective_area import plot_effective_area


@click.command()
@click.argument('GAMMA_HEADERS')
@click.argument('GAMMA_DL3')
@click.argument('PROTON_HEADERS')
@click.argument('PROTON_DL3')
@click.option('-t', '--threshold', type=float, default=[0.8], multiple=True, help='Prediction threshold to use')
@click.option('--theta2-cut', type=float, default=[0.03], multiple=True, help='Theta squared cut to use')
@click.option('--n-bins', type=int, default=20,  help='Number of bins for the area')
@click.option('--e-low', type=float, help='Lower energy limit in GeV')
@click.option('--e-high', type=float, help='Upper energy limit in GeV')
@click.option('-o', '--output')
def main(
    gamma_headers,
    gamma_dl3,
    proton_headers,
    proton_dl3,
    threshold,
    theta2_cut,
    n_bins,
    e_low,
    e_high,
    output,
):

    theta2_cuts = theta2_cut
    thresholds = threshold

    gamma = (gamma_headers, gamma_dl3, 'Gamma Rays')
    proton = (proton_headers, proton_dl3, 'Protons')
    for i, (corsika_headers, analysis_output, label) in enumerate([proton, gamma]):

        all_events = read_data(corsika_headers, key='corsika_events')

        analysed = read_data(
            analysis_output,
            key='events',
            columns=[
                'corsika_event_header_total_energy',
                'gamma_prediction',
                'theta_deg'
            ]
        )

        with h5py.File(analysis_output, 'r') as f:
            fraction = f.attrs.get('sample_fraction', 1.0)
            print('Using a sample fraction of', fraction)

        simulated_spectrum = read_simulated_spectrum(corsika_headers)
        impact = simulated_spectrum['x_scatter']
        print('Using max_impact of', impact)

        e_low = e_low or all_events.total_energy.min()
        e_high = e_high or all_events.total_energy.max()
        bins = np.logspace(np.log10(e_low), np.log10(e_high), n_bins + 1)

        assert len(theta2_cuts) == len(thresholds), 'Number of cuts has to be the same for theta and threshold'

        alpha_step = 0.6 / (len(theta2_cuts) - 1)

        for j, (threshold, theta2_cut) in enumerate(zip(thresholds[:], theta2_cuts[:])):
            selected = analysed.query(
                '(gamma_prediction >= @threshold) & (theta_deg <= sqrt(@theta2_cut))'
            ).copy()

            plot_effective_area(
                all_events.total_energy,
                selected.corsika_event_header_total_energy,
                bins=bins,
                impact=impact,
                sample_fraction=fraction,
                label=label if (j + 1) == len(theta2_cuts) else None,
                color=f'C{i}',
                alpha=0.4 + alpha_step * j,
            )

    plt.legend(loc='lower right')
    plt.xlabel(r'$E_{\text{true}} \mathbin{/} \si{\GeV}$')
    plt.ylabel(r'$A_{\text{eff}} \mathbin{/} \si{\meter\squared}')

    plt.yscale('log')
    plt.xscale('log')

    plt.tight_layout(pad=0.02)
    if output is not None:
        plt.savefig(output, dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    main()
