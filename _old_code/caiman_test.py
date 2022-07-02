# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:43:25 2020

@author: Yoshi
"""

import os
base_path = 'D:/Yoshi/Google Drive (UIUC)/University of Illinois at Urbana-Champaign/Work/Llano Lab/Tonotopic Analysis'
folder = '/2019-07-18/2019-07-18 Anesthetized IC Area 1/Test'
path = base_path + folder
os.chdir(path)

import caiman as cm
test_movie = cm.load('stack_test.tif')
print(test_movie.shape)

from caiman.motion_correction import MotionCorrect, tile_and_correct, motion_correction_piecewise

max_shifts = (3,3)
strides = (48,48)
overlaps = (24,24)
mc = MotionCorrect(test_movie)
mc.motion_correct(save_movie=True)
MotionCorrect()