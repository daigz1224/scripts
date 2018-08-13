# Author: daiguozheng
# 用法：python3 sample.py
# 说明：在输入目录下每个子目录都随机抽取 n 张

import os
import random
import shutil


def main(dirpath, num):
    output = dirpath + '_sample'
    if os.path.exists(output) == 0:
        os.mkdir(output)

    for index in os.listdir(dirpath):

        if os.path.exists(output + '/' + index) == 0:
            os.mkdir(output + '/' + index)

        files = os.listdir(dirpath + '/' + index)
        sample = random.sample(files, num)
        for f in sample:
            src = dirpath + '/' + index + '/' + f
            dst = output + '/' + index + '/' + f
            shutil.copyfile(src, dst)
    print('End.')

if __name__ == '__main__':
    path = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_rain_1_minutes'
    n = 10
    print("dirpath: " + path)
    print("#sample = " + str(n))
    main(path, n)
