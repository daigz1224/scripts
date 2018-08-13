import os
import random
import shutil

root_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703/data"
image_val_dir = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/images_val"
percentage = 0.1


def main():

    for mark_task in os.listdir(root_path):

        dir_path = os.path.join(root_path, mark_task, 'images')

        if not os.path.isdir(dir_path):
            continue

        for dirname in os.listdir(dir_path):

            img_path = os.path.join(dir_path, dirname)

            if not os.path.isdir(img_path):
                continue

            img_list = os.listdir(img_path)

            n_val = int(len(img_list) * percentage)
            print(n_val)

            img_val = random.sample(img_list, n_val)

            for img in img_val:
                src = os.path.join(img_path, img)
                shutil.copy(src, image_val_dir)


if __name__ == "__main__":
    main()