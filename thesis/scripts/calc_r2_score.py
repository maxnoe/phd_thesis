from sklearn.metrics import r2_score
from fact.io import read_h5py
from argparse import ArgumentParser
import numpy as np


def r2(s):
    return r2_score(s['label'].values, s['label_prediction'].values)


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('outputfile')
args = parser.parse_args()


df = read_h5py(args.inputfile)
score = df.groupby('cv_fold').apply(r2)

with open(args.outputfile, 'w') as f:
    f.write(r'\num{' f'{score.mean():.3f} +- {score.std():.3f}' '}')
