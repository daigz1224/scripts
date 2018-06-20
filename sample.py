# sample.py
import os
import random
import shutil

dirpath = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_night_5_minutes'
dirname = dirpath.split('/')[-1]
output = dirpath + '_sample'

if os.path.exists(output) == 0:
    os.mkdir(output)

nums = 10

for index in os.listdir(dirpath):
    if os.path.exists(output + '/' + index) == 0:
        os.mkdir(output + '/' + index)

    jpgs = os.listdir(dirpath + '/' + index)
    sample = random.sample(jpgs, nums)
    for jpg in sample:
        src = dirpath + '/' + index + '/' + jpg
        dst = output + '/' + index + '/' + jpg
        shutil.copyfile(src, dst)
print('end.')