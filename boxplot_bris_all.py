# boxplot_bris_all.py
import matplotlib.pyplot as plt
import numpy as np
import pickle

pkl_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_night_5_minutes.pkl"
pkl_name = pkl_path.split('/')[-1]

with open(pkl_path, 'rb') as f:
    bris_all = pickle.load(f)

bris_all_3var = []

for bris in bris_all:
    bris_numpy = np.array(bris)
    print('origin num of bris: ' + str(len(bris_numpy)))
    mu = np.mean(bris_numpy)
    var = np.var(bris_numpy)
    bris_numpy_3var = bris_numpy[(bris_numpy > mu - 3 * var) & (bris_numpy < mu + 3 * var)]
    print('after filter 3 var: ' + str(len(bris_numpy_3var)))
    bris_all_3var.append(bris_numpy_3var.tolist())

plt.figure()
plt.boxplot(bris_all_3var)
plt.xlabel("time index")
plt.ylabel("brightness")
plt.title(pkl_name)
plt.show()