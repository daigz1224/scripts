# Author: daiguozheng
# 用法：python3 arrange_imgs_in_period.py
# 说明：从 input_path 中按照一定的时间周期建立文件夹存放对应时间的图片。
# 前提：input_path 中需要筛选好特定时间段，该脚本 不会 按照文件名对应的时间进行提取。

import os
import shutil

def key_record(record):
    # 按照 record 文件名终中的关键数组进行排序
    num = record.split('_')[3]
    return int(num)

def main(input_path, period, output_dir):
    # input_name = input_path.split('/')[-1]
    recordlist = sorted(os.listdir(input_path), key=key_record)
    print("recordlist: \n")
    print(recordlist)
    sublist = [recordlist[i: i+period] for i in range(0, len(recordlist), period)]
    print("we got " + str(len(sublist)) + ' sublists in total.')

    for i in range(len(sublist)):
        ii = "%05d" % i  # 强行补零，方便字符串排序
        ## 创建时间目录
        index_path = output_dir + '/' + ii
        if os.path.exists(index_path) == 0:
            os.mkdir(index_path)
        ## 将每个 record 中的 jpg 拷贝到对应时间目录中
        for record in sublist[i]:
            record_path = input_path + '/' + record           
            print('time index: ' + ii + ', dealing with record file: ' + record)
            for f in os.listdir(record_path + '/image_data'):
                if f.endswith('.jpg'):
                    f_path = record_path + '/image_data/' + f
                    target_path = index_path + '/' + f
                    shutil.copyfile(f_path, target_path)

if __name__ == '__main__':
    input_dir_path = '~/Documents/export_dir/0607'
    period_min = 5  # min
    output_dir_path = '~/Documents/' + 'data_night_' + str(period_min) + '_minutes'
    
    if os.path.exists(output_dir_path) == 0:
        os.mkdir(output_dir_path)

    print("input_path: " + input_dir_path)
    print("period: " + str(period_min))

    main(input_dir_path, period_min, output_dir_path)

    print('End.')