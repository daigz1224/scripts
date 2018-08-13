import os
import pickle


# INPUT:
scores_pkl_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                  "scores.pkl"
# OUTPUT:
outlier_ids_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/20180703_coco/" \
                   "outlier_ids.txt"

def select_outlier():

    with open(scores_pkl_path, 'rb') as f:
        scores = pickle.load(f)

    outliers = []

    for ii in scores:
        s = scores[ii]
        if s['det_none'] != s['gt_none']:
            outliers.append(ii)

    print(outliers)
    with open(outlier_ids_path, 'w') as f:
        for ii in outliers:
            f.write(ii)
            f.write('\n')

if __name__ == "__main__":
    main()
    print("DONE.")