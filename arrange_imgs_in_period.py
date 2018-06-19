import os
import shutil
from matplotlib import pyplot as plt

input_path = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/data_night'
input_name = input_path.split('/')[-1]

period = 10  # 10 min
output_dir = '/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files' + '/data_night_' + str(period) + '_min'

if os.path.exists(output_dir) == 0:
    os.mkdir(output_dir)


def key_record(record):
    num = record.split('_')[3]
    return int(num)

recordlist = sorted(os.listdir(input_path), key=key_record)
# because data_night have 2 source: 0606 and 0607
sublist = [recordlist[i: i+period*2] for i in range(0, len(recordlist), period*2)]
print(str(len(sublist)) + ' sublist in total...')

for index in range(len(sublist)):
    if os.path.exists(output_dir + '/' + str(index)) == 0:
        print('mkdir ' + output_dir + '/' + str(index) + '...')
        os.mkdir(output_dir + '/' + str(index))
    for r in sublist[index]:
        print('index = ' + str(index) + ', record = ' + r)
        for f in os.listdir(input_path + '/' + r + '/image_data'):
            if f.endswith('.jpg'):
                # print('copying ' + f + '...')
                f_path = input_path + '/' + r + '/image_data/' + f
                target_path = output_dir + '/' + str(index) + '/' + f
                shutil.copyfile(f_path, target_path)

print('end.')