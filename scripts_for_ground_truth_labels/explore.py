# coding: utf-8
import os
import logging
import json
import pickle
import random
import numpy as np
import cv2

import matplotlib
matplotlib.use('Agg')  # plt.show() or not

import matplotlib.pyplot as plt
import fire


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

# 重要！指定特定的障碍物
# ob_list = ['car']
# ob_list = ['pedestrian']
# ob_list = ['cyclist']
# ob_list = ['van']
# ob_list = ['truck']
# ob_list = ['motorcyclist']
# ob_list = ['trafficcone']
# ob_list = ['tricyclelist']
# ob_list = ['noidea1']
ob_list = ['noidea2']
# ob_list = [LABEL_MAP[key] for key in LABEL_MAP]

# 数据、输出的根目录
data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703'
pkl_flag = 0  # 0：重新提取 1：从pkl中读取

if len(ob_list) == 1:
    suffix = ob_list[0]
else:
    suffix = 'all'

dirres = os.path.join(data_root+'/result_'+suffix)

if os.path.exists(dirres) == 0:
    os.mkdir(dirres)

dirdata  = os.path.join(data_root, 'data')
dirpkl   = os.path.join(data_root, dirres, 'data_pkl')
dirplt   = os.path.join(data_root, dirres, 'data_plt')
log_path = os.path.join(data_root, dirres, 'result_explore.log')

info_list_pkl   = pkl_flag    # 是否通过读取data_pkl中文件得到info_list
center_pkl      = pkl_flag    # 是否通过读取data_pkl中文件得到center
cover_pkl       = pkl_flag    # 是否通过读取data_pkl中文件得到cover
palace_dict_pkl = pkl_flag    # 是否通过读取data_pkl中文件得到palace_dict

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
                    # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    # datefmt='%a, %d %b %Y %H:%M:%S',
                    # filename=log_path,
                    # filemode='w'
myfigsize = (20,15)
mydpi = 72

IMAGE_W = 1920
IMAGE_H = 1080

# 检测框的颜色仓库
box_colors = [(random.randint(0, 255),
               random.randint(0, 255),
               random.randint(0, 255)) for ob in range(20)]

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

def count_obstacles(info_list):
    """
    统计每种障碍物的数量
    :param info_list:
    :return: count
    """
    count = {}
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
            # logging.debug(res)
            ob = LABEL_MAP[res['tag']]
            if ob not in count:
                count[ob] = 0
            count[ob] = count[ob] + 1
    return count

def cent_heap(info_list):
    """
    返回检测框中心位置的热力图
    :param info_list:
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
    logging.debug("total = " + str(total))
    logging.debug("valid = " + str(valid))
    return center

def cover_heap(info_list):
    """
    返回检测框覆盖范围的热力图
    :param info_list:
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

def save_img_with_bb(video_name, frame_id, res, dirsave):
    """
    将异常检测框在图上标注并保存下来查看
    :param video_name:
    :param frame_id:
    :param res: 'tag','x','y','h','w'...
    :param dirsave:
    :return:
    """
    # if os.path.exists(dirsave):
    #     shutil.move(dirsave, dirsave+'_tmp')

    if os.path.exists(dirsave) == 0:
        os.mkdir(dirsave)
    # find target jpg path
    jpg_name = video_name.split('.')[0] + '_' + str(frame_id)
    target_path = ''
    for mark_task in os.listdir(dirdata):
        if os.path.isdir(os.path.join(dirdata, mark_task)) == 0:
            continue
        images_path = os.path.join(dirdata, mark_task, 'images')
        for vn in os.listdir(images_path):
            if vn == video_name.split('.')[0]:
                jpgs_path = os.path.join(images_path, vn)
                for jpg in os.listdir(jpgs_path):
                    if jpg.split('.')[0] == jpg_name:
                        target_path = os.path.join(jpgs_path, jpg)
                        break
    if target_path:
        im = cv2.imread(target_path)
        # im_height, im_width, im_channels = im.shape
        ob = LABEL_MAP[res['tag']]
        x_min = res['x']
        y_min = res['y']
        h = res['h']
        w = res['w']
        x_max = x_min + w
        y_max = y_min + h
        box_color = box_colors[res['tag'] - 1]

        # e.g. cv2.rectangle(img, (x,y), (x+w,y+h), (B,G,R), Thickness)
        cv2.rectangle(im, (int(x_min), int(y_min)), (int(x_max), int(y_max)), box_color, 2)

        # e.g. cv2.putText(img, text, (x,y), Font, Size, (B,G,R), Thickness)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(im, ob, (int(x_min), int(y_min)), font, 0.5, (255, 255, 0), 1)
        cv2.imwrite(os.path.join(dirsave, jpg_name + '_with_bb.jpg'), im)
        # plt.figure(figsize=myfigsize, dpi=mydpi)
        # plt.imshow(im)
    else:
        logging.error("Error: " + jpg_name + " not found.")

def palace_partition(info_list):
    """
    划分九宫格，将中心点位于对应宫格内的检测框存到对应字典中
    :param info_list:
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

def plot_palace(palace_dict, target):
    """
    绘制九宫格分析图，以及全数据分析图
    :param palace_dict:
    :param target:
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
    plt.savefig(os.path.join(dirplt, 'palace_' + target + '.jpg'))
    plt.show()
    logging.debug('palace_' + target + '.jpg saved.')

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
            h = res['h']
            w = res['w']
            obstacle_dict[ob].append([video_name, frame_id, res])

    logging.debug("Done.")

    return obstacle_dict

def plot_obstacle(obstacle_dict, ob_list):
    for ob in ob_list:
        obstacle_ratio = [info[2]['h'] / info[2]['w'] for info in obstacle_dict[ob]]
        obstacle_height = [info[2]['h'] for info in obstacle_dict[ob]]
        obstacle_width = [info[2]['w'] for info in obstacle_dict[ob]]

        obstacle_ratio_np = np.array(obstacle_ratio)
        obstacle_height_np = np.array(obstacle_height)
        obstacle_width_np = np.array(obstacle_width)

        plt.figure(figsize=myfigsize, dpi=mydpi)
        n_bin = 200

        plt.subplot(3, 1, 1)
        plt.title(str(ob_list) + ' ratio range in ' + str(round(obstacle_ratio_np.min(), 2)) +
                  '~' + str(round(obstacle_ratio_np.max(), 2)))
        # upper_r = 6
        upper_r = round(obstacle_ratio_np.max(), 2) / 2
        gap_r = upper_r / n_bin
        bins = list(np.arange(0, upper_r, gap_r))
        plt.hist(obstacle_ratio_np, bins)

        plt.subplot(3, 1, 2)
        plt.title(str(ob_list) + ' height range in ' + str(round(obstacle_height_np.min(), 2)) +
                  '~' + str(round(obstacle_height_np.max(), 2)))
        # upper_h = 400
        upper_h = round(obstacle_height_np.max(), 2) / 2
        gap_h = upper_h / n_bin
        bins = list(np.arange(0, upper_h, gap_h))
        plt.hist(obstacle_height_np, bins)

        plt.subplot(3, 1, 3)
        plt.title(str(ob_list) + ' width range in ' + str(round(obstacle_width_np.min(), 2)) +
                  '~' + str(round(obstacle_width_np.max(), 2)))
        # upper_w = 250
        upper_w = round(obstacle_width_np.max(), 2) / 2
        gap_w = upper_w / n_bin
        bins = list(np.arange(0, upper_h, gap_w))
        plt.hist(obstacle_width_np, bins)


class Explore(object):

    @staticmethod
    def main():
        """
        主程序，从pkl文件读取数据 或 通过result.txt文件重新制作pkl文件
        :return:
        """
        logging.debug("Start explore " + str(ob_list) + "...")

        if os.path.exists(dirplt) == 0:
            os.mkdir(dirplt)
        if os.path.exists(dirpkl) == 0:
            os.mkdir(dirpkl)

        if info_list_pkl == 1:
            logging.debug("opening info_list.pkl of " + str(ob_list) + "...")
            with open(os.path.join(dirpkl, 'info_list.pkl'), 'rb') as fr:
                info_list = pickle.load(fr)
        else:
            info_list = []
            for subfolder in os.listdir(dirdata):
                if os.path.isdir(os.path.join(dirdata, subfolder)) == 0:
                    continue
                # logging.debug("Processing the subfolder of: " + subfolder)
                result_path = os.path.join(dirdata, subfolder, 'result.txt')
                info_list = info_list + extract_info_from_txt(result_path)
            with open(os.path.join(dirpkl, 'info_list.pkl'), 'wb') as fw:
                pickle.dump(info_list, fw)
                logging.debug("info_list.pkl saved.")

        # 统计每种障碍物出现的频次
        count = count_obstacles(info_list)
        for ob in count.keys():
            logging.info(ob + ': ' + str(count[ob]))
            # print(ob + ': ' + str(count[ob]))

        # 绘制检测框中心点的热力图
        if center_pkl == 1:
            logging.debug("opening center.pkl of " + str(ob_list) + "...")
            with open(os.path.join(dirpkl, 'center.pkl'), 'rb') as fr:
                center = pickle.load(fr)
        else:
            logging.debug("making center.pkl...")
            center = cent_heap(info_list)
            with open(os.path.join(dirpkl, 'center.pkl'), 'wb') as fw:
                pickle.dump(center, fw)
                logging.debug("center.pkl saved.")

        # center_min, center_max = center.min(), center.max()
        # center_norm = (center - center_min) / (center_max - center_min)
        # center_255 = center_norm * 255

        plt.figure(figsize=myfigsize, dpi=mydpi)
        plt.title('center point of ' + str(ob_list))
        plt.imshow(center)
        # plt.colorbar()
        plt.savefig(os.path.join(dirplt, 'center_point_heap.jpg'))
        plt.show()

        # 绘制检测框覆盖范围的热力图
        if cover_pkl == 1:
            logging.debug("opening cover.pkl of " + str(ob_list) + "...")
            with open(os.path.join(dirpkl, 'cover.pkl'), 'rb') as fr:
                cover = pickle.load(fr)
        else:
            logging.debug("making cover.pkl...")
            cover = cover_heap(info_list)
            with open(os.path.join(dirpkl, 'cover.pkl'), 'wb') as fw:
                pickle.dump(cover, fw)
                logging.debug("cover.pkl saved.")

        # cover_min, cover_max = cover.min(), cover.max()
        # cover_norm = (cover - cover_min) / (cover_max - cover_min)
        # cover_255 = cover_norm * 255

        plt.figure(figsize=myfigsize, dpi=mydpi)
        plt.title('cover area of ' + str(ob_list))
        plt.imshow(cover)
        # plt.colorbar()
        plt.savefig(os.path.join(dirplt, 'cover_area_heap.jpg'))
        plt.show()

        # 按照九宫格存储重要信息
        if palace_dict_pkl == 1:
            logging.debug("opening palace_dict.pkl of " + str(ob_list) + "...")
            with open(os.path.join(dirpkl, 'palace_dict.pkl'), 'rb') as fr:
                palace_dict = pickle.load(fr)
        else:
            logging.debug("making palace_dict.pkl...")
            palace_dict = palace_partition(info_list)
            with open(os.path.join(dirpkl, 'palace_dict.pkl'), 'wb') as fw:
                pickle.dump(palace_dict, fw)
                logging.debug("palace_dict.pkl saved.")

        # 绘制每个宫格的研究信息
        plot_palace(palace_dict, 'ratio')
        plot_palace(palace_dict, 'width')
        plot_palace(palace_dict, 'height')

    @staticmethod
    def outlier(target='ratio'):
        """
        读取info_list.pkl文件，根据判定条件将异常检测框的图片保存下来
        :param: target:
        :return:
        """
        logging.debug("opening info_list.pkl of " + str(ob_list) + "...")
        if os.path.exists(os.path.join(dirpkl, 'info_list.pkl')) == 0:
            logging.error("No info_list.pkl.")

        with open(os.path.join(dirpkl, 'info_list.pkl'), 'rb') as fr:
            info_list = pickle.load(fr)

        count = 0
        # 根据判断条件输出异常图片
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
                h = res['h']
                w = res['w']
                # 重要！判断outlier的条件，将异常检测框的图片保存下来
                if target == 'range':
                    if h > IMAGE_H or w > IMAGE_W:
                        dirsave = os.path.join(data_root, dirres, 'data_outlier_range')
                        save_img_with_bb(video_name, frame_id, res, dirsave)
                        count = count + 1
                elif target == 'ratio':
                    if h/w > 10 or w/h > 10:
                        dirsave = os.path.join(data_root, dirres, 'data_outlier_ratio')
                        save_img_with_bb(video_name, frame_id, res, dirsave)
                        count = count + 1
                else:
                    logging.error("No target.")
        logging.info("count: " + str(count))

    @staticmethod
    def sample(sample_num=10):
        """
        随机获取一些包含在ob_list的图片
        :param sample_num: 需要采样的数目
        :return:
        """
        logging.debug("opening info_list.pkl...")
        if os.path.exists(os.path.join(dirpkl, 'info_list.pkl')) == 0:
            logging.error("No info_list.pkl for func: main4outlier.")

        with open(os.path.join(dirpkl, 'info_list.pkl'), 'rb') as fr:
            info_list = pickle.load(fr)

        count = 0
        while count < sample_num:
            sample = random.randint(0, len(info_list)-1)
            info = info_list[sample]
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
                dirsave = os.path.join(data_root, dirres, 'sample')
                save_img_with_bb(video_name, frame_id, res, dirsave)
                count = count + 1

    @staticmethod
    def count():
        logging.debug("opening info_list.pkl of " + str(ob_list) + "...")

        if os.path.exists(os.path.join(dirpkl, 'info_list.pkl')) == 0:
            logging.error("No info_list.pkl.")

        with open(os.path.join(dirpkl, 'info_list.pkl'), 'rb') as fr:
            info_list = pickle.load(fr)

        count_occ = {}
        count_tru = {}
        count_all = {}
        for ob in [LABEL_MAP[key] for key in LABEL_MAP]:
            count_occ[ob] = 0
            count_tru[ob] = 0
            count_all[ob] = 0

        # 根据判断条件输出异常图片
        for info in info_list:
            label = json.loads(info[3])
            result = label['result']
            # video_name: MKZ078_23_1522650020_1522650320.bag
            # video_name = label['videoName']
            # frame_id: 4170
            # frame_id = label['frameId']
            # jpg_name: MKZ078_23_1522650020_1522650320_4170
            # jpg_name = video_name.split('.')[0] + '_' + str(frame_id))
            for res in result:
                ob = LABEL_MAP[res['tag']]
                count_all[ob] = count_all[ob] + 1
                if res['istruncated'] == 1:
                    count_tru[ob] = count_tru[ob] + 1
                if res['isoccluded'] > 0:
                    count_occ[ob] = count_occ[ob] + 1

        logging.info("count_all:")
        for ob in count_all:
            logging.info(str(ob) + " : " + str(count_all[ob]))
        logging.info("count_tru:")
        for ob in count_tru:
            logging.info(str(ob) + " : " + str(count_tru[ob]))
        logging.info("count_occ:")
        for ob in count_occ:
            logging.info(str(ob) + " : " + str(count_occ[ob]))


        # return count_all, count_tru, count_occ

if __name__ == '__main__':
    fire.Fire(Explore)
    logging.debug("Done.")