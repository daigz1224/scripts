# 计算灰度图像的亮度
from PIL import Image, ImageStat
import os
import matplotlib.pyplot as plt

dirname = "/Users/daiguozheng/Downloads/export_image/0605_nigit_rain/"
jpgs = os.listdir(dirname)
index = list(range(1, len(jpgs) + 1, 1))
bris = []
for jpg in jpgs:
    path = dirname + jpg
    im = Image.open(path)
    stat = ImageStat.Stat(im)
    bri = stat.sum[0] / stat.count[0]
    bris.append(bri)
plt.figure()
plt.plot(index, bris)