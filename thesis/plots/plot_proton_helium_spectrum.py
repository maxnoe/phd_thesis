import tarfile
import pandas as pd
from io import TextIOWrapper
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()


def read_data(tar, member):
    f = TextIOWrapper(tar.extractfile(member), encoding='ascii')

    for i in range(2):
        line = next(f)

    names = line.lstrip('#').strip().replace('<', '').replace('>', '').split()

    return pd.read_csv(f, sep=r'\s+', comment='#', names=names, header=None)


# primaries = ('helium', 'proton', 'carbon', 'oxygen', 'iron')
# markers = ('.', '.', 's', '*', 'o')
primaries = ('helium', 'proton')
markers = ('.', '.')

for particle, marker in zip(primaries, markers):
    f = tarfile.open(f'../data/{particle}_spectra.tar.gz')

    experiments = read_data(f, 'data_exps.txt')
    experiments['file_name'] = experiments['file_name'].apply(os.path.basename)
    if 'qty' in experiments.columns:
        experiments[['qty', 'exp_name']] = experiments[['exp_name', 'qty']]

    data = {}
    for row in experiments.itertuples():
        df = read_data(f, row.file_name)
        experiments.loc[row.Index, 'e_min'] = df.E.min()
        experiments.loc[row.Index, 'e_max'] = df.E.max()
        data[row.exp_name] = df

    experiments['file_num'] = experiments.index + 1
    experiments['experiment'] = experiments['exp_name'].str.split('(', expand=True)[0]
    experiments = experiments.sort_values('e_max').tail(20)
    experiments.set_index('experiment', inplace=True)

    names = ['AMS02', 'ATIC02', 'CREAM-I', 'CREAM-II', 'PAMELA', 'JACEE', 'RUNJOB']
    all_data = pd.DataFrame()
    for i, name in enumerate(names):
        if name not in experiments.index:
            print('no data for experiment', name)
            continue

        exp = experiments.loc[name]

        df = read_data(f, f'data_exp{exp.file_num}.dat')
        df['experiment'] = name
        all_data = all_data.append(df)

        plt.errorbar(
            df.E,
            df.y * df.E**2,
            yerr=(
                df.yerrtot_lo * df.E**2,
                df.yerrtot_up * df.E**2,
            ),
            linestyle='',
            marker=marker,
            label=name if particle == 'proton' else None,
            ms=5 if marker == '.' else 3,
            mew=0,
            color=f'C{i}',
            alpha=0.3 if particle == 'helium' else 1
        )

    def linear(x, m, b):
        return m * x + b

    fit = all_data.query('E > 100')
    params, cov = np.polyfit(np.log10(fit.E), np.log10(fit.y), 1, cov=True)
    err = np.sqrt(np.diag(cov))

    with open(f'build/{particle}_index.tex', 'w') as f:
        f.write(r'\num{' + f'{params[0]:.3f}' + '}\n')

    with open(f'build/{particle}_norm.tex', 'w') as f:
        f.write(r'\num{' + f'{10**params[1]:.1f}' + '}\n')

    with open(f'build/{particle}_cov.tex', 'w') as f:
        f.write(r'\begin{pmatrix*}[r]' + '\n')
        f.write(f'{cov[0, 0]:.6f} & {cov[0, 1]:.6f}' + r'\\' + '\n')
        f.write(f'{cov[1, 0]:.6f} & {cov[1, 1]:.6f}' + r'\\' + '\n')
        f.write(r'\end{pmatrix*}' + '\n')

    if particle != 'electron':
        e = np.logspace(2, 6, 100)
    else:
        e = np.logspace(2, 3.5, 100)
    plt.plot(
        e, e**2 * 10**linear(np.log10(e), *params),
        color='gray',
        alpha=0.3 if particle == 'helium' else 1
    )

plt.grid()
plt.legend(ncol=3, bbox_to_anchor=[0.5, 1.025], loc='lower center')
plt.yscale('log')
plt.xscale('log')
plt.xlabel(r'$E \mathbin{/} \si{\GeV}$')

plt.ylabel(
    r'$E^2 \frac{\symup{d}N}{\symup{d}E} \bigm/'
    r' \bigl(\si{\GeV\per\square\meter\per\second\per\steradian}\bigr)$'
)

plt.tight_layout(pad=0)
plt.savefig(args.outputfile)
