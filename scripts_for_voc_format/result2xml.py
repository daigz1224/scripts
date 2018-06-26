# coding: utf-8
import os
import json
from common import LABEL_MAP

from lxml.etree import Element, SubElement, tostring
import pprint
from xml.dom.minidom import parseString

IMAGE_W = 1920
IMAGE_H = 1080


class ImageResult:
    def __init__(self, result, *args, **kwargs):
        self.result = result


def is_results_line(line):
    fields = line.split()
    return len(fields) == 5 and fields[0].endswith(".bag")


def result2xml(fields, output):
    jpg_name = ".".join(fields[2].split("/")[-1].split(".")[:-1]) # name: ARZ034_3_1494827276_1494827345_120
    xml_path = os.path.join(output, jpg_name + ".xml")

    jsonstr = fields[3]
    decodejson = json.loads(jsonstr)
    result_class = ImageResult(**decodejson)

    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'mark_task_511-20170515_ShangDi_ARZ034-2D_OBSTACLE_NO_GROUND_POINT'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = jpg_name + '.jpg'

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(IMAGE_W)

    node_height = SubElement(node_size, 'height')
    node_height.text = str(IMAGE_H)

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'

    for result_object in result_class.result:
        name = LABEL_MAP[int(result_object["tag"])]
        x = float(result_object["x"])
        y = float(result_object["y"])
        w = float(result_object["w"])
        h = float(result_object["h"])
        x1, y1, x2, y2 = x, y, x + w, y + h

        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = name
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(x1)
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(y1)
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(x2)
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(y2)

    xml = tostring(node_root, pretty_print=True)  # 格式化显示，该换行的换行
    # dom = parseString(xml)
    with open(xml_path, 'w') as fp:
        fp.write(xml)
        print(jpg_name+'.xml' + ' done.')


def main(result_path, output):
    if not os.path.exists(output):
        os.makedirs(output)

    with open(result_path, 'r') as fp:
        v_labels = [line.split() for line in fp if is_results_line(line)]

    for i, fields in enumerate(v_labels):  
        result2xml(fields, output)
        


if __name__ == '__main__':
    data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/mark_task_511-20170515_ShangDi_ARZ034-2D_OBSTACLE_NO_GROUND_POINT/'
    result_path = data_root + 'result.txt'
    output = data_root + 'xml'
    print("data_root: " + data_root)
    print("output: " + output)
    main(result_path, output)
