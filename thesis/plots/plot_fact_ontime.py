from fact.factdb import RunInfo, Source, SourceType, read_into_dataframe, ontime
from peewee import fn
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import pandas as pd

parser = ArgumentParser()
parser.add_argument('outputfile')
parser.add_argument('--download', action='store_true')
args = parser.parse_args()


if args.download:
    q = (
        RunInfo
        .select(
            Source.fsourcename.alias('source'),
            fn.SUM(ontime).alias('ontime')
        )
        .join(Source, on=RunInfo.fsourcekey == Source.fsourcekey)
        .join(SourceType, on=Source.fsourcetypekey == SourceType.fsourcetypekey)
        .where(SourceType.fsourcetypename == 'TeVSource')
        .group_by(Source.fsourcename)
        .order_by(fn.SUM(ontime).desc())
        .limit(10)
    )

    df = read_into_dataframe(q)
    df.set_index('source', inplace=True)
    df.to_csv('../data/fact_obstime.csv')


df = pd.read_csv('../data/fact_obstime.csv', index_col=0)
ontime = df.ontime
ontime /= 3600
ontime[ontime > 100].sort_values().plot.barh()

plt.xlabel('Observation time per source / hours')
plt.ylabel('')
plt.tight_layout(pad=0)
plt.savefig(args.outputfile)
