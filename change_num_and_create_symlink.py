# change_num_and_create_symlink.py
import os
import shutil

input_path="/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/export_data/0606_night"
output_path="/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/tmp"

for record in os.listdir(input_path):
    print(record)
    record_split = record.split('_')
    num = int(record_split[3])
    num = num - 1
    new_record_split = record_split[:3]
    new_record_split.append(str(num))
    new_record_split = new_record_split + record_split[4:]
    new_record = '_'.join(new_record_split)
    print(new_record)
    record_path = input_path + '/' + record
    new_record_path = output_path + '/' + new_record
    os.symlink(record_path, new_record_path)

