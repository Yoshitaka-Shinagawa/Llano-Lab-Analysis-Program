# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:33:28 2019

@author: Yoshi
"""

import os
import copy

program_path = 'D:/Yoshi/Google Drive (UIUC)/University of Illinois at Urbana-Champaign/Work/Llano Lab/Tonotopic Analysis/Program'

os.chdir(f'{program_path}/data_extractor')
from data_extractor import *
os.chdir(f'{program_path}/p_value_tests')
from cell_flagger_0 import *
from cell_flagger_1 import *
from cell_flagger_2 import *
from cell_flagger_3 import *
os.chdir(f'{program_path}/tonotopic_map_generator')
from tonotopic_map_generator import *
os.chdir(f'{program_path}/cell_grapher')
from cell_grapher import *
os.chdir(f'{program_path}/debug_tools')
from sum_grapher import *

def p_value_test(path):
    
    p_value_directory = f'{path}/P-value Test'
    os.mkdir(p_value_directory)
    
    # Stabilizes, filters, and extracts the data from the images
    extra_flag,cell_locations,cell_flags,data,dfof_data,base_image,framerate = data_extractor(path)
    
    # p-value = 0.001
    path_0 = f'{p_value_directory}/0.0001'
    os.mkdir(path_0),os.mkdir(f'{path_0}/Output')
    cell_flags_0 = copy.deepcopy(cell_flags)
    cell_flags_0,key,frequencies,decibels = cell_flagger_0(path,cell_flags_0,dfof_data)
    tonotopic_map_generator(path_0,base_image,cell_locations,frequencies,cell_flags_0,extra_flag)
    cell_grapher(path_0,dfof_data,cell_flags_0,framerate,key,frequencies,decibels)
    
    # p-value = 0.05
    path_1 = f'{p_value_directory}/0.05'
    os.mkdir(path_1),os.mkdir(f'{path_1}/Output')
    cell_flags_1 = copy.deepcopy(cell_flags)
    cell_flags_1,key,frequencies,decibels = cell_flagger_1(path,cell_flags_1,dfof_data)
    tonotopic_map_generator(path_1,base_image,cell_locations,frequencies,cell_flags_1,extra_flag)
    cell_grapher(path_1,dfof_data,cell_flags_1,framerate,key,frequencies,decibels)
    
    # p-value = 0.01
    path_2 = f'{p_value_directory}/0.01'
    os.mkdir(path_2),os.mkdir(f'{path_2}/Output')
    cell_flags_2 = copy.deepcopy(cell_flags)
    cell_flags_2,key,frequencies,decibels = cell_flagger_2(path,cell_flags_2,dfof_data)
    tonotopic_map_generator(path_2,base_image,cell_locations,frequencies,cell_flags_2,extra_flag)
    cell_grapher(path_2,dfof_data,cell_flags_2,framerate,key,frequencies,decibels)
    
    # p-value = 0.001
    path_3 = f'{p_value_directory}/0.001'
    os.mkdir(path_3),os.mkdir(f'{path_3}/Output')
    cell_flags_3 = copy.deepcopy(cell_flags)
    cell_flags_3,key,frequencies,decibels = cell_flagger_3(path,cell_flags_3,dfof_data)
    tonotopic_map_generator(path_3,base_image,cell_locations,frequencies,cell_flags_3,extra_flag)
    cell_grapher(path_3,dfof_data,cell_flags_3,framerate,key,frequencies,decibels)
    
    return #extra_flag,cell_locations,cell_flags,data,dfof_data,base_image,framerate,key,frequencies,decibels