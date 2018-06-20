# boxplot_bris_all.py
import matplotlib.pyplot as plt
import numpy as np
import pickle

pkl_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_rain_1_minutes.pkl"
pkl_name = pkl_path.split('/')[-1]

with open(pkl_path, 'rb') as f:
    bris_all = pickle.load(f)

bris_all_filter = []

for bris in bris_all:
    bris_numpy = np.array(bris)
    mu = np.mean(bris_numpy)
    var = np.var(bris_numpy)
    threshold = 3
    bris_numpy_filter = bris_numpy[(bris_numpy > mu - threshold * var) & (bris_numpy < mu + threshold * var)]
    print('after filter: ' + str(len(bris_numpy_filter)) + ' / ' + str(len(bris_numpy)))
    bris_all_filter.append(bris_numpy_filter.tolist())
    
plt.figure()
plt.boxplot(bris_all_filter, sym='x')
plt.xlabel('time index')
plt.ylabel('brightness')
plt.title(pkl_name + ': 11:10 - 11:19 + 19:34 - 19:38')
plt.show()