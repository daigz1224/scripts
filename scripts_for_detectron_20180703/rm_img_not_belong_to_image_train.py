import os

root_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco"
image_val_path = os.path.join(root_path, 'images_val')
image_train_path = os.path.join(root_path, 'images_train')

def main():

    for img in os.listdir(image_val_path):
        rm_path = os.path.join(image_train_path, img)
        os.remove(rm_path)

if __name__ == "__main__":
    main()