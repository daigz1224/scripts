import os
import json

ground_truth_json_path = "/home/dai/Documents/GitHub/detectron/detectron/datasets/data/20180703_coco/annotations/" \
                         "instances_all.json"
ground_truth_txt_dir = "/home/dai/Documents/GitHub/detectron/detectron/datasets/data/20180703_coco/annotations/" \
                       "instances_all"
total_num_images = 281620

def main():
    if not os.path.exists(ground_truth_txt_dir):
        os.mkdir(ground_truth_txt_dir)

    with open(ground_truth_json_path, 'r') as fr:
        ground_truth = json.loads(fr.read())

    annoations = ground_truth['annotations']

    count = 0
    one_anno_list = []

    for anno in annoations:
        if count % 10000 == 0:
            print("LOG: Processing anno: " + str(count))
        count += 1

        image_id = anno['image_id']
        image_id_0 = "%06d" % image_id
        category_id = anno['category_id']
        bbox = anno['bbox']

        one_anno_list.append(category_id)
        one_anno_list.extend(bbox)

        one_line = ' '.join([str(i) for i in one_anno_list])
        one_anno_list.clear()

        txt_path = os.path.join(ground_truth_txt_dir, image_id_0 + '.txt')
        with open(txt_path, 'a') as fw:
            fw.write(one_line)
            fw.write('\n')

if __name__ == "__main__":
    main()
    print("DONE.")