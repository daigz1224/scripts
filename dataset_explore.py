#!/usr/bin/env python
# coding: utf-8
import os
import argparse
import logging
import json
from common import LABEL_MAP
DESCRIPTION = """
"""
IMAGE_W = 1920
IMAGE_H = 1080
def runcmd(cmd):
    """ Run command.
    """
    logging.info("%s" % cmd)
    os.system(cmd)
def getargs():
    """ Parse program arguments.
    """
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('raw_label', type=str, help='result.txt')
    parser.add_argument('label_dir', type=str, help='dir to save labels')
    parser.add_argument('--ground', action='store_true', help='save ground points')
    parser.add_argument("--log", type=str, default="INFO", help="log level")
    return parser.parse_args()
def is_results_line(line):
    fields = line.split()
    return len(fields) == 5 and fields[0].endswith(".bag")
class ImageResult:
    def __init__(self, result, *args, **kwargs):
        self.result = result
def main(args):
    """ Main entry.
    """
    # print args
    if not os.path.exists(args.label_dir):
        os.makedirs(args.label_dir)
    with open(args.raw_label, 'r') as fp:
        v_labels = [line.split() for line in fp if is_results_line(line)]
    for i, fields in enumerate(v_labels):
        if i % 1000 == 0:
            logging.info("{}/{}".format(i, len(v_labels)))
        name = ".".join(fields[2].split("/")[-1].split(".")[:-1])
        label_path = os.path.join(args.label_dir, name + ".txt")
        jsonstr = fields[3]
        decodejson = json.loads(jsonstr)
        result_class = ImageResult(**decodejson)
        with open(label_path, 'w') as fp:
            for result_object in result_class.result:
                x = float(result_object["x"])
                y = float(result_object["y"])
                w = float(result_object["w"])
                h = float(result_object["h"])
                x1, y1, x2, y2 = x, y, x + w, y + h
                fp.write("{} 0 0 0 {} {} {} {} 0 0 0 0 0 0 0 1.0\n".format(
                    LABEL_MAP[int(result_object["tag"])], x1, y1, x2, y2))
    logging.info("{}/{}".format(len(v_labels), len(v_labels)))
if __name__ == '__main__':
    args = getargs()
    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: " + args.log)
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=numeric_level)
    main(args)