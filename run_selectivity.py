import pickle
import os
import sys
import numpy as np
from random import sample
import multiprocessing as mp

if __name__ == "__main__":

    input_path = sys.argv[1]
    with open(input_path, 'rb') as handle:
        para_dict = pickle.load(handle)
    data_path = os.path.dirname(sys.argv[2])

    # for item in os.listdir():
    #     if 'para_dict' in item:
    #         with open('para_dict.pickle', 'rb') as handle:
    #             para_dict = pickle.load(handle)
    #         print('changed para_dict:')
    #         print(para_dict)
    #         break

    cwd = os.getcwd()

    # import modules
    microcircuit_path = '/home/hanjia/Documents/microcircuit/'
    if os.path.isdir(cwd + '/microcircuit/'):
        microcircuit_path = cwd + '/microcircuit/'
    sys.path.insert(1, microcircuit_path)

    analysis_path = '/home/hanjia/Documents/analysis/'
    if os.path.isdir(cwd + '/analysis/'):
        analysis_path = cwd + '/analysis/'
    sys.path.insert(1, analysis_path)

    import network
    from network_params import net_dict
    from sim_params import sim_dict
    from stimulus_params import stim_dict
    import microcircuit_tools as tools

    # assign parameters
    if para_dict['on_server']:
        cpu_ratio = 1
    else:
        cpu_ratio = 0.5

    # change network parameters
    sim_dict['local_num_threads'] = int(mp.cpu_count() * cpu_ratio)
    sim_dict['t_sim'] = para_dict['t_sim']
    sim_dict['data_path'] = data_path
    stim_dict['th_start'] = np.arange(para_dict['th_start'],
                                      para_dict['t_sim'],
                                      (para_dict['t_sim'] -
                                       para_dict['th_start'])/2)
    stim_dict['orientation'] = para_dict['orientation']

    net = network.Network(sim_dict, net_dict, stim_dict)
    net.setup()
    net.simulate()
    tools.plot_raster(
        sim_dict['data_path'], 'spike_detector',
        stim_dict['th_start'][0] - 100.0,
        stim_dict['th_start'][0] + 100.0)
    mean_fr_cache, std_fr = \
        tools.fire_rate(sim_dict['data_path'], 'spike_detector', 500.0, 1500.0)
    tools.boxplot(net_dict, sim_dict['data_path'])
