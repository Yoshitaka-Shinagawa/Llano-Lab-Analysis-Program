# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:32:46 2020

@author: Yoshi
"""

import fissa

#import holoviews as hv

rois_location = 'D:/Yoshi/Google Drive (UIUC)/University of Illinois at Urbana-Champaign/Work/Llano Lab/Tonotopic Analysis/2019-07-18/2019-07-18 Anesthetized IC Area 1/Test/20150429.zip'
images_location = 'D:/Yoshi/Google Drive (UIUC)/University of Illinois at Urbana-Champaign/Work/Llano Lab/Tonotopic Analysis/2019-07-18/2019-07-18 Anesthetized IC Area 1/Test/20150429'
output_folder = 'D:/Yoshi/Google Drive (UIUC)/University of Illinois at Urbana-Champaign/Work/Llano Lab/Tonotopic Analysis/2019-07-18/2019-07-18 Anesthetized IC Area 1/Test/FISSA_output_test'

experiment = fissa.Experiment(images_location,rois_location,output_folder,ncores_preparation=4,ncores_separation=4)
# experiment.separate()

# import matplotlib.pyplot as plt
# plt.plot(experiment.raw[0][0][0,:])
# plt.plot(experiment.result[0][0][0,:])

# c = 0
# t = 0
# cell = hv.Curve(experiment.roi_polys[c][t][0][0])
# neuropil1 = hv.Curve(experiment.roi_polys[c][t][1][0])
# cell*neuropil1