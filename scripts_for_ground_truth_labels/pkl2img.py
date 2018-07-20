# coding: utf-8
import os
import sys
import logging
import random
import json
import pickle
import cv2

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

# 检测框的颜色仓库
box_colors = [(random.randint(0, 255),
               random.randint(0, 255),
               random.randint(0, 255)) for ob in range(20)]

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

def outlier(info_list, ob_list, dirimg, target):
    """
    读取info_list.pkl文件，根据判定条件将异常检测框的图片保存下来
    :param info_list:
    :param ob_list:
    :param target:
    :param dirimg:
    :return:
    """
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
                    dirsave = os.path.join(dirimg, 'range_out')
                    save_img_with_bb(video_name, frame_id, res, dirsave)
                    count = count + 1
            elif target == 'ratio':
                if h/w > 10 or w/h > 10:
                    dirsave = os.path.join(dirimg, 'ratio_10')
                    save_img_with_bb(video_name, frame_id, res, dirsave)
                    count = count + 1
            else:
                logging.error("No target.")
    logging.info("outlier of " + target + " count: " + str(count))

def sample(info_list, ob_list, dirimg, sample_num=10):
    """
    随机获取一些包含在ob_list的图片
    :param info_list:
    :param ob_list:
    :param dirimg:
    :param sample_num:
    :return:
    """
    count = 0
    while count < sample_num:
        seed = random.randint(0, len(info_list)-1)
        info = info_list[seed]
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
            dirsave = os.path.join(dirimg, 'sample')
            save_img_with_bb(video_name, frame_id, res, dirsave)
            count = count + 1

def main(ob, target):
    """
    主程序
    :param ob:
    :param target:
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
    dirimg = os.path.join(dirres, 'data_img')

    if os.path.exists(dirimg):
        logging.debug(dirimg + "alreadly exists.")
    else:
        os.mkdir(dirimg)
        logging.debug("making folder: " + dirimg)

    info_list_pkl_path = os.path.join(data_root, 'info_list.pkl')
    if os.path.exists(info_list_pkl_path):
        logging.debug("opening info_list.pkl of ...")
        with open(info_list_pkl_path, 'rb') as fr:
            info_list = pickle.load(fr)
            logging.debug("info_list.pkl loaded.")
    else:
        info_list = []
        logging.error("info_list.pkl not found.")

    if target == 'outlier':
        outlier(info_list, ob_list, dirimg, 'range')
        outlier(info_list, ob_list, dirimg, 'ratio')
    elif target == 'sample':
        sample(info_list, ob_list, dirimg, sample_num=10)
    else:
        logging.error("no target like 'outlier' or 'sample'.")

if __name__ == '__main__':
    # 数据目录
    data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703'
    dirdata = os.path.join(data_root, 'data')
    ob_str = sys.argv[1]
    target_str = sys.argv[2]
    # 运行主程序
    main(ob_str, target_str)
