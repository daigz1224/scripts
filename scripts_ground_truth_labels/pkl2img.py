# coding: utf-8
import pickle
import numpy as np
import matplotlib.pyplot as plt

IMAGE_W = 1920
IMAGE_H = 1080

LABEL_MAP = {
    1:    'car',
    2:    'truck',
    3:    'van',
    4:    'bus',
    5:    'pedestrian',
    6:    'cyclist',
    7:    'tricyclelist',
    8:    'motorcyclist',
    12:    'barrowlist',
    13:    'pedestrianignore',
    14:    'carignore',
    15:    'othersignore',
    16:    'trafficcone',
    17:    'confused',
}

def main(pkl_path, obstacles):
    with open(pkl_path, 'rb') as fp:
        res_pkl = pickle.load(fp)
    heap = np.zeros( (IMAGE_H, IMAGE_W) )
    for ob in obstacles:
        for box in res_pkl[ob]:
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            cent_x, cent_y = x + 0.5 * w, y + 0.5 * h
            heap[cent_y][cent_x] = heap[cent_y][cent_x] + 1
    plt.imshow()
    plt.show()



if __name__=='__main__':
    data_root = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files"
    pkl_name = "mark_task_2988-layer1-city-test-LAYER1_BARRIER_2018.pkl"
    obstacles = ['car']

    pkl_path = data_root + '/' + pkl_name
    print("pkl_path: " + pkl_path)
    print(obstacles)
    main(pkl_path)
    print("End.")