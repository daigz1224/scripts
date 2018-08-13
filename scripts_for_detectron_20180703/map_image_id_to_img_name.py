import json
import pickle

ground_truth_json_path = "/home/dai/Documents/GitHub/detectron/detectron/datasets/data/20180703_coco/annotations/instances_all.json"
image_id2name_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/annotations/image_id2name.pkl"

def main():

    image_id2name = dict()

    with open(ground_truth_json_path, 'r') as fr:
        ground_truth = json.loads(fr.read())

    imgs_info = ground_truth['images']

    for info in imgs_info:
        image_id, image_name = info['id'], info['file_name']
        if image_id % 10000 == 0:
            print(str(image_id) + ' -> ' + image_name)
        image_id2name[image_id] = image_name

    with open(image_id2name_path, 'wb') as fw:
        pickle.dump(image_id2name, fw)

    print("LOG: Saving image_id2name.pkl to " + image_id2name_path)

if __name__ == "__main__":
    main()
    print("DONE.")