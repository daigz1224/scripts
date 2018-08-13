import sys
import os
import json
import cv2
import math
import random as rd
import numpy as np

ANNO = 'annotation'
results_pic = 'pic/'
INFO_DOMAIN_NUM = 5 
image_all_num = 0
sub_type_num = 26
show_image = True 
save_annotation =True
#file_filter = 'mark_task_3056-layer1-city-test-LAYER1_BARRIER_2018'
#file_filter = 'mark_task_2988-layer1-city-test-LAYER1_BARRIER_2018'
file_filter = 'mark_task_3200-layer1-test-LAYER1_BARRIER_2018'
obj_crop = False 
obj_crop_only_car = True 
#ARZ033
k = [2015.462836979624, 0.0, 950.9007353846725, 0.0, 2008.7783500949665, 536.7185567781081, 0.0, 0.0, 1.0]
k_m = np.matrix('2015.462836979624, 0.0, 950.9007353846725; 0.0, 2008.7783500949665, 536.7185567781081; 0.0, 0.0, 1.0')
#k 3*3 camera intrinsic mat
def get_ry_from_label_is_front(bbox, x_mid, is_left, hwl):
    pi = 3.14159265359
    w = bbox[2] - bbox[0]
    f = k[0] + k[4] / 2
    height_near = bbox[3] - bbox[1]
    print "Typ: ", type(hwl[0])
    z_near = f * hwl[0] / height_near
    ry_label = 0
#    wp = is_left ? (x_mid - bbox[0]) : (bbox[2] - x_mid)
    wp = (x_mid - bbox[0]) if is_left else (bbox[2] - x_mid)
    lp = w - wp
#    print height_near
#    print z_near
#    print wp
#    print lp
#    print f
#    print hwl[2]
#    print hwl[1]
#    print z_near * wp / (f * hwl[1])
    if wp < (w / 4):
        value = z_near * lp / (f * hwl[2])
        if value > 1:
            value = 1;
        ry_label = math.acos(value)
    else:
        value = z_near * wp / (f * hwl[1])
        if value > 1:
            value = 1;
        ry_label = math.asin(value)

    ry_label = max(pi - ry_label, ry_label) if is_left else min (pi - ry_label, ry_label)
    return ry_label

def calculation_rotation_from_label(bbox, x_mid, is_front, is_left, hwl, k):
    pi = 3.14159265359
    w = bbox[2] - bbox[0]
    d = min(abs(x_mid - bbox[0]), abs(x_mid - bbox[2]))
    ry_label = 0
    if d < max(w / 20.0, 3):
        ry_label = pi / 2 if is_front else -pi / 2
        return ry_label
    if not is_front:
        ry_label = get_ry_from_label_is_front(bbox, x_mid, not is_left, hwl)
        ry_label -= pi

    if ry_label > pi:
        ry_label -= 2*pi
    if ry_label < -pi:
        ry_label += 2*pi

    return ry_label

#    f = k[0] + k[4] / 2
#    height_near = bbox[3] - bbox[1]
#    print "Typ: ", type(hwl[0])
#    z_near = f * hwl[0] / height_near
#    ry_label = 0
##    wp = is_left ? (x_mid - bbox[0]) : (bbox[2] - x_mid)
#    wp = (x_mid - bbox[0]) if is_left else (bbox[2] - x_mid)
#    lp = w - wp
##    print height_near
##    print z_near
##    print wp
##    print lp
##    print f
##    print hwl[2]
##    print hwl[1]
##    print z_near * wp / (f * hwl[1])
#    if wp < (w / 4):
#        value = z_near * lp / (f * hwl[2])
#        if value > 1:
#            value = 1;
#        ry_label = math.acos(value)
#    else:
#        value = z_near * wp / (f * hwl[1])
#        if value > 1:
#            value = 1;
#        ry_label = math.asin(value)
#
#    ry_label = max(pi - ry_label, ry_label) if is_left else min (pi - ry_label, ry_label)
#    if not is_front:
#        ry_label -= pi
#    return ry_label
def calculation_rotation_from_label_1(bbox, x_mid, segment_type, is_left, hwl, k) :
    ration_thresh = 10
    pi = math.pi
#    print bbox
#    print k
#    print x_mid
#    print hwl
    
    is_w_left = (segment_type == 1) or (segment_type == 3) 
    ry_label = 0
#    if d < max((bbox[2] - bbox[0]) / 10.0, 3):
#        ry_label = pi / 2 if not is_front else -pi / 2
#        return ry_label
    l_line = np.matrix([[bbox[0]], [bbox[3]], [1.0]])
    r_line = np.matrix([[bbox[2]], [bbox[3]], [1]])
#   print l_line
#   print r_line
    l_line_real = k_m.I * l_line 
    r_line_real = k_m.I * r_line 
    print l_line_real
    print r_line_real
    tan_l = l_line_real[0] / l_line_real[2]
    tan_r = r_line_real[0] / r_line_real[2]
#    print "tan_l: ", tan_l
#    print "tan_r: ", tan_r
    print "tan_l_angle: ", math.atan(tan_l) * 180 / pi
    print "tan_r_angle: ", math.atan(tan_r) * 180 / pi
    if bbox[2] - x_mid < 0.3:
        seg_ratio = 30
    else:
        seg_ratio = (x_mid - bbox[0]) / (bbox[2] - x_mid)
    print "seg_ratio: ", seg_ratio
    lw_ratio = hwl[2] / hwl[0]
    print 'lw_ratio: ', lw_ratio
    if not is_w_left:
        lw_ratio = 1 / lw_ratio
        #rotation_tan = (1 + seg_ratio * (1 / lw_ratio) * tan_r) /(-tan_l + seg_ratio * (1 / lw_ratio))
        #rotation_tan = (-tan_l + seg_ratio / lw_ratio) / (1 + seg_ratio / lw_ratio * tan_r)
    rotation_tan = (-tan_l + seg_ratio * lw_ratio) / (1 + seg_ratio * lw_ratio * tan_r)
    print "fenmu: ", (1 + seg_ratio * lw_ratio * tan_r)
    
    print 'rotation_tan: ', rotation_tan
    print 'rotation_angle: ', math.atan(rotation_tan) * 180 / pi 
    ry_label = math.atan(rotation_tan) 
    if is_left and ry_label < 0:
        ry_label += pi

    print 'ry_label: ', ry_label
    if segment_type == 1:
        ry_label -= pi
    elif segment_type == 2:
        ry_label -= pi / 2
    elif segment_type == 4:
        ry_label += pi / 2
    if ry_label > pi:
        ry_label -= 2*pi
    if ry_label < -pi:
        ry_label += 2*pi
    #right, left car tail, ry_label < pi / 2
    #if segment_type == 3 and not is_left and ry_label > pi * 8 / 9:
    #    ry_label = 0 

    #print 'ry_label: ', ry_label
    #if segment_type == 4 and is_left and ry_label < pi * 1 / 9:
    #    ry_label = pi 
    print 'ry_label: ', ry_label
    #clockwise positive
    ry_label = -ry_label

    print "angle: ", int(ry_label * 180 / pi)
    return ry_label


#load size table
print 'load size table.'
table_file = open('table_size.txt', 'r')
table_lines = table_file.readlines()
table_file.close()
#h w l
obj_size_table = []
for line in table_lines:
    line = line.strip()
    line = line.split()
    obj_size_table.append([float(line[3]), float(line[2]), float(line[1])])

#print "table_file: ", obj_size_table[0][0]

#exit(-1)

box_colors = [(rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)) for c in range(sub_type_num)] 
print box_colors

label_valid_num = 0

if not os.path.isdir(ANNO):
    os.system('mkdir -p %s' % (ANNO))
for datafolder in os.listdir("./") :
#    print datafolder
    if datafolder[-7:] == '.tar.gz':
        datafolder_src = datafolder[0:-7]
        if datafolder_src != file_filter:
            continue
        print datafolder_src
        dst_file_folder = ANNO + datafolder_src;
        for subset in os.listdir(datafolder_src):
            #print subset
            if subset.find('result.txt') == -1:
                continue

            # parse the results.
            result_file = datafolder_src + '/' + subset
            result_file_ptr = open(result_file, 'r')
            info_lines = result_file_ptr.readlines()
            result_file_ptr.close()
            #print "processing : %s" % (result_file)
            if len(info_lines) > 0 :
                header = info_lines[0].strip().split('\t')[0]
                if header == 'video_name' or header == 'file_name':
                    info_lines = info_lines[1:] # discard the info menu header Line
            else:
                print "result file is empty."
                exit(-1)
            for line in info_lines:
                line = line.strip()
                if not line:
                    continue
                image_all_num = image_all_num + 1 
                print "image_all_num: ", image_all_num
                #if image_all_num < 35:
                #    continue
                
                infos = line.split('\t')
                if len(infos) != INFO_DOMAIN_NUM :
                    print "Info line does not has enough num of info domains ({} vs [{}])".format(len(infos), INFO_DOMAIN_NUM)
                    exit(-1)

                file_name = infos[0]
                frame_id = infos[1]
                image_file = infos[2]
                label_result = infos[3]
                draw_save_dir = results_pic
                image_file_name = image_file[image_file.rfind('/') + 1 : ];
                image_file_name = image_file_name[0:image_file_name.rfind('.')]
                image_file_temp = image_file
                im_draw_file = os.path.join(draw_save_dir, image_file_temp.replace('/', '_'))
                #print "im_draw_file: ", im_draw_file
                image_file = datafolder_src + '/' + image_file
                print "image_file: ", image_file
                #print image_file
                im = cv2.imread(image_file)
                if im is None:
                    print 'img is None'
                    continue
                im_height, im_width, im_channels = im.shape
                #print im_height, im_width, im_channels
                #exit(-1)
#                print label_result
                try:
                    result_json_info = json.loads(label_result)
                    #print result_json_info


                    if len(result_json_info) == 0:
                        print 'Get no valid info from json string "{}", continue flag'.format(label_result)
                        continue
                    #print result_json_info['videoName']
                    #print result_json_info['numberBox']
                    #print result_json_info['result']
                    video_name = result_json_info['videoName']
                    num_obj = result_json_info['numberBox']
                    result_str = result_json_info['result']
                except Exception, e:
                    print "parse json faild, continue"
                    #traceback.print_exc()
                    continue
                frame_obj_info = []
                label_valid_num = 0
                for obj in xrange(num_obj):
                    label_info_i = result_str[obj]
                    obj_type = int(label_info_i['tag'])
                    sub_type = int(label_info_i['sub_type'])
                    height = float((label_info_i['h']))
                    width = float(label_info_i['w'])
                    x = float(label_info_i['x'])
                    y = float(label_info_i['y'])
                    x1 = max(0, int(min(im_width - 1, x) + 0.5))
                    y1 = max(0, int(min(im_height - 1, y) + 0.5))
                    x2 = max(0, int(min(im_width - 1, x + width - 1) + 0.5))
                    y2 = max(0, int(min(im_height - 1, y + height -1) + 0.5))
                    bbox_float = [x, y, x + width, y + height]
                    istruncated = int(label_info_i['istruncated'])
                    isoccluded = int(label_info_i['isoccluded'])
                    segment_info = label_info_i['segment']
                    #segment_type = segment_info[0]
                    #make sure head tail 
                   # print label_info_i
                   # print segment_info
                   # print obj
                    if len(segment_info) > 0 :
                        if segment_info.has_key('head'):
                            segment_type = int(segment_info['head']['segment_type'])
                            x_offset = float(segment_info['head']['x_offset'])
                        else:
                            segment_type = int(segment_info['tail']['segment_type'])
                            x_offset = float(segment_info['tail']['x_offset'])
                    else:
                        segment_type = 0
                        x_offset = 0
                        #continue

                    #calculate rotation    
                    #def calculation_rotation_from_label(bbox, x_mid, is_front, is_left, hwl, k):
                    bbox = [x1, y1, x2, y2]
                    #tail, forward
                    is_front = segment_type > 2 
                    #is_left = (segment_type == 1) or (segment_type == 3) 
                    print "sub_type: ", sub_type
                    hwl = obj_size_table[sub_type - 1]
                    print "hwl: ", hwl
                    x_mid = bbox[0] + x_offset
                    is_left = x_mid <  im_width / 2
                    print 'x_offset: ', x_offset
                    print 'istruncated: ', istruncated
                    if sub_type > 0:
                        label_valid_num += 1
                        print 'label_result: ', label_valid_num
                        
                        # xun solver
                        #is_front = not is_front
                        #rotation = calculation_rotation_from_label(bbox_float, x_mid, is_front, is_left, hwl, k)
                        
                        #my solver
                        rotation = calculation_rotation_from_label_1(bbox_float, x_mid, segment_type, is_left, hwl, k)
                    else:
                        rotation = 0
                    
                    print "rotation: ", rotation
                    if save_annotation:

                        if sub_type < 16:
                            # include -1 == ignore
                            sub_type_str = 'vehicle'
                        elif sub_type < 22:
                            sub_type_str = 'pedestrian'
                        else:
                            sub_type_str = 'bicycle'
                        #obj_anno = [sub_type, istruncated, isoccluded, -99,
                        obj_anno = [sub_type_str, 0, 0, -99,
                                bbox_float[0], bbox_float[1], bbox_float[2], bbox_float[3],
                                hwl[0], hwl[1], hwl[2],
                                -99, -99, -99, rotation, 0]
                        #print obj_anno
                        frame_obj_info.append(obj_anno)

                       # obj_anno_str = ' '.join(str(e) for e in obj_anno)
                       # print obj_anno_str
                       # exit()
                        
                    if show_image:
                        # draw bbox
                        box_color = box_colors[sub_type]
                        #thickness = 1 if ign != 0 else 2
                        #lineType = 4 if ign != 0 else 8
                        cv2.rectangle(im, (x1, y1), (x2, y2), box_color, 2)
                        if x_offset > 0:
                            mid_color = (0, 255, 255) if (segment_type <= 2) else (255, 255, 0)
                            cv2.line(im, (x1 + int(x_offset + 0.5), y1), (x1 + int(x_offset + 0.5), y2), mid_color, 1)
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            #cv2.putText(im, str(int(rotation * 180 / 3.1415926))+" "+str(segment_type) +" " + str(label_valid_num),(x1, y1), font, 0.5, (255, 255, 0), 1, cv2.CV_AA)
                            #cv2.putText(im, str(int(rotation * 180 / 3.1415926))+" "+str(segment_type), (x1, y1), font, 0.5, (255, 255, 0), 1, cv2.CV_AA)
                            cv2.putText(im, str(int(rotation * 180 / 3.1415926))+' '+str(sub_type), (x1, y1), font, 0.5, (255, 255, 0), 1, cv2.CV_AA)
                            #cv2.putText(im, str(int(segment_type)),(x1, y1), font, 0.5, (255, 255, 0), 1, cv2.CV_AA)
                    if obj_crop:
                        crop_add = 2
                        x1c = max(0, int(min(im_width - 1, x - crop_add) + 0.5))
                        y1c = max(0, int(min(im_height - 1, y - crop_add) + 0.5))
                        x2c = max(0, int(min(im_width - 1, x + width - 1 + crop_add) + 0.5))
                        y2c = max(0, int(min(im_height - 1, y + height -1 + crop_add) + 0.5))
                        crop_obj = im[y1c:y2c, x1c:x2c]
                        print  draw_save_dir + image_file_temp + str(label_valid_num) + '.jpg'
                        if obj_crop_only_car:
                            if sub_type > 15:
                                continue
                        #60 -> 50m : 1.5 height
                        if y2c-y1c > 100:
                            cv2.imwrite(draw_save_dir + image_file_temp.replace('/', '-') + str(label_valid_num) + '.jpg',  crop_obj)

                if show_image:
                    cv2.imwrite(im_draw_file, im)
                if save_annotation:
                    print "save_image_file: ", image_file_name
                    wfile = open(ANNO + '/' + image_file_name + '.txt', 'w')
                    for line in frame_obj_info:
                        line_str = ' '.join(str(e) for e in line)
                       # print line_str
                        wfile.write(line_str+'\n')
                    wfile.close()

                #exit()
                
               # if image_all_num > 100:
               #    exit(-1)

