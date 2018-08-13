import os
import shutil

root_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco"
label_train_path = os.path.join(root_path, 'kitti_labels_33d_train')
label_val_path = os.path.join(root_path, 'kitti_labels_33d_val')
image_val_path = os.path.join(root_path, 'images_val')

# ATTENTION:
# the 'labels_train' is equal to 'labels_all' now.
# we will reduce the label which belong to 'labels_val'
def main():

    for img in os.listdir(image_val_path):
        name = img.split('.')[0]
        label = str(name) + '.txt'
        label_path = os.path.join(label_train_path, label)
        shutil.move(label_path, label_val_path)

if __name__ == "__main__":
    main()