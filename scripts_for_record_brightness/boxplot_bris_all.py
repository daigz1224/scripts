# Author: daiguozheng
# 用法： python3 boxplot_bris_all.py
# 说明：从 pkl 读取并画出 boxplot 图

import pickle
import numpy as np
import matplotlib.pyplot as plt

def main(pkl):
    pkl_name = pkl.split('/')[-1]

    with open(pkl, 'rb') as f:
        bris_all = pickle.load(f)

    bris_all_filter = []
    for bris in bris_all:
        bris_numpy = np.array(bris)
        mu = np.mean(bris_numpy)  # 同一个时间序列的亮度均值
        var = np.var(bris_numpy)  # 同一个时间序列的亮度方差
        threshold = 3  # 筛选出 (mu - threshold * var, mu + threshold * var) 内的亮度
        bris_numpy_filter = bris_numpy[(bris_numpy > mu - threshold * var) & (bris_numpy < mu + threshold * var)]
        print('After filter: ' + str(len(bris_numpy_filter)) + ' / ' + str(len(bris_numpy)))

        bris_all_filter.append(bris_numpy_filter.tolist())
        
    plt.figure()
    plt.boxplot(bris_all_filter, sym='r')
    plt.xlabel('time index')
    plt.ylabel('brightness')
    plt.title(pkl_name)
    plt.show()

if __name__ == '__main__':
    pkl_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_rain_1_minutes.pkl"
    main(pkl_path)