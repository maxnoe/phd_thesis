from argparse import ArgumentParser
import re

parser = ArgumentParser()
parser.add_argument('log_file')
parser.add_argument('output_base')
args = parser.parse_args()


with open(args.log_file) as f:
    log = f.read()


acc = re.search(r'Mean accuracy from CV: (.*)', log).groups()[0]

with open(args.output_base + '_accuracy.tex', 'w') as f:
    f.write(r'\num{' + acc.replace('±', r'\pm') + '}\n')


r2 = re.search(r'score from CV: (.*)', log).groups()[0]

with open(args.output_base + '_r2.tex', 'w') as f:
    f.write(r'\num{' + r2.replace('±', r'\pm') + '}\n')
