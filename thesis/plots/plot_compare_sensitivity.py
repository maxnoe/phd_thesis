import matplotlib.pyplot as plt
import pandas as pd
import click


@click.command()
@click.argument('outputfile')
@click.option('--sensitivity', type=(str, str), multiple=True)
@click.option('--logy', is_flag=True)
def main(outputfile, sensitivity, logy):

    for label, infile in sensitivity:

        s = pd.read_csv(infile)
        s.dropna(inplace=True)
        plt.errorbar(
            s['e_center'],
            s['relative_sensitivity'],
            yerr=(
                s['relative_sensitivity'] - s['relative_sensitivity_uncertainty_low'],
                s['relative_sensitivity_uncertainty_high'] - s['relative_sensitivity']
            ),
            xerr=s['e_width'] / 2,
            label=label,
            ls='',
        )

    plt.legend(loc='upper center')
    plt.xlabel(r'$E_{\text{est}} \mathbin{/} \si{\GeV}$')
    plt.ylabel(r'Flux / Crab Units')
    plt.xscale('log')
    if logy:
        plt.yscale('log')

    plt.ylim(0, 3)
    plt.tight_layout(pad=0)
    plt.savefig(outputfile)


if __name__ == '__main__':
    main()
