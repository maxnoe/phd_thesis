import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('outputfile')
args = parser.parse_args()


df = pd.read_json('../data/ft_coordinates_comparison.json')
df['obstime'] = pd.to_datetime(df['obstime'])
df['distance'] *= 3600

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
df.plot('obstime', 'distance', ax=ax, legend=False)
ax.set_xlabel('')
ax.set_ylabel('distance / arcseconds')
fig.tight_layout(pad=0)
fig.savefig(args.outputfile)
