from fact.io import read_h5py
from collections import defaultdict
from pprint import pprint


APA = 85

dl3_columns = ['gamma_prediction', 'theta_deg']


event_nums = defaultdict(dict)
event_nums['Crab Observations']['trigger'] = 21898338
event_nums['Diffuse gammas']['trigger'] = 1491524
event_nums['Wobble gammas']['trigger'] = 11304586
event_nums['Protons']['trigger'] = 8709718
event_nums['Helium']['trigger'] = 314812

threshold = float(open(f'build/threshold_apa{APA}.txt').read())
theta2_cut = float(open(f'build/theta2_cut_apa{APA}.txt').read())

datasets = {
    'Protons': [
        f'../data/dl2/simulations/v1.1.2/apa{APA}/protons_corsika76900.hdf5',
        f'../build/apa{APA}/proton_precuts.hdf5',
        f'../build/apa{APA}/proton_test_dl3.hdf5',
    ],
    'Helium': [
        f'../data/dl2/simulations/v1.1.2/apa{APA}/helium4_corsika76900.hdf5',
        f'../build/apa{APA}/helium_precuts.hdf5',
        f'../build/apa{APA}/helium_dl3.hdf5',
    ],
    'Wobble gammas': [
        f'../data/dl2/simulations/v1.1.2/apa{APA}/gammas_wobble_corsika76900.hdf5',
        f'../build/apa{APA}/gamma_precuts.hdf5',
        f'../build/apa{APA}/gamma_test_dl3.hdf5',
    ],
    'Diffuse gammas': [
        f'../data/dl2/simulations/v1.1.2/apa{APA}/gammas_diffuse_corsika76900.hdf5',
        f'../build/apa{APA}/gamma_diffuse_precuts.hdf5',
    ],
    'Crab Observations': [
        '../data/dl2/observations/v1.1.2/crab1314_v1.1.2.hdf5',
        f'../build/apa{APA}/crab_precuts.hdf5',
        f'../build/apa{APA}/crab_dl3.hdf5',
    ]
}

for label, dataset in datasets.items():
    f = dataset[0]
    event_nums[label]['ft'] = len(read_h5py(f, key='events', columns=['event_num']))

    f = dataset[1]
    event_nums[label]['precuts'] = len(read_h5py(f, key='events', columns=['event_num']))

    if len(dataset) < 3:
        continue

    f = dataset[2]
    df = read_h5py(f, key='events', columns=dl3_columns)
    df = df.query(f'gamma_prediction >= {threshold}')
    event_nums[label]['threshold'] = len(df)

    event_nums[label]['on'] = len(df.query(f'theta_deg <= sqrt({theta2_cut})'))


with open('build/event_num_table.tex', 'w') as f:
    f.write(r'\begin{tabular}{l r r r r r}' + '\n')
    f.write(r'  \toprule' + '\n')
    f.write(r'  Dataset & Triggered & Image Cleaning & Pre-Selection & Separation & On-Region \\' + '\n')
    f.write(r'  \midrule' + '\n')

    for key, events in event_nums.items():
        f.write('  ' + key)
        for k in ('trigger', 'ft', 'precuts', 'threshold', 'on'):
            val = events.get(k, '—')
            f.write(f'& {val}')
        f.write(r' \\' + '\n')
    f.write(r'  \bottomrule' + '\n')
    f.write(r'\end{tabular}' + '\n')
