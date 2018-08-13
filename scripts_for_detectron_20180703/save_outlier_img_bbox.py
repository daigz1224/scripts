import os
import pickle
import cv2
import random
import numpy as np

# INPUT
scores_pkl_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                  "scores.pkl"
outlier_ids_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                   "outlier_ids.txt"
image_dir_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                 "images_all"
image_id2name_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/annotations/" \
                     "image_id2name.pkl"
detections_path    = "/home/dai/Documents/GitHub/detectron/test/20180703_coco_all/generalized_rcnn/" \
                     "bbox_20180703_coco_all_results"
groundtruths_path  = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/annotations/" \
                     "instances_all"
# OUTPUT:
output_gt_dir_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                  "outlier_gt_with_bbox"
output_det_dir_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                  "outlier_det_with_bbox"
output_dir_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                  "outlier_with_bbox_gt_none"

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
    18:    'unknown_unmovable',
    19:    'unknown_movable'
}

IMAGE_W = 1920
IMAGE_H = 1080

# 检测框的颜色仓库
box_colors = [(random.randint(0, 255),
               random.randint(0, 255),
               random.randint(0, 255)) for _ in range(20)]

confidence_thresh = 0.5

def select_outlier():
    """
    筛选异常标注数据的规则
    :return:
    """
    with open(scores_pkl_path, 'rb') as f:
        scores = pickle.load(f)

    outliers = []

    for ii in scores:
        s = scores[ii]

        # Rule 1:
        if s['det_none'] == False and s['gt_none'] == True:
            if s['total_det'] > 2:
                outliers.append(ii)

        # Rule 2:
        if s['det_none'] == True and s['gt_none'] == False:
            if s['total_gt'] > 2:
                outliers.append(ii)

        # Rule 3: FP_high
        if s['det_none'] == False and \
            s['gt_none'] == False and \
              len(s['FP_high']) / (s['total_det']) > 0.25:
            outliers.append(ii)

        # Rule 4: 异常标注框的比例
        if len(s['FN_ratio']) > 0:
            outliers.append(ii)

    outliers = list(set(outliers))
    print("LOG: len(outliers) = " + str(len(outliers)))

    return outliers

def get_img_with_bbox(img_path, label_path):
    """
    根据 bbox 在 image 上画图
    :param img_path:
    :param label_path:
    :return:
    """
    im = cv2.imread(img_path)
    # image_name = img_path.split("/")[-1]
    # image_name = image_name.split('.')[0]

    with open(label_path, 'r') as fr:
        lines = fr.readlines()

    for l in lines:
        l = l.split(' ')
        confidence = 0.0
        if len(l) == 5:
            # gt label
            category_id = int(l[0])
            x1 = float(l[1])
            y1 = float(l[2])
            w = float(l[3])
            h = float(l[4])
        elif len(l) == 6:
            # det label
            category_id = int(l[0])
            x1 = float(l[1])
            y1 = float(l[2])
            w = float(l[3])
            h = float(l[4])
            confidence = float(l[5])
            if confidence < confidence_thresh:
                continue
        else:
            print("ERROR: Wrong label in " + label_path)
            continue
        x2 = x1 + w
        y2 = y1 + h

        ob = LABEL_MAP[category_id]
        color = box_colors[category_id - 1]

        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        # print([category_id, ob, color, x1, y1, x2, y2])

        # e.g. cv2.rectangle(img, (x,y), (x+w,y+h), (B,G,R), Thickness)
        cv2.rectangle(im, (x1, y1), (x2, y2), color, 2)

        # e.g. cv2.putText(img, text, (x,y), Font, Size, (B,G,R), Thickness)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if confidence > 0.0:
            text = ob + ' ' + str(confidence)
        else:
            text = ob
        cv2.putText(im, text, (x1, y1), font, 0.8, (255, 255, 0), 1)
        # cv2.imwrite(os.path.join(output_dir, image_name + '_with_bb.jpg'), im)
    return im

def paint_one_target_image_gt_det_from_image_id(image_id=''):
    tmp_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
               "tmp_image_gt_det"

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)

    with open(image_id2name_path, 'rb') as fr:
        id2name = pickle.load(fr)
    img_name = id2name[int(image_id)]
    img_path = os.path.join(image_dir_path, img_name)
    label_gt_path = os.path.join(groundtruths_path, image_id + '.txt')
    label_det_path = os.path.join(detections_path, image_id + '.txt')
    img_gt = get_img_with_bbox(img_path, label_gt_path)
    img_det = get_img_with_bbox(img_path, label_det_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_gt, 'ground_truth_bbox', (20, 20), font, 0.8, (255, 255, 255), 2)
    cv2.putText(img_det, 'detection_bbox', (20, 20), font, 0.8, (255, 255, 255), 2)
    img_gt_det = np.vstack((img_gt, img_det))
    cv2.imwrite(os.path.join(tmp_path, img_name.split('.')[0] + '_with_gt_det_bbox.jpg'), img_gt_det)

def paint_one_target_image_gt_det_from_image_name(img_name=''):
    tmp_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
               "tmp_image_gt_det"

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)

    with open(image_id2name_path, 'rb') as fr:
        id2name = pickle.load(fr)
    image_id = ''
    for i in id2name:
        if id2name[i] == img_name:
            image_id = "%06d" % i
    print(image_id)
    print(img_name)
    img_path = os.path.join(image_dir_path, img_name)
    label_gt_path = os.path.join(groundtruths_path, image_id + '.txt')
    label_det_path = os.path.join(detections_path, image_id + '.txt')
    img_gt = get_img_with_bbox(img_path, label_gt_path)
    img_det = get_img_with_bbox(img_path, label_det_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_gt, 'ground_truth_bbox', (20, 20), font, 0.8, (255, 255, 255), 2)
    cv2.putText(img_det, 'detection_bbox', (20, 20), font, 0.8, (255, 255, 255), 2)
    img_gt_det = np.vstack((img_gt, img_det))
    cv2.imwrite(os.path.join(tmp_path, img_name.split('.')[0] + '_with_gt_det_bbox.jpg'), img_gt_det)

def main():

    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)

    with open(image_id2name_path, 'rb') as fr:
        id2name = pickle.load(fr)

    # with open(outlier_ids_path, 'r') as fr:
    #     lines = [l.strip('\n') for l in fr.readlines()]

    outliers = select_outlier()

    for ii in outliers:
        print("LOG: Processing image id " + ii + " ...")
        img_name = id2name[int(ii)]

        if not os.path.join(image_dir_path, img_name):
            print("ERROR: " + img_name + " not found")

        img_path = os.path.join(image_dir_path, img_name)
        label_gt_path = os.path.join(groundtruths_path, ii+'.txt')
        label_det_path = os.path.join(detections_path, ii+'.txt')

        img_gt = get_img_with_bbox(img_path, label_gt_path)
        img_det = get_img_with_bbox(img_path, label_det_path)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_gt, 'ground_truth_bbox', (20, 20), font, 0.8, (255, 255, 255), 2)
        cv2.putText(img_det, 'detection_bbox', (20, 20), font, 0.8, (255, 255, 255), 2)
        img_gt_det = np.vstack((img_gt, img_det))
        cv2.imwrite(os.path.join(output_dir_path, img_name.split('.')[0] + '_with_gt_det_bbox.jpg'), img_gt_det)


if __name__ == "__main__":
    # paint_one_target_image_gt_det_from_image_id('100347')
    # paint_one_target_image_gt_det_from_image_name("MKZ078_52_1522657520_1522657820_4215.jpg")

    main()