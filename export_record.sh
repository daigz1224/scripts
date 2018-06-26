#! /usr/bin/env bash
# Author: daiguozheng
# 用法：./export_record.sh folder
# 说明：提取目录下所有 .record 里面的 image 和 pointcloud 信息
# 前提：脚本运行之前在另一个终端开启 cyber_launch start export_msgs.launch

folder=$1
export_dir=$2

if [ ! $1 ]; then echo "command failed"; exit 1; fi

if [ ! $2 ]; then
    export_dir="~/Documents/export_dir";
    echo "use default export_dir: $export_dir";
fi

# cybertron 的 xxx/build/install 目录路径
cybertron="~/Documents/build/install"

dirname=${folder##*/}
if [ ! -d export_dir/$dirname ]; then
    mkdir export_dir/$dirname
fi

echo "cybertron: $cybertron"
echo "export_dir: $export_dir"
echo "Start exporting record files in  $folder to $export_dir"

for filename in $(ls $folder)
do
    # 运行程序
    echo "=================| start play $filename |================="
    cyber_recorder play $folder/$filename

    # 整理输出
    name="${filename%.*}"
    mkdir $export_dir/$dirname/$name
    echo "mv output to $export_dir/$dirname/$name"
    cd $cybertron
    mv sensor_camera_smartereye_image_data/* $export_dir/$dirname/$name/image/
    mv sensor_velodyne16_all_compensator_PointCloud2_data/* $export_dir/$dirname/$name/pointcloud/

done

echo "End export all record files in $folder to $export_dir."