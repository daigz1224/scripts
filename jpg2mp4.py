# coding: utf-8
import glob as gb
import cv2

img_path = gb.glob("/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/for_liumingjian/calibrator_result/*.jpg")
img_path.sort()
# img_size = (1920, 1080)
img_size = (2304, 1296)
fps = 20

videoWriter = cv2.VideoWriter('calibrator_result.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, img_size)

for path in img_path:
    img  = cv2.imread(path) 
    img = cv2.resize(img, img_size)
    videoWriter.write(img)

# generate test.mp4 in current folder
