# coding: utf-8
import os
import sys
import logging
import json
import pickle
import numpy as np

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

IMAGE_W = 1920
IMAGE_H = 1080

def extract_info_from_txt(txt_path):
    """
    提取 result.txt 中有用的信息，包括每张图片的所属视频片段、帧号以及标注信息等
    :param txt_path: path/to/result.txt
    :return: info_list
    """
    with open(txt_path, 'r') as fp:
        info_list = []
        for line in fp:
            info = line.split()
            if len(info) == 5 and info[0].endswith(".bag"):
                info_list.append(info)
    # logging.debug("len(info_lines) = %d" % len(info_list))
    return info_list

def cent_heap(info_list, ob_list):
    """
    返回检测框中心位置的热力图
    :param info_list:
    :param ob_list:
    :return: center
    """
    center = np.zeros((IMAGE_H, IMAGE_W))
    total = 0
    valid = 0
    for info in info_list:
        label = json.loads(info[3])
        result = label['result']
        # video_name: MKZ078_23_1522650020_1522650320.bag
        # video_name = label['videoName']
        # frame_id: 4170
        # frame_id = label['frameId']
        # jpg_name: MKZ078_23_1522650020_1522650320_4170
        # jpg_name = video_name.split('.')[0] + '_' + str(frame_id)
        for res in result:
            ob = LABEL_MAP[res['tag']]
            if ob not in ob_list:
                continue
            x = res['x']
            y = res['y']
            h = res['h']
            w = res['w']
            cent_x, cent_y = int(x + 0.5 * w), int(y + 0.5 * h)
            total = total + 1
            if cent_x >= IMAGE_W or cent_y >= IMAGE_H:
                continue
            center[cent_y, cent_x] = center[cent_y, cent_x] + 1
            valid = valid + 1
    logging.debug("center point total = " + str(total))
    logging.debug("center point valid = " + str(valid))
    return center

def cover_heap(info_list, ob_list):
    """
    返回检测框覆盖范围的热力图
    :param info_list:
    :param ob_list:
    :return: cover
    """
    cover = np.zeros((IMAGE_H, IMAGE_W))
    for info in info_list:
        label = json.loads(info[3])
        result = label['result']
        # video_name: MKZ078_23_1522650020_1522650320.bag
        # video_name = label['videoName']
        # frame_id: 4170
        # frame_id = label['frameId']
        # jpg_name: MKZ078_23_1522650020_1522650320_4170
        # jpg_name = video_name.split('.')[0] + '_' + str(frame_id)
        for res in result:
            ob = LABEL_MAP[res['tag']]
            if ob not in ob_list:
                continue
            x_min = int(res['x'])
            y_min = int(res['y'])
            h = res['h']
            w = res['w']
            x_max = int(x_min + w)
            y_max = int(y_min + h)
            if x_max >= IMAGE_W:
                x_max = IMAGE_W - 1
            if y_max >= IMAGE_H:
                y_max = IMAGE_H - 1
            cover[y_min:y_max, x_min:x_max] = cover[y_min:y_max, x_min:x_max] + 1
    return cover

def palace_partition(info_list, ob_list):
    """
    划分九宫格，将中心点位于对应宫格内的检测框存到对应字典中
    :param info_list:
    :param ob_list:
    :return: palace_dict
    """
    palace_dict = {'lt': [], 'mt': [], 'rt': [],
                   'lm': [], 'mm': [], 'rm': [],
                   'lb': [], 'mb': [], 'rb': []}
    for info in info_list:
        label = json.loads(info[3])
        result = label['result']
        # video_name: MKZ078_23_1522650020_1522650320.bag
        video_name = label['videoName']
        # frame_id: 4170
        frame_id = label['frameId']
        # jpg_name: MKZ078_23_1522650020_1522650320_4170
        # jpg_name = video_name.split('.')[0] + '_' + str(frame_id))
        for res in result:
            ob = LABEL_MAP[res['tag']]
            if ob not in ob_list:
                continue
            x = res['x']
            y = res['y']
            h = res['h']
            w = res['w']
            cent_x, cent_y = int(x + 0.5 * w), int(y + 0.5 * h)
            if cent_x >= IMAGE_W or cent_y >= IMAGE_H:
                continue
            # find target palace and append useful info
            if cent_x <= IMAGE_W / 3:
                if cent_y <= IMAGE_H / 3:
                    palace_dict['lt'].append([video_name, frame_id, res])
                elif cent_y <= IMAGE_H * 2 / 3:
                    palace_dict['lm'].append([video_name, frame_id, res])
                else:
                    palace_dict['lb'].append([video_name, frame_id, res])
            elif cent_x <= IMAGE_W * 2 / 3:
                if cent_y <= IMAGE_H / 3:
                    palace_dict['mt'].append([video_name, frame_id, res])
                elif cent_y <= IMAGE_H * 2 / 3:
                    palace_dict['mm'].append([video_name, frame_id, res])
                else:
                    palace_dict['mb'].append([video_name, frame_id, res])
            else:
                if cent_y <= IMAGE_H / 3:
                    palace_dict['rt'].append([video_name, frame_id, res])
                elif cent_y <= IMAGE_H * 2 / 3:
                    palace_dict['rm'].append([video_name, frame_id, res])
                else:
                    palace_dict['rb'].append([video_name, frame_id, res])

    # logging.debug("ob_list: " + str(ob_list))
    # palace_list = ['lt', 'mt', 'rt',
    #                'lm', 'mm', 'rm',
    #                'lb', 'mb', 'rb']
    # for p in palace_list:
    #     logging.info("#palace %s: %d" % (p, len(palace_dict[p])))
    #     print("#palace %s: %d" % (p, len(palace_dict[p])))
    return palace_dict

def obstacle_partition(info_list):
    """
    按照障碍物类型进行统计
    :param info_list:
    :return: obstacle_dict:
    """
    obstacle_dict = {}
    for ob in [LABEL_MAP[key] for key in LABEL_MAP]:
        obstacle_dict[ob] = []

    for info in info_list:
        label = json.loads(info[3])
        result = label['result']
        # video_name: MKZ078_23_1522650020_1522650320.bag
        video_name = label['videoName']
        # frame_id: 4170
        frame_id = label['frameId']
        # jpg_name: MKZ078_23_1522650020_1522650320_4170
        # jpg_name = video_name.split('.')[0] + '_' + str(frame_id))
        for res in result:
            ob = LABEL_MAP[res['tag']]
            obstacle_dict[ob].append([video_name, frame_id, res])

    return obstacle_dict

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
    # 建立输出目录
    if len(ob_list) == 1:
        suffix = ob_list[0]
    else:
        suffix = 'all'
    dirres = os.path.join(data_root + '/result_' + suffix)
    dirpkl = os.path.join(dirres, 'data_pkl')
    if os.path.exists(dirres):
        logging.debug(dirres + "alreadly exists.")
    else:
        logging.debug("making folder: " + dirres)
        os.mkdir(dirres)
    if os.path.exists(dirpkl):
        logging.debug(dirpkl + "alreadly exists.")
    else:
        os.mkdir(dirpkl)
        logging.debug("making folder: " + dirpkl)

    # 生成源数据所有的标注信息列表 info_list.pkl
    info_list_pkl_path = os.path.join(data_root, 'info_list.pkl')
    if os.path.exists(info_list_pkl_path):
        logging.debug("opening info_list.pkl of " + str(ob_list) + "...")
        with open(info_list_pkl_path, 'rb') as fr:
            info_list = pickle.load(fr)
            logging.debug("info_list.pkl loaded.")
    else:
        info_list = []
        logging.debug("making info_list.pkl...")
        for subfolder in os.listdir(dirdata):
            if os.path.isdir(os.path.join(dirdata, subfolder)) == 0:
                continue
            result_path = os.path.join(dirdata, subfolder, 'result.txt')
            info_list = info_list + extract_info_from_txt(result_path)
        with open(info_list_pkl_path, 'wb') as fw:
            pickle.dump(info_list, fw)
            logging.debug("info_list.pkl saved.")

    # 生成检测框中心点的热力图 center.pkl
    center_pkl_path = os.path.join(dirpkl, 'center.pkl')
    if os.path.exists(center_pkl_path):
        logging.debug("opening center.pkl of " + str(ob_list) + "...")
        with open(center_pkl_path, 'rb') as fr:
            center = pickle.load(fr)
            logging.debug("center.pkl loaded.")
    else:
        logging.debug("making center.pkl...")
        center = cent_heap(info_list, ob_list)
        with open(center_pkl_path, 'wb') as fw:
            pickle.dump(center, fw)
            logging.debug("center.pkl saved.")

    # 生成检测框覆盖范围的热力图 cover.pkl
    cover_pkl_path = os.path.join(dirpkl, 'cover.pkl')
    if os.path.exists(cover_pkl_path):
        logging.debug("opening cover.pkl of " + str(ob_list) + "...")
        with open(cover_pkl_path, 'rb') as fr:
            cover = pickle.load(fr)
            logging.debug("cover.pkl loaded.")
    else:
        logging.debug("making cover.pkl...")
        cover = cover_heap(info_list, ob_list)
        with open(cover_pkl_path, 'wb') as fw:
            pickle.dump(cover, fw)
        logging.debug("cover.pkl saved.")

    # 生成按照九宫格的统计信息 palace_dict.pkl
    palace_dict_pkl_path = os.path.join(dirpkl, 'palace_dict.pkl')
    if os.path.exists(palace_dict_pkl_path):
        logging.debug("opening palace_dict.pkl of " + str(ob_list) + "...")
        with open(palace_dict_pkl_path, 'rb') as fr:
            palace_dict = pickle.load(fr)
            logging.debug("palace_dict.pkl loaded.")
    else:
        logging.debug("making palace_dict.pkl...")
        palace_dict = palace_partition(info_list, ob_list)
        with open(palace_dict_pkl_path, 'wb') as fw:
            pickle.dump(palace_dict, fw)
            logging.debug("palace_dict.pkl saved.")

    # 生成按照障碍物类别的统计信息 obstacle_dict.pkl
    obstacle_dict_pkl_path = os.path.join(data_root, 'obstacle_dict.pkl')
    if os.path.exists(obstacle_dict_pkl_path):
        logging.debug("opening obstacle_dict.pkl of " + str(ob_list) + "...")
        with open(obstacle_dict_pkl_path, 'rb') as fr:
            # obstacle_dict = pickle.load(fr)
            logging.debug("obstacle_dict.pkl loaded.")
    else:
        logging.debug("making obstacle_dict.pkl...")
        obstacle_dict = obstacle_partition(info_list)
        with open(obstacle_dict_pkl_path, 'wb') as fw:
            pickle.dump(obstacle_dict, fw)
            logging.debug("obstacle_dict.pkl saved.")

    logging.debug("done!")

if __name__ == '__main__':
    # 数据目录
    data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703'
    dirdata = os.path.join(data_root, 'data')
    ob_str = sys.argv[1]  # e.g. 'car' or 'all'
    # 运行主程序
    main(ob_str)



