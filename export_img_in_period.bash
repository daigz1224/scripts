#! /usr/bin/env bash
# bash export_img_in_period.bash

DIRPATH=$1
# e.g "/media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/export_data/0605_nigit_rain"
period=10
mkdir /media/dai/ed9cf21d-a757-4514-b33a-34472199d3b2/daiguozheng_files/export_img_in_10

for subdir in $(ls $DIRPATH)