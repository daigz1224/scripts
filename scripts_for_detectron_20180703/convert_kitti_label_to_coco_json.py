import os
import json

root_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/"
kitti_label_dir = os.path.join(root_path, 'kitti_labels_33d')
coco_json_file = os.path.join(root_path, 'annotations', 'instances_all_modified.json')

IMAGE_W = 1920
IMAGE_H = 1080

# LABEL_MAP = {
#      1:    'car',
#      2:    'truck',
#      3:    'van',
#      4:    'bus',
#      5:    'pedestrian',
#      6:    'cyclist',
#      7:    'tricyclelist',
#      8:    'motorcyclist',
#     12:    'barrowlist',
#     13:    'pedestrianignore',
#     14:    'carignore',
#     15:    'othersignore',
#     16:    'trafficcone',
#     17:    'confused',
#     18:    'unknown_unmovable',
#     19:    'unknown_movable'
# }

LABEL_MAP = {
     1:    'car',
     2:    'truck',
     3:    'van',
     4:    'bus',
     5:    'pedestrian',
     6:    'cyclist',
     7:    'tricyclelist',
     8:    'motorcyclist',
     9:    'barrowlist',
    10:    'pedestrianignore',
    11:    'carignore',
    12:    'othersignore',
    13:    'trafficcone',
    14:    'confused',
    15:    'unknown_unmovable',
    16:    'unknown_movable'
}


GET_CATEGORY_ID = {value:key for key, value in LABEL_MAP.items()}

coco = dict()

coco['info'] = {'year': 2018,
                'version': '',
                'description': '',
                'contributor': 'daiguozheng',
                'url': '',
                'date_created': ''}

coco['licenses'] = [{'url': '',
                     'id': 0,
                     'name': ''}]

coco['categories'] = []

for item in GET_CATEGORY_ID:

    category = dict()

    category['id'] = GET_CATEGORY_ID[item]
    category['name'] = item
    category['supercategory'] = GET_CATEGORY_ID[item]

    coco['categories'].append(category)

coco['type'] = 'instances'

coco['images'] = []

coco['annotations'] = []

def get_all_category():
    """
    Get name of all category from txt file.
    :return:
    """
    count = 0
    categories = {}

    print("From directory: " + kitti_label_dir)

    for file in os.listdir(kitti_label_dir):
        count = count + 1

        if not file.endswith('.txt'):
            continue

        if count % 10000 == 0:
            print('LOG: proessing txt count = ' + str(count))

        with open(os.path.join(kitti_label_dir, file), 'r', errors='ignore') as fr:
            labels = fr.readlines()

        for l in labels:
            c = l.split(' ')[0]
            if count % 10000 == 0:
                print(c)
            if c not in categories:
                categories[c] = 0
            categories[c] = categories[c] + 1

    print("SUMMARY: categories = \n")
    print(categories)
    return categories


def main():
    """
    Process txt files in one directory to a json file.
    :return:
    """

    image_id = 0
    annotations_id = 0

    for file in os.listdir(kitti_label_dir):

        if not file.endswith('.txt'):
            continue

        name = file.split('.')[0]
        image_name = str(name) + '.jpg'

        if image_id % 10000 == 0:
            print("LOG: processing image_id " + str(image_id))

        # just for function test
        # if image_id == 10: break

        image_json = dict()
        image_json['height'] = IMAGE_H
        image_json['width'] = IMAGE_W
        image_json['license'] = ''
        image_json['url'] = ''
        image_json['date_captured'] = ''
        image_json['file_name'] = image_name
        image_json['id'] = image_id

        coco['images'].append(image_json)

        with open(os.path.join(kitti_label_dir, file), 'r', errors='ignore') as fr:
            labels = fr.readlines()

        for l in labels:
            label_list = l.split(' ')
            c = label_list[0]

            if c not in GET_CATEGORY_ID:
                print('ERROR: strange category ' + c + ' in ' + file)
                continue

            x1, y1, x2, y2 = float(label_list[4]), float(label_list[5]), float(label_list[6]), float(label_list[7])
            w = x2 - x1
            h = y2 - y1
            bbox = [x1, y1, w, h]
            segs = [[x1, y1, x2, y1, x2, y2, x1, y2]]

            annotations_json = dict()
            annotations_json['segmentation'] = segs
            annotations_json['area'] = w * h
            annotations_json['iscrowd'] = 0
            annotations_json['image_id'] = image_id
            annotations_json['bbox'] = bbox
            annotations_json['category_id'] = GET_CATEGORY_ID[c]
            annotations_json['id'] = annotations_id

            coco['annotations'].append(annotations_json)

            annotations_id = annotations_id + 1

        image_id = image_id + 1

    with open(coco_json_file, 'w') as fw:
        fw.write(json.dumps(coco))
        print("Saving to " + coco_json_file)

if __name__ == '__main__':
    main()
    # get_all_category()

    # {'car': 1210055,
    # 'van': 204744,
    # 'pedestrianignore': 50214,
    # 'trafficcone': 178965,
    # 'bus': 104435,
    # 'carignore': 702550,
    # 'pedestrian': 190810,
    # 'truck': 123737,
    # 'othersignore': 15993,
    # 'motorcyclist': 38190,
    # 'barrowlist': 652,
    # 'unknown_unmovable': 3220,
    # 'tricyclelist': 11006,
    # 'cyclist': 22828,
    # 'unknown_movable': 252,
    # 'confused': 36}
