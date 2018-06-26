# Author: daiguozheng
# 用法: python3 cal_brightness.py
# 说明：计算每个目录下的所有灰度图像的亮度，并 pickle.dump 保存到当前目录
# 前提：需要按时间序列整理好的图片目录

import os
import pickle
from PIL import Image, ImageStat


def main(dirpath):
    dirname = dirpath.split('/')[-1]
    output = dirname + ".pkl"
    # time = sorted(list(map(int, os.listdir(dirpath))))  # [0,1,2,3..,9]
    time = sorted(os.listdir(dirpath))
    print("time list: ")  # [00000, 00001,...]
    print(time)

    bris_all = []
    for index in time:
        print('time index = ' + index)
        jpgs = os.listdir(dirpath + '/' + index)
        # jpgs_index = list(range(1, len(jpgs) + 1, 1))

        bris = []
        for jpg in jpgs:
            jpg_path = dirpath + '/' + index + '/' + jpg
            im = Image.open(jpg_path)
            stat = ImageStat.Stat(im)
            bri = stat.sum[0] / stat.count[0]
            bris.append(bri)
        print('len(bris) = ' + str(len(bris)))

        bris_all.append(bris)

    print('output: ' + output)
    with open(output, 'wb') as f:
        pickle.dump(bris_all, f)
    print('End.')

if __name__ == '__main__':
    dirpath = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_night_10_minutes"
    main(dirpath)