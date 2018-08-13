# coding: utf-8
import os
import sys
import logging
import pickle
import random
import numpy as np

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

myfigsize = (20,15)
mydpi = 72

IMAGE_W = 1920
IMAGE_H = 1080

# 检测框的颜色仓库
box_colors = [(random.randint(0, 255),
               random.randint(0, 255),
               random.randint(0, 255)) for ob in range(20)]

def plot_palace(palace_dict, target, ob_list, dirplt):
    """
    绘制九宫格分析图
    :param palace_dict:
    :param target:
    :param ob_list
    :param dirplt:
    :return:
    """
    plt.figure(figsize=myfigsize, dpi=mydpi)
    palace_list = ['lt', 'mt', 'rt',
                   'lm', 'mm', 'rm',
                   'lb', 'mb', 'rb']
    for i in range(1, 10):
        plt.subplot(3, 3, i)
        p = palace_list[i - 1]
        if target == 'ratio':
            data = [info[2]['h'] / info[2]['w'] for info in palace_dict[p]]
            plt.boxplot(data, vert=False, sym='.r', showmeans=True, showfliers=False)
        elif target == 'width':
            data = [info[2]['w'] for info in palace_dict[p]]
            plt.boxplot(data, vert=False, sym='.r', showmeans=True, showfliers=False)
        elif target == 'height':
            data = [info[2]['h'] for info in palace_dict[p]]
            plt.boxplot(data, vert=False, sym='.r', showmeans=True, showfliers=False)
        else:
            logging.error("No specific target.")

        plt.grid(linestyle='--')
        plt.title('count: ' + str(len(palace_dict[p])))

    plt.suptitle(target + ' of the bounding box in each palace of ' + str(ob_list))
    plt.savefig(os.path.join(dirplt, 'palace_' + target + '.jpg'), bbox_inches ='tight')
    plt.show()
    logging.debug('palace_' + target + '.jpg saved.')

def plot_obstacle(obstacle_dict, target, ob_list, dirplt):
    """
    根据障碍物类型绘制分析图
    :param obstacle_dict:
    :param target:
    :param ob_list:
    :param dirplt:
    :return:
    """
    obstacle_ratio = []
    obstacle_height = []
    obstacle_width = []

    for ob in ob_list:
        obstacle_ratio = obstacle_ratio + \
                         [ info[2]['h'] / info[2]['w'] for info in obstacle_dict[ob]]
        obstacle_height = obstacle_height + \
                          [ info[2]['h'] for info in obstacle_dict[ob]]
        obstacle_width = obstacle_width + \
                         [ info[2]['w'] for info in obstacle_dict[ob]]

    obstacle_ratio_np = np.array(obstacle_ratio)
    obstacle_height_np = np.array(obstacle_height)
    obstacle_width_np = np.array(obstacle_width)

    plt.figure(figsize=(20, 10))
    n_bin = 200
    if target == 'ratio':
        plt.title(str(ob_list) + ' ratio range in ' + str(round(obstacle_ratio_np.min(), 2)) +
                  '~' + str(round(obstacle_ratio_np.max(), 2)))
        upper_r = round(obstacle_ratio_np.max(), 2) / 2
        gap_r = upper_r / n_bin
        bins = list(np.arange(0, upper_r, gap_r))
        plt.hist(obstacle_ratio_np, bins)

    elif target == 'height':
        plt.title(str(ob_list) + ' height range in ' + str(round(obstacle_height_np.min(), 2)) +
                  '~' + str(round(obstacle_height_np.max(), 2)))
        upper_h = round(obstacle_height_np.max(), 2) / 2
        gap_h = upper_h / n_bin
        bins = list(np.arange(0, upper_h, gap_h))
        plt.hist(obstacle_height_np, bins)

    elif target == 'width':
        plt.title(str(ob_list) + ' width range in ' + str(round(obstacle_width_np.min(), 2)) +
                  '~' + str(round(obstacle_width_np.max(), 2)))
        upper_w = round(obstacle_width_np.max(), 2) / 2
        gap_w = upper_w / n_bin
        bins = list(np.arange(0, upper_w, gap_w))
        plt.hist(obstacle_width_np, bins)
    else:
        logging.error("target not found.")

    plt.savefig(os.path.join(dirplt, 'obstacle_' + target + '.jpg'), bbox_inches ='tight')
    plt.show()
    logging.debug('obstacle_' + target + '.jpg saved.')

def main(ob):
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
    dirpkl = os.path.join(dirres, 'data_pkl')
    dirplt = os.path.join(dirres, 'data_plt')

    if os.path.exists(dirplt):
        logging.debug(dirplt + " alreadly exists.")
    else:
        os.mkdir(dirplt)
        logging.debug("making folder: " + dirplt)

    # info_list_pkl_path = os.path.join(dirpkl, 'info_list.pkl')
    # if os.path.exists(info_list_pkl_path):
    #     logging.debug("opening info_list.pkl of ...")
    #     with open(info_list_pkl_path, 'rb') as fr:
    #         info_list = pickle.load(fr)
    #         logging.debug("info_list.pkl loaded.")
    # else:
    #     info_list = []
    #     logging.error("info_list.pkl not found.")

    center_pkl_path = os.path.join(dirpkl, 'center.pkl')

    if os.path.exists(center_pkl_path):
        logging.debug("opening center.pkl of ...")
        with open(center_pkl_path, 'rb') as fr:
            center = pickle.load(fr)
            logging.debug("center.pkl loaded.")
    else:
        center = []
        logging.error("center.pkl not found.")
        exit(-1)

    cover_pkl_path = os.path.join(dirpkl, 'cover.pkl')
    # logging.debug(cover_pkl_path)
    if os.path.exists(cover_pkl_path):
        logging.debug("opening cover.pkl of ...")
        with open(cover_pkl_path, 'rb') as fr:
            cover = pickle.load(fr)
            logging.debug("cover.pkl loaded.")
    else:
        cover = []
        logging.error("cover.pkl not found.")
        exit(-1)

    palace_dict_pkl_path = os.path.join(dirpkl, 'palace_dict.pkl')
    if os.path.exists(palace_dict_pkl_path):
        logging.debug("opening palace_dict.pkl of ...")
        with open(palace_dict_pkl_path, 'rb') as fr:
            palace_dict = pickle.load(fr)
            logging.debug("palace_dict.pkl loaded.")
    else:
        palace_dict = {}
        logging.error("palace_dict.pkl not found.")
        exit(-1)

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

    ## 画图：center_point_heap.jpg
    plt.figure(figsize=myfigsize, dpi=mydpi)
    plt.title('center point of ' + str(ob_list))
    plt.imshow(center)
    plt.savefig(os.path.join(dirplt, 'center_point_heap.jpg'), bbox_inches ='tight')
    plt.show()
    # 画图：cover_area_heap.jpg
    plt.figure(figsize=myfigsize, dpi=mydpi)
    plt.title('cover area of ' + str(ob_list))
    plt.imshow(cover)
    plt.savefig(os.path.join(dirplt, 'cover_area_heap.jpg'), bbox_inches ='tight')
    plt.show()
    # 画图：palace_ratio.jpg palace_width.jpg palace_height.jpg
    plot_palace(palace_dict, 'ratio', ob_list, dirplt)
    plot_palace(palace_dict, 'width', ob_list, dirplt)
    plot_palace(palace_dict, 'height', ob_list, dirplt)
    # 画图：obstacle_ratio.jpg obstacle_width.jpg obstacle_height.jpg
    plot_obstacle(obstacle_dict, 'ratio', ob_list, dirplt)
    plot_obstacle(obstacle_dict, 'width', ob_list, dirplt)
    plot_obstacle(obstacle_dict, 'height', ob_list, dirplt)

if __name__ == '__main__':
    # 数据目录
    data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703'
    dirdata = os.path.join(data_root, 'data')
    ob_str = sys.argv[1]
    # 运行主程序
    main(ob_str)