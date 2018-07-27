# encoding: UTF-8

import os

img_path = "0606_rain"

i = 1

jpg_list = os.listdir(img_path)

jpg_list.sort()

for item in jpg_list:
    index = "%05d" % i
    os.rename(os.path.join(img_path, item), os.path.join(img_path, index+'.jpg'))
    i = i + 1
print('done!')