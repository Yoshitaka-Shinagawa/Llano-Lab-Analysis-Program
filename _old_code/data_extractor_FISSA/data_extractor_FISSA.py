# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:33:28 2019

@author: Yoshi
"""

import os
import numpy as np
import csv
import fissa
import shutil
import zipfile
from skimage import io



from roi_zip_reader import *
from key_reader import *
from background_subtractor import *

def data_extractor_FISSA(path):
    
    # Location of the data path
    data_path = f'{path}/Data'
    os.chdir(data_path)
    
    # If combined ROI set exists, deletes it
    if os.path.exists('RoiSet_FISSA.zip'):
        os.remove('RoiSet_FISSA.zip')
    
    # Import ROIs with two different ways of reading depending on whether there are one or two sets of ROIs
    roi_zip_list = [file for file in os.listdir(data_path) if file.endswith('.zip')]
    extra_flag = 'N/A'
    if len(roi_zip_list) == 2:
        for roi_zip in roi_zip_list:
            if 'non' not in roi_zip:
                extra_flag = roi_zip[7:-4]
                locations_1,flags_1 = roi_zip_reader(extra_flag,roi_zip)
            elif 'non' in roi_zip:
                locations_2,flags_2 = roi_zip_reader('N/A',roi_zip)
            else:
                print('Error! ROIs are not named properly!')
                return
        cell_locations = locations_1 + locations_2
        cell_flags = flags_1 + flags_2
    elif len(roi_zip_list) == 1:
        cell_locations,cell_flags = roi_zip_reader('N/A',roi_zip_list[0])
    elif len(roi_zip_list) != 0:
        print('Error! Too many ROI zip files found!')
        return
    else:
        print('Error! No ROI zip file found!')
        return
    
    # Declares start of data extraction
    print('Starting data extraction')
    
    # Sets up the information for FISSA
    images_location = f'{path}/Stabilized Images'
    output_folder = f'{path}/Fissa Output Folder'
    if os.path.exists(output_folder) == False:
        os.mkdir(output_folder)
    
    # Deletes prep files for FISSA since it can trigger a bug
    if os.path.exists(f'{output_folder}/preparation.npy'):
        os.remove(f'{output_folder}/preparation.npy')
    if os.path.exists(f'{output_folder}/separated.npy'):
        os.remove(f'{output_folder}/separated.npy')
    
    # Two ROI zips
    if len(roi_zip_list) == 2:
        
        # Combines the two zip files into a single file
        for roi_zip in roi_zip_list:
            if 'non' not in roi_zip:
                shutil.copy(roi_zip,'RoiSet_FISSA.zip')
                flag_zip = zipfile.ZipFile('RoiSet_FISSA.zip','a')
            elif 'non' in roi_zip:
                non_flag_zip = zipfile.ZipFile(roi_zip,'r')
        [flag_zip.writestr(t[0],t[1].read()) for t in ((n,non_flag_zip.open(n)) for n in non_flag_zip.namelist())]
        flag_zip.close()
        
        # Sets location of ROI zip to combined zip
        rois_location = f'{data_path}/RoiSet_FISSA.zip'
    
    # One ROI zip
    elif len(roi_zip_list) == 1:
        
        # Sets location of ROI zip to single zip
        rois_location = f'{data_path}/{roi_zip_list[0]}'
    
    # Runs FISSA
    experiment = fissa.Experiment(images_location,rois_location,output_folder,ncores_preparation=8,ncores_separation=8)
    experiment.separate()
    
    # Reading data from new data set
    if 0 == 1:#experiment.result.shape[1] == 10:
        print('WIP')
        return
    
    # Reading data from old data set
    else:
        
        # Read framerate info
        if os.path.exists(f'{data_path}/framerates.csv') == True:
            open_framerate_file = open(f'{data_path}/framerates.csv')
            framerate_file = csv.reader(open_framerate_file)
            framerate_information = []
            for row in framerate_file:
                for info in row:
                    framerate_information.append(float(info))
            framerate_information[0] = int(framerate_information[0])
        else:
            print('Error! Framerate data not found!')
            return
        
        # Converts data to dF/F
        experiment.calc_deltaf(freq=framerate_information[0], across_trials=True)
        
        # Creates empty numpy array to write data into
        cells = experiment.deltaf_result.shape[0]
        samples = experiment.deltaf_result.shape[1]
        frames = experiment.deltaf_result[0,0].shape[1]
        data_duration = round(framerate_information[0]*framerate_information[1])
        cycle_duration = round(framerate_information[0]*framerate_information[2])
        cycles = int(frames/cycle_duration)
        data = np.zeros((cells,samples,cycles-1,cycle_duration),dtype=np.float32)
        
        # Copies data from experiment module to numpy array
        for cell in range(cells):
            for sample in range(samples):
                sample_data = experiment.deltaf_result[cell][sample][0,:]
                
                # Separates sample into cycles and store data into numpy array
                for cycle in range(1,cycles):
                    cycle_start = cycle*cycle_duration
                    cycle_end = cycle_start + data_duration
                    cycle_data = sample_data[cycle_start:cycle_end]
                    subtracted_cycle_data = background_subtractor(cycle_data)
                    data[cell,sample,cycle-1] = subtracted_cycle_data * 100
        
        # Reads key from file
        if os.path.exists(f'{data_path}/key.csv'):
            key,frequencies,decibels = key_reader(path)
        else:
            print('Error! Key not found!')
            return
    
    # Declares end of data extraction
    print('Finished data extraction')
    
    return extra_flag,cell_locations,cell_flags,data,framerate_information,key,frequencies,decibels