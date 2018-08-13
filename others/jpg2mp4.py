# coding: utf-8
import glob as gb
import cv2

img_path = gb.glob("/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/_unused/result/MKZ063_35/calibrator_result_10/*.jpg")
img_path.sort()
# img_size = (1920, 1080)
img_size = (2304, 1296)
fps = 20

videoWriter = cv2.VideoWriter('test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, img_size)

for path in img_path:
    img  = cv2.imread(path) 
    img = cv2.resize(img, img_size)
    videoWriter.write(img)

# generate test.mp4 in current folder
