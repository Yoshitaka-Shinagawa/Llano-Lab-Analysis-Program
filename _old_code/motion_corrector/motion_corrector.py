# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:17:30 2021

@author: Yoshi
"""

import os
import shutil
import tifffile as tiff
from datetime import datetime



from base_image_creator import *
from motion_stabilizer import *

def motion_corrector(path,gauss_filter):
    
    # Creates output folder for stabilized images
    images_output_path = f"{path}/Stabilized Images"
    if os.path.exists(images_output_path) == True:
        shutil.rmtree(images_output_path)
    if os.path.exists(images_output_path) == False:
        os.mkdir(images_output_path)
    
    # Creates debug folder for storing averaged images
    debug_output_path = f"{path}/Output"
    if os.path.exists(debug_output_path) == False:
        os.mkdir(debug_output_path)
    if os.path.exists(f"{debug_output_path}/Debug") == False:
        os.mkdir(f"{debug_output_path}/Debug")
    if os.path.exists(f"{debug_output_path}/Debug/Average Images") == True:
        shutil.rmtree(f"{debug_output_path}/Debug/Average Images")
    if os.path.exists(f"{debug_output_path}/Debug/Average Images") == False:
        os.mkdir(f"{debug_output_path}/Debug/Average Images")
    
    # Location of the data path
    data_path = f"{path}/Data"
    
    # Creates a list of folders in the data directory
    os.chdir(data_path)
    folders_list = [folder for folder in os.listdir(data_path) if os.path.isdir(folder)]
    if "Key" in folders_list:
        folders_list.remove("Key")
    if len(folders_list) == 0:
        print("Error! Folders could not be found!")
        return
    
    # Declares start of motion stabilization
    print("Starting motion stabilization")
    
    # Craetes base image for motion stabilization
    base_image = base_image_creator(data_path,debug_output_path,folders_list)
    
    # Goes through each data folder
    for folder in folders_list:
        
        # Changes directory to folder
        folder_path = f"{data_path}/{folder}"
        os.chdir(folder_path)
        
        # Generates a list of data images
        files_list = [file for file in os.listdir(folder_path) if file.endswith(".tif")]
        if len(files_list) == 0:
            print("Error! Empty folder detected!")
            return
        
        # Goes through each data image and reads the data
        folder_images = [cv2.imread(file,2) for file in files_list]
        folder_images = np.array(folder_images,dtype=np.uint16)
        
        # Stabilizes motion of images
        filtered_stabilized_images = motion_stabilizer(folder,debug_output_path,base_image,folder_images,gauss_filter)
        
        # Saves images as tiff stack
        tiff.imwrite(f"{images_output_path}/{folder}.tiff",filtered_stabilized_images)
        del filtered_stabilized_images
        
        # Prints folder number for tracking
        print(f"Folder {folder}")
    
    # Declares end of data extraction
    print("Finished motion stabilization")
    
    # Creates a text file that declares end of motion stabilization
    finished = open(f"{path}/Stabilized Images/finished.txt","w")
    finished.write(f"Motion correction finished on {datetime.now()}""\n")
    finished.close()
    
    return