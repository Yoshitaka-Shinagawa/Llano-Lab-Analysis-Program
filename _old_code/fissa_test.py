# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:37:08 2019

@author: Yoshi
"""

import fissa



# Info to put into FISSA
output_folder = 'D:/Llano Lab/FISSA test/Output Folder'
roi = 'D:/Llano Lab/FISSA test/20150429.zip'
data_folder = 'D:/Llano Lab/FISSA test/20150529'

# Works
experiment = fissa.Experiment(data_folder,roi,output_folder,ncores_preparation=8,ncores_separation=8)
experiment.separate(redo_prep=True, redo_sep=True)



# Info to put into FISSA
images_location = 'D:/Llano Lab/Tonotopic Analysis/Data Set 1/2019-07-18/Gaussian Filter Test (1,1,3)/Stabilized Images'
output_folder = 'D:/Llano Lab/Tonotopic Analysis/Data Set 1/2019-07-18/Gaussian Filter Test (1,1,3)/Fissa Output Folder'
rois_location = 'D:/Llano Lab/Tonotopic Analysis/Data Set 1/2019-07-18/Gaussian Filter Test (1,1,3)/Data/RoiSet_FISSA.zip'

# Doesn't work
experiment = fissa.Experiment(images_location,rois_location,output_folder)
experiment.separate(redo_prep=True, redo_sep=True)
