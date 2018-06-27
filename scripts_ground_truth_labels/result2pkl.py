# coding: utf-8
import os
import json
import pickle

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

def is_results_line(line):
    fields = line.split()
    return len(fields) == 5 and fields[0].endswith(".bag")    

def main(txt_path, pkl_path):
    with open(txt_path, 'r') as fp:
        info_lines = [line.split() for line in fp if is_results_line(line)]
    print("info_lines = %d\n", info_lines)
    res_pkl = {}
    for label in enumerate(info_lines):  
        # bag_name = label[0]
        # jpg_path = label[2]
        # numberBox = result_dict['numberBox']
        result = label[3]
        result_dict = json.loads(result)

        for obstacle_dict in result_dict['result']:
            tag = LABEL_MAP[obstacle_dict['tag']]
            if tag not in obstacle_dict:
                res_pkl[tag] = []
            x = float(obstacle_dict["x"])
            y = float(obstacle_dict["y"])
            w = float(obstacle_dict["w"])
            h = float(obstacle_dict["h"])
            res_pkl[tag].append([x, y, w, h])
    with open(pkl_path, 'w') as fw:
        pickle.dump(res_pkl, fw)

if __name__ == '__main__':
    data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files'
    folder = 'mark_task_2988-layer1-city-test-LAYER1_BARRIER_2018'
    txt_path = data_root + '/' + folder + '/' + 'result.txt'
    pkl_path = data_root + '/' + folder + '.pkl'

    print("txt_path: " + txt_path)
    print("pkl_path: " + pkl_path)
    main(txt_path, pkl_path)

    print("End.")