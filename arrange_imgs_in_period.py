import os
import shutil
from matplotlib import pyplot as plt

input_path = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/night_data/0607'
input_name = input_path.split('/')[-1]

period = 5  # 10 min
output_dir = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files' + '/data_night_' + str(period) + '_minutes'

if os.path.exists(output_dir) == 0:
    os.mkdir(output_dir)


def key_record(record):
    num = record.split('_')[3]
    return int(num)

recordlist = sorted(os.listdir(input_path), key=key_record)
sublist = [recordlist[i: i+period] for i in range(0, len(recordlist), period)]
print(str(len(sublist)) + ' sublist in total...')

for index in range(len(sublist)):
    index = "%04d" % index
    ## 创建时间目录
    if os.path.exists(output_dir + '/' + index) == 0:
        print('mkdir ' + output_dir + '/' + index + '...')
        os.mkdir(output_dir + '/' + index)
    ## 将每个record中的jpg拷贝到对应时间目录中
    for r in sublist[index]:
        record_path = input_path + '/' + r            
        print('index = ' + index + ', record = ' + r)
        
        for f in os.listdir(input_path + '/' + r + '/image_data'):
            if f.endswith('.jpg'):
                # print('copying ' + f + '...')
                f_path = input_path + '/' + r + '/image_data/' + f
                target_path = output_dir + '/' + index + '/' + f
                shutil.copyfile(f_path, target_path)

print('end.')