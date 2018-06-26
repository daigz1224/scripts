#! /usr/bin/env bash
# Author: daiguozheng
# Usage: ./generate_train_txt.sh folder train.txt

folder=$1
txt=$2

files=`ls $1`

for f in $file
do
    name=${f%.*};
    echo $name >> $2
done