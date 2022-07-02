# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:37:29 2021

@author: Yoshi
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.ndimage import gaussian_filter



from base_image_creator import *
from xyz_gaussian_filter import *

path = "D:/Llano Lab/Tonotopic Analysis/Axon Imaging/2021-07-16/2021-07-16 2nd Trial CBA Mouse Tonotopy"
data_path = f"{path}/Data"

os.chdir(data_path)
folders_list = [folder for folder in os.listdir(data_path) if os.path.isdir(folder)]

if "Key" in folders_list:
    folders_list.remove("Key")

folder_averages = []
for folder in folders_list:
    folder_images = []
    folder_path = f"{data_path}/{folder}"
    os.chdir(folder_path)
    files_list = [file for file in os.listdir(folder_path) if file.endswith(".tif")]
    for file in files_list:
        folder_images.append(cv2.imread(file,2))
    folder_images = np.array(folder_images,dtype=np.float32)
    folder_average = np.average(folder_images,axis=0)
    folder_average = np.around(folder_average)
    folder_average = folder_average.astype(np.uint16)
    folder_averages.append(folder_average)
folder_averages = np.array(folder_averages,dtype=np.float32)
base_image_no_filter = np.average(folder_averages,axis=0)
base_image = gaussian_filter(base_image_no_filter,sigma=(2,2),mode="nearest")
base_image = base_image/256
base_image = np.around(base_image)
base_image = base_image.astype(np.uint8)

folder = folders_list[0]
folder_path = f"{data_path}/{folder}"
os.chdir(folder_path)
files_list = [file for file in os.listdir(folder_path) if file.endswith(".tif") and "Ch1" in file]

folder_images = [cv2.imread(file,2) for file in files_list]
folder_images = np.array(folder_images,dtype=np.float32)

folder_average = np.average(folder_images,axis=0)
folder_average = folder_average*(256/np.amax(folder_average))
folder_average = np.around(folder_average)
folder_average = folder_average.astype(np.uint8)
