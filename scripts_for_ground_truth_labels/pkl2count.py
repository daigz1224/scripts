# coding: utf-8
import os
import sys
import logging
import pickle

import matplotlib
matplotlib.use('Agg')  # plt.show() or not

import matplotlib.pyplot as plt

# 障碍物类型
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
    18:    'noidea1',
    19:    'noidea2'
}

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

# myfigsize = (20,15)
myfigsize = (20, 10)
mydpi = 72

IMAGE_W = 1920
IMAGE_H = 1080

def main(ob='all'):
    """
    主程序
    :param ob:
    :return:
    """
    ob_list = []
    if ob == 'all':
        ob_list = ob_list + [LABEL_MAP[key] for key in LABEL_MAP]
    else:
        if ob not in [LABEL_MAP[key] for key in LABEL_MAP]:
            logging.error("No this kind of obstalce.")
            exit(-1)
        ob_list.append(ob)
    logging.debug("ob_list = " + str(ob_list))
    # 确认输入输出路径
    if len(ob_list) == 1:
        suffix = ob_list[0]
    else:
        suffix = 'all'
    dirres = os.path.join(data_root + '/result_' + suffix)
    dirplt = os.path.join(dirres, 'data_plt')

    obstacle_dict_pkl_path = os.path.join(data_root, 'obstacle_dict.pkl')
    if os.path.exists(obstacle_dict_pkl_path):
        logging.debug("opening obstacle_dict.pkl of ...")
        with open(obstacle_dict_pkl_path, 'rb') as fr:
            obstacle_dict = pickle.load(fr)
            logging.debug("obstacle_dict.pkl loaded.")
    else:
        obstacle_dict = {}
        logging.error("obstacle_dict.pkl not found.")
        exit(-1)

    count_dict = {}
    for ob in ob_list:
        count_dict[ob] = [0, 0, 0]  # all, istruncated, isoccluded
        for info in obstacle_dict[ob]:
            count_dict[ob][0] = count_dict[ob][0] + 1  # 总共
            if info[2]['istruncated'] == 1:
                count_dict[ob][1] = count_dict[ob][1] + 1  # 截断
            if info[2]['isoccluded'] > 0:
                count_dict[ob][2] = count_dict[ob][2] + 1  # 遮挡
    # 输出
    for ob in ob_list:
        ob_all = count_dict[ob][0]
        ob_istruncated = count_dict[ob][1]
        ob_isoccluded = count_dict[ob][2]
        ob_istruncated_percentage = 100 * ob_istruncated / ob_all
        ob_isoccluded_percentage = 100 * ob_isoccluded / ob_all
        logging.info("'%s': %d, %s: %d (%.2f%%), %s: %d (%.2f%%)" %
                     (ob, ob_all, "istruncated", ob_istruncated, ob_istruncated_percentage,
                      "isoccluded", ob_isoccluded, ob_isoccluded_percentage))
    # 画图
    plt.figure(figsize=myfigsize, dpi=mydpi)
    bar_width = 0.2

    count_all = [count_dict[ob][0] for ob in count_dict]
    count_tru = [count_dict[ob][1] for ob in count_dict]
    count_occ = [count_dict[ob][2] for ob in count_dict]

    index = [i + 1 for i in list(range(len(count_all)))]

    plt.bar(index, count_all,
            width=bar_width, edgecolor='white', label='all')
    plt.bar([i + bar_width for i in index], count_occ,
            width=bar_width, edgecolor='white', label='isoccluded')
    plt.bar([i + bar_width * 2 for i in index], count_tru,
            width=bar_width, edgecolor='white', label='istruncated')

    plt.xticks([i + bar_width for i in index], list(count_dict.keys()))
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(dirplt, 'count_tru_occ.jpg'), bbox_inches ='tight')
    plt.show()


if __name__ == '__main__':
    # 数据目录
    data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703'
    dirdata = os.path.join(data_root, 'data')
    # ob_str = sys.argv[1]
    # 运行主程序
    main()