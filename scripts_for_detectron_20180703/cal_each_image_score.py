import os
import pickle
import numpy as np

# INPUT:
detections_path    = "/home/dai/Documents/GitHub/detectron/test/20180703_coco_all/generalized_rcnn/" \
                     "bbox_20180703_coco_all_results"
groundtruths_path  = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/annotations/" \
                     "instances_all"
total_num_images   = 281620
iou_thresh = 0.5
FP_high_confidence_thresh = 0.8
FN_ratio_thresh = 10.0
confidence_thresh = 0.5

# OUTPUT:
scores_pkl_path    = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                     "scores.pkl"

def fill_all_image_id():
    """
    补全 txt 的 label
    :return:
    """
    for i in range(total_num_images):
        ii = "%06d" % i
        gt_txt_path = os.path.join(groundtruths_path, ii + '.txt')
        if not os.path.exists(gt_txt_path):
            print('LOG: touch ' + ii + '.txt in ' + groundtruths_path)
            with open(gt_txt_path, 'w'):
                pass
        det_txt_path = os.path.join(detections_path, ii + '.txt')
        if not os.path.exists(det_txt_path):
            print('LOG: touch ' + ii + '.txt in ' + detections_path)
            with open(det_txt_path, 'w'):
                pass

def eval_image_score(det_list, gt_list):
    """
    根据 det_bbox 和 gt_bbox 收集信息
    :param det_list:
    :param gt_list:
    :return:
    """

    det_list_valid = []
    for det in det_list:
        if float(det[5]) - confidence_thresh > 0:
            det_list_valid.append(det)

    # print(det_list_valid)
    det_mat = np.array(det_list_valid, dtype=np.float)
    gt_mat = np.array(gt_list, dtype=np.float)

    # print("det_mat: ")
    # print(det_mat)
    # print("gt_mat: ")
    # print(gt_mat)
    # det_mat = det_mat_orginal[ det_mat_orginal[:,5]>confidence_thresh ]

    score = dict()
    score['total_det'] = det_mat.shape[0]
    score['total_gt'] = gt_mat.shape[0]
    score['TP'] = 0
    score['FP'] = 0
    score['FN'] = 0
    score['precision'] = 0
    score['recall'] = 0
    score['iou'] = []
    score['FP_high'] = []
    score['FN_ratio'] = []
    score['det_none'] = False
    score['gt_none'] = False

    if det_mat.shape[0] == 0 and gt_mat.shape[0] == 0:
        score['det_none'] = True
        score['gt_none'] = True
        return score

    if det_mat.shape[0] == 0 and gt_mat.shape[0] > 0:
        score['det_none'] = True
        score['FN'] = gt_mat.shape[0]
        return score

    if gt_mat.shape[0] == 0 and det_mat.shape[0] > 0:
        score['gt_none'] = True
        # 继续计算FP和iou_FP_high
        score['FP'] = det_mat.shape[0]
        for i in range(det_mat.shape[0]):
            confidence = det_mat[i, 5]
            if confidence > 0.9:
                score['FP_high'].append(confidence)
        return score


    # 按照置信度降序排序
    det_mat = det_mat[det_mat[:, -1].argsort()][::-1]

    gt_index_cache = []

    for i in range(det_mat.shape[0]):
        category_id = int(det_mat[i, 0])
        bbox = det_mat[i, 1:5]
        confidence = det_mat[i, 5]

        ixmin = np.maximum(gt_mat[:, 1], bbox[0])
        iymin = np.maximum(gt_mat[:, 2], bbox[1])
        ixmax = np.minimum(gt_mat[:, 1] + gt_mat[:, 3], bbox[0] + bbox[2])
        iymax = np.minimum(gt_mat[:, 2] + gt_mat[:, 4], bbox[1] + bbox[3])

        iw = np.maximum(ixmax - ixmin + 1., 0.)
        ih = np.maximum(iymax - iymin + 1., 0.)
        inters = iw * ih
        union = ((bbox[2] + 1. ) * (bbox[3] + 1.) +
                 (gt_mat[:, 3] + 1.) * (gt_mat[:, 4] + 1.) - inters)
        iou = inters / union
        ioumax = np.max(iou)
        gt_index = np.argmax(iou)

        if gt_index not in gt_index_cache:
            gt_index_cache.append(gt_index)
            if ioumax > iou_thresh:
                # 认为该det_bbox与gt_bbox是为了同一个物体
                # 不考虑标签
                score['TP'] += 1
                score['iou'].append(ioumax)
                # 考虑标签
                # if int(gt_mat[gt_index, 0]) - category_id == 0:
                #     score['TP'] += 1
                #     score['iou'].append(ioumax)
                # else:
                #     score['FP'] += 1
                #     if confidence > FP_high_confidence_thresh:
                #         score['FP_high'].append(confidence)
            else:
                # 与gt重叠较少，但是置信度很高，怀疑gt框不准
                score['FP'] += 1
                if confidence > FP_high_confidence_thresh:
                    score['FP_high'].append(confidence)
        else:
            # 匹配的gt已经有检测框匹配了，与gt重叠较少，但是置信度很高，怀疑有漏标的gt
            if ioumax < 0.001:
                if confidence > FP_high_confidence_thresh:
                    score['FP_high'].append(confidence)
            continue

    for i in range(gt_mat.shape[0]):
        if i in gt_index_cache:
            continue
        w = gt_mat[i,3]
        h = gt_mat[i,4]
        r1 = h / w
        r2 = w / h
        if r1 >= FN_ratio_thresh or r2 >= FN_ratio_thresh:
            r = r1 if r1 > r2 else r2
            score['FN_ratio'].append(r)

    score['FN'] = gt_mat.shape[0] - score['TP']

    score['precision'] = score['TP'] / (score['TP'] + score['FP'])
    score['recall'] = score['TP'] / (score['TP'] + score['FN'])
    # print(score)
    return score

def main(is_test):

    if len(os.listdir(groundtruths_path)) < total_num_images or \
            len(os.listdir(detections_path)) < total_num_images:
        print("LOG: fill_all_image_id()")
        fill_all_image_id()

    scores = dict()

    for i in range(total_num_images):
        ii = "%06d" % i
        scores[ii] = []

        detection_txt_path = os.path.join(detections_path, ii+'.txt')
        groundtruth_txt_path = os.path.join(groundtruths_path, ii+'.txt')

        detection_list = []
        with open(detection_txt_path, 'r') as f:
            det_lines = [l.strip('\n') for l in f.readlines()]
            for l in det_lines:
                detection_list.append(l.split(' '))
        groundtruth_list = []
        with open(groundtruth_txt_path, 'r') as f:
            gt_lines = [l.strip('\n') for l in f.readlines()]
            for l in gt_lines:
                groundtruth_list.append(l.split(' '))

        s = eval_image_score(detection_list, groundtruth_list)
        s['image_id'] = ii
        if i % 20000 == 0:
            print("LOG: Processing image_id:" + ii)
            print(s)

        scores[ii] = s

        if is_test:
            print("LOG: Just testing.")
            exit()

    with open(scores_pkl_path, 'wb') as fw:
        pickle.dump(scores, fw)
        print("LOG: Save scores to " + scores_pkl_path)

if __name__ == "__main__":
    main(False)
    print("DONE.")
