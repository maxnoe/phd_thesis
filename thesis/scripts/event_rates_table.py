from fact.io import read_h5py
import h5py




for apa in [85, 95, 100]:
    cleaning = '../data/dl2/simulations/v1.1.2/apa{}/gammas_wobble_corsika76900.hdf5'
    precuts = '../build/apa{}/gamma_precuts.hdf5'
    test = '../build/apa{}/gamma_test_dl3.hdf5'

    print(f'APA {apa}%')
    print('Gammas')
    n_events = h5py.File(cleaning.format(apa), mode='r')['events/event_num'].shape[0]
    print('Events after cleaning: ', n_events)

    n_events = h5py.File(precuts.format(apa), mode='r')['events/event_num'].shape[0]
    print('Events after precuts:  ', n_events)

    df = read_h5py(test.format(apa), key='events', columns=['gamma_prediction', 'theta_deg'])
    n_events = len(df.query('gamma_prediction > 0.8 and theta_deg < sqrt(0.02)'))
    print('Events after selection:', n_events)

    print('\nProtons')

    cleaning = '../data/dl2/simulations/v1.1.2/apa85/protons_corsika76900.hdf5'
    precuts = '../build/apa{}/proton_precuts.hdf5'
    test = '../build/apa{}/proton_test_dl3.hdf5'

    print(f'APA {apa}%')
    n_events = h5py.File(cleaning.format(apa), mode='r')['events/event_num'].shape[0]
    print('Events after cleaning:  ', n_events)

    n_events = h5py.File(precuts.format(apa), mode='r')['events/event_num'].shape[0]
    print('Events after precuts:   ', n_events)

    df = read_h5py(test.format(apa), key='events', columns=['gamma_prediction', 'theta_deg'])
    n_events = len(df.query('gamma_prediction > 0.8 and theta_deg < sqrt(0.02)'))
    print('Events after selection: ', n_events)

    print('\nData')
    cleaning = '../data/dl2/observations/v1.1.2/crab1314_v1.1.2.hdf5'
    precuts = '../build/apa{}/crab_precuts.hdf5'
    test = '../build/apa{}/crab_dl3.hdf5'

    print(f'APA {apa}%')
    n_events = h5py.File(cleaning.format(apa), mode='r')['events/event_num'].shape[0]
    print('Events after cleaning:  ', n_events)

    n_events = h5py.File(precuts.format(apa), mode='r')['events/event_num'].shape[0]
    print('Events after precuts:   ', n_events)

    df = read_h5py(test.format(apa), key='events', columns=['gamma_prediction', 'theta_deg'])
    n_events = len(df.query('gamma_prediction > 0.8 and theta_deg < sqrt(0.02)'))
    print('Events after selection: ', n_events)
    print('\n')


print('\nProtons MMCS 6.5')
cleaning = '../data/dl2/simulations/v1.1.2/apa85/protons_mmcs6500.hdf5'
# precuts = '../build/apa85-mmcs6500/crab_precuts.hdf5'
# test = '../build/apa85-mmcs6500/crab_dl3.hdf5'

n_events = h5py.File(cleaning.format(apa), mode='r')['events/event_num'].shape[0]
print('Events after cleaning:  ', n_events)

# n_events = h5py.File(precuts.format(apa), mode='r')['events/event_num'].shape[0]
# print('Events after precuts:   ', n_events)

# df = read_h5py(test.format(apa), key='events', columns=['gamma_prediction', 'theta_deg'])
# n_events = len(df.query('gamma_prediction > 0.8 and theta_deg < sqrt(0.02)'))
# print('Events after selection: ', n_events)
# print('\n')
