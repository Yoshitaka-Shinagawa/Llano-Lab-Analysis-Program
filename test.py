# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:46:44 2019

@author: Yoshi
"""

import warnings
warnings.simplefilter(action="ignore",category=FutureWarning)

import os



program_path = os.getcwd()

os.chdir(f"{program_path}/motion_corrector")
from motion_corrector import *
os.chdir(f"{program_path}/data_extractor_subtraction")
from data_extractor_subtraction import *
os.chdir(f"{program_path}/cell_flagger")
from cell_flagger import *
os.chdir(f"{program_path}/map_generators")
from tonotopic_map_generator import *
os.chdir(f"{program_path}/cell_grapher")
from cell_grapher import *
os.chdir(f"{program_path}/population_analysis")
from population_analysis import *
os.chdir(f"{program_path}/receptive_field_sum_analysis")
from receptive_field_sum_analysis import *
os.chdir(f"{program_path}/correlation_matrix")
from correlation_matrix import *
os.chdir(f"{program_path}/debug_tools")
from r_histogram_creator import *
os.chdir(f"{program_path}/KClustering")
from k_clustering import *
from sample_averaging import *
from cannon_wave import *
from pair_plot import * 
from labeled_waveform_graphs import *


path = "E:/Llano Lab/Sex Difference/2022-08-24/RCAMP CBA 032722 F (+287,-006,-094)/Tonotopy"
# path = "D:/Llano Lab/Tonotopic Analysis/PCB Toxicity Data/Group 1/2021-05-02/2021-05-02 A4NON Data Set 2 Tonotopy"
# path = "D:/Llano Lab/Tonotopic Analysis/PCB Toxicity Data/Group 1/2021-05-02/2021-05-02 A4NON Data Set 1 Modulated Noise"
# path = "D:/Llano Lab/Tonotopic Analysis/PCB Toxicity Data/Group 2/2021-04-30/2021-04-30 B1NON Modulated Noise"
# path = "D:/Llano Lab/Tonotopic Analysis/Axon Imaging/2021-07-16/2021-07-16 2nd Trial CBA Mouse Tonotopy"
# path = "D:/Llano Lab/Tonotopic Analysis/Axon Imaging/2021-08-31/2021-08-31 R1 Tonotopy"
# path = "D:/Llano Lab/Tonotopic Analysis/Axon Imaging/2021-08-31/2021-08-31 R1 Modulated Noise"
# path = "D:/Llano Lab/Tonotopic Analysis/Axon Imaging/2021-08-31/2021-08-31 R2 Tonotopy"
# path = "D:/Llano Lab/Tonotopic Analysis/Module Project/2021-09-04/2021-09-04 Prism GAD67xRCAMP Data Set 1 Modulation"

gauss_filter=(2,2,2)#"Default"
threshold=0.6

# Sets mode, 0 for tonotopy, 1 for noise
mode = 0

# Create a class to store various information in
class info_storage:
    def __init__(self):
        self.path         = path
        self.gauss_filter = gauss_filter
        self.threshold    = threshold
        self.mode         = mode

# Create an instance of the class
tonotopy_info = info_storage()

# Stabilizes and filters images
raw_images,filtered_images,tonotopy_info = motion_corrector(tonotopy_info)

# Extracts the data from the images
data,tonotopy_info = data_extractor_subtraction(filtered_images,tonotopy_info)

# Flags cells based on their responsiveness
tonotopy_info = cell_flagger(data,tonotopy_info)

# Creates tonotopic map based on cell flags
tonotopy_info = tonotopic_map_generator(tonotopy_info)
# 
#Hashmaps sample averages
sample_hash,df,tonotopy_info = sample_averages(data,tonotopy_info)

#Creates cannonical waveform
df3,df2,tonotopy_info = cannon_wave(tonotopy_info)

#Creates Copy of Dataframe
df3_copy = df3

#Creates the pair plot
df4 = pair_plot(df3_copy)


#Conducts k_clustering 
df_labeled = k_clustering(df3_copy)


df_labeled_copy = df_labeled 

#Creates graphs, organized by labeled_waveform
labeled_waveform_graphs(df_labeled, df3)

# Creates graphs for traces of individual cells
# cell_grapher(data,tonotopy_info)

# Analyzes response of cell populations
# population_analysis(data,tonotopy_info)

# Analyzes receptive field sum
# receptive_field_sum_analysis(tonotopy_info)

# Creates a correlation matrix between cells
# correlation_matrix(path,data,cell_flags,framerate_information,extra_flag,mode)

# Various debugging tools
# r_histogram_creator(tonotopy_info)

# Announces that analysis is finished
# print(f"Analysis finished for {path}")

# Changes directory to main so deleting folders does not interfere with rerunning the program
os.chdir(path)

