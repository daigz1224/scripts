# coding: utf-8
import os
import json

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


def result2xml(feilds):
    name = ".".join(fields[2].split("/")[-1].split(".")[:-1]) # name: ARZ034_3_1494827276_1494827345_120
    xml_path = os.path.join(xml_dir, name + ".xml")
    jsonstr = fields[3]
    decodejson = json.loads(jsonstr)
    result_class = ImageResult(**decodejson)


    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'mark_task_511-20170515_ShangDi_ARZ034-2D_OBSTACLE_NO_GROUND_POINT')
    node_folder.text = 'GTSDB'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = '000001.jpg'

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '500'

    node_height = SubElement(node_size, 'height')
    node_height.text = '375'

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'

    node_object = SubElement(node_root, 'object')
    node_name = SubElement(node_object, 'name')
    node_name.text = 'mouse'
    node_difficult = SubElement(node_object, 'difficult')
    node_difficult.text = '0'
    node_bndbox = SubElement(node_object, 'bndbox')
    node_xmin = SubElement(node_bndbox, 'xmin')
    node_xmin.text = '99'
    node_ymin = SubElement(node_bndbox, 'ymin')
    node_ymin.text = '358'
    node_xmax = SubElement(node_bndbox, 'xmax')
    node_xmax.text = '135'
    node_ymax = SubElement(node_bndbox, 'ymax')
    node_ymax.text = '375'

    xml = tostring(node_root, pretty_print=True)  # 格式化显示，该换行的换行
    dom = parseString(xml)
    print(xml)
    return xml


def main(result_path, xml_dir):

    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    with open(result_path, 'r') as fp:
        v_labels = [line.split() for line in fp if is_results_line(line)]

    for i, fields in enumerate(v_labels):  
        xml = result2xml(fields)
        with open(xml_path, 'w') as fp:
            fp.write(xml)
            print(name+'.xml'+' done.')


if __name__ == '__main__':
    data_root = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/mark_task_511-20170515_ShangDi_ARZ034-2D_OBSTACLE_NO_GROUND_POINT/'
    result_path = data_root + 'result.txt'
    xml_dir = data_root + 'xml'
    main(result_path, xml_dir)
