# !/home/dai/anaconda3/bin python3
# coding: utf-8
import os
import json
import matplotlib.pyplot as plt


IMAGE_W = 1920
IMAGE_H = 1080

class ImageResult:
    def __init__(self, result, *args, **kwargs):
        self.result = result

def is_results_line(line):
    fields = line.split()
    return len(fields) == 5 and fields[0].endswith(".bag")


def main():
    result_path = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/mark_task_511-20170515_ShangDi_ARZ034-2D_OBSTACLE_NO_GROUND_POINT/result.txt'
    with open(result_path, 'r') as fp:
        v_labels = [line.split() for line in fp if is_results_line(line)]
    img_n = 0
    tag_n = 0
    tag_list = []
    for i, fields in enumerate(v_labels):
        name = ".".join(fields[2].split("/")[-1].split(".")[:-1])
        # name: ARZ034_3_1494827276_1494827345/ARZ034_3_1494827276_1494827345_120
        jsonstr = fields[3]
        decodejson = json.loads(jsonstr)
        result_class = ImageResult(**decodejson)
        img_n = img_n + 1
        for result_object in result_class.result:
            '''
            result_object:
            {'isauto': 0,
            'trackingId': 31749,
            'h': 27.84446756105,
            'isoccluded': 1,
            'tag': 1,
            'w': 33.242023008147,
            'y': 415.55574496251,
            'x': 990.29248756641,
            'ground_points': [],
            'istruncated': 0}
            '''
            if 'tag' not in result_object:
                print('No tag!!!!')
            tag_n = tag_n + 1
            tag_list.append(int(result_object['tag']))
            print(result_object['isauto'])
            # print(result_object['tag'])
    print("img_n = %d\n", img_n)
    print("tag_n = %d\n", tag_n)
    tag_dict = {}
    for tag in set(tag_list):
        tag_dict[tag] = tag_list.count(tag)
    print("tag_dict: \n")
    print(tag_dict)
    # lists = sorted(tag_dict.items())
    # x, y = zip(*lists)
    # plt.bar(x, y)
    # plt.show()
if __name__ == '__main__':
    main()