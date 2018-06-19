# create_symlink.py

import os

input_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/export_data/0606_rain/"

for record in os.listdir(input_path):
     record_path = input_path + record
     new_path = "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/rain_data/0606/" + record
     os.symlink(record_path, new_path)