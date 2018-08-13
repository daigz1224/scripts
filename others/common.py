#!/usr/bin/env python
# coding: utf-8
"""
   File Name: utils/common.py
      Author: Wan Ji
      E-mail: wanji@live.com
  Created on: Thu 06 Jul 2017 09:21:28 AM CST
 Description:
"""
NAME2ID_MAP = {
    'car':                  0,
    'van':                  0,
    'bus':                  0,
    'truck':                0,
    'vehicle':              0,
    'cyclist':              1,
    'motorcyclist':         1,
    'bicycle':              1,
    'tricyclelist':         1,
    'pedestrian':           2,
    'trafficcone':          3,
    # KITTI labels
    'Car':                  0,
    'Van':                  0,
    'Tram':                 0,
    'Truck':                0,
    'Cyclist':              1,
    'Pedestrian':           2,
    'Person_sitting':       2,
    # 'Misc':               -1,
    # 'DontCare':           -1,
}
# wuk: with unknown
NAME2ID_MAP_wuk = NAME2ID_MAP.copy()
NAME2ID_MAP_wuk['unknown_unmovable'] = 4
NAME2ID_MAP_wuk['unknown_movable'] = 5
NAME2ID_MAP_8cls = {
    'car':             0,
    'van':             1,
    'bus':             2,
    'truck':           3,
    'cyclist':         4,
    'motorcyclist':    4,
    'tricyclelist':    5,
    'barrowlist':      5,
    'pedestrian':      6,
    'trafficcone':     7,
    # KITTI labels
    'Car':             0,
    'Van':             1,
    'Bus':             2,
    'Tram':            2,
    'Truck':           3,
    'Cyclist':         4,
    'Pedestrian':      6,
    'Person_sitting':  6,
    # 'Misc':           -1,
    # 'DontCare':       -1,
}
NAME2ID_MAP_11cls = {
    'car':              0,
    'van':              1,
    'bus':              2,
    'truck':            3,
    'cyclist':          4,
    'motorcyclist':     5,
    'tricyclelist':     6,
    'barrowlist':       6,
    'pedestrian':       7,
    'trafficcone':      8,
    'unknown_unmovable':9,
    'unknown_movable':  10,
    # KITTI labels
    'Car':              0,
    'Van':              1,
    'Bus':              2,
    'Tram':             2,
    'Truck':            3,
    'Cyclist':          4,
    'Pedestrian':       7,
    'Person_sitting':   7,
    # 'Misc':           -1,
    # 'DontCare':       -1,
}
LABEL_MAP = {
    1:    'car',
    2:    'truck',
    3:    'van',
    4:    'bus',
    5:    'pedestrian',
    6:    'cyclist',
    7:    'tricyclelist',
    8:    'motorcyclist',
    12:    'barrowlist',
    13:    'pedestrianignore',
    14:    'carignore',
    15:    'othersignore',
    16:    'trafficcone',
    17:    'confused',
    18:    'unknown_unmovable',
    19:    'unknown_movable',
    21:    'plate',
    22:    'face',
}
