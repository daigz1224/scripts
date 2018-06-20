# 计算灰度图像的亮度
from PIL import Image, ImageStat
import os
import pickle

dirpath = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_night_10_minutes"
dirname = dirpath.split('/')[-1]
output = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files" + '/' + dirname + '.pkl'
time = sorted(os.listdir(dirpath))  # [0,1,2,3..,9]
print(time)

bris_all = []

for index in time:
    print('time_index = ' + index)
    jpgs = os.listdir(dirpath+'/'+index)
    jpgs_index = list(range(1, len(jpgs) + 1, 1))

    bris = []
    for jpg in jpgs:
        path = dirpath + '/' + index + '/' + jpg
        im = Image.open(path)
        stat = ImageStat.Stat(im)
        bri = stat.sum[0] / stat.count[0]
        bris.append(bri)
    print('len(bris) = ' + str(len(bris)))
    bris_all.append(bris)

print('output: ' + output)

with open(output, 'wb') as f:
    pickle.dump(bris_all, f)
print('end.')