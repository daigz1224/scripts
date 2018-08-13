import os
import json

bbox_results_json_path = "/home/dai/Documents/GitHub/detectron/test/20180703_coco_all/generalized_rcnn/" \
                         "bbox_20180703_coco_all_results.json"
bbox_results_txt_dir = "/home/dai/Documents/GitHub/detectron/test/20180703_coco_all/generalized_rcnn/" \
                       "bbox_20180703_coco_all_results"
total_num_images = 281620

def main():
    if not os.path.exists(bbox_results_txt_dir):
        os.mkdir(bbox_results_txt_dir)

    with open(bbox_results_json_path, 'r') as fr:
        bbox_results = json.loads(fr.read())

    count = 0
    one_bbox_list = []

    for one_bbox in bbox_results:
        if count % 50000 == 0:
            print("LOG: Processing bbox: " + str(count))
        count += 1

        image_id = one_bbox['image_id']
        image_id_0 = "%06d" % image_id
        category_id = one_bbox['category_id']
        bbox = one_bbox['bbox']
        score = one_bbox['score']

        one_bbox_list.append(category_id)
        one_bbox_list.extend(bbox)  # Attention!
        one_bbox_list.append(score)

        one_line = ' '.join([str(i) for i in one_bbox_list])
        one_bbox_list.clear()

        txt_path = os.path.join(bbox_results_txt_dir, image_id_0 + '.txt')
        with open(txt_path, 'a') as fw:
            fw.write(one_line)
            fw.write('\n')

def fill_all_image_id():
    for i in range(total_num_images):
        ii = "%06d" % i
        txt_path = os.path.join(bbox_results_txt_dir, ii + '.txt')
        if os.path.exists(txt_path) == 0:
            print('LOG: touch ' + ii + '.txt')
            with open(txt_path, 'r'):
                pass

if __name__ == "__main__":
    # main()
    fill_all_image_id()
    print("DONE.")