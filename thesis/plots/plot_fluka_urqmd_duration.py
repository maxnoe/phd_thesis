import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()



df = pd.read_csv('../data/runtimes_fluka_urqmd.csv')
df['duration'] /= 3600

limits = df.duration.min(), df.duration.max()

for name, group in df.groupby('name'):
    label = r'\texttt{FLUKA}' if 'fluka' in name else r'\texttt{URQMD}'
    plt.hist(
        group['duration'],
        bins=35,
        histtype='step',
        range=limits,
        label=label
    )

plt.xlabel('Duration ${} \mathbin{/} \si{\hour}')
plt.legend()
plt.tight_layout(pad=0)
plt.savefig(args.outputfile)
