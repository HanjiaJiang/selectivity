import sys
import numpy as np
import pickle

output_list = sys.argv[1:]

orientation_list = np.linspace(0.0, np.pi/2, num=len(output_list))

for output_path, orientation_val in zip(output_list, orientation_list):
    para_dict = {
        'on_server': False,
        't_sim': 2000.0,
        'th_start': 1500.0,
        'orientation': orientation_val
    }
    with open(output_path, 'wb') as handle:
        pickle.dump(para_dict, handle)

