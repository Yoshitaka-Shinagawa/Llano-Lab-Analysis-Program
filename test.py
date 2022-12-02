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
from latency_response_mapper import *
os.chdir(f"{program_path}/cell_grapher")
from cell_grapher import *
os.chdir(f"{program_path}/population_analysis")
from population_analysis import *
os.chdir(f"{program_path}/receptive_field_sum_analysis")
from receptive_field_sum_analysis import *
os.chdir(f"{program_path}/correlation_matrix")
from correlation_matrix import *
os.chdir(f"{program_path}/somatosensory")
from multisensory_integration import *
from latency_map_onset import *
from latency_map_offset import * 
from onset_offset_extractor import *
from first_2_trials_extractor import *
from first_2_grapher import *
from latency_df_maker import *
# os.chdir(f"{program_path}/debug_tools")
# from r_histogram_creator import *



# path = "E:/Llano Lab/SomatoSensory/2022-10-14/RCAMP GAD67 070422/low_power/D1/For analysis/SO1"
# path = "E:/Llano Lab/SomatoSensory/2022-10-14/RCAMP GAD67 070422/low_power/D1/For analysis/SOM1"
# path = "E:/Llano Lab/SomatoSensory/2022-10-14/RCAMP GAD67 070422/low_power/D1/For analysis/OVER1"
path = "E:/Llano Lab/SomatoSensory/2022-10-14/RCAMP GAD67 070422/low_power/D2/For analysis/SO2"
# path = "E:/Llano Lab/SomatoSensory/2022-10-14/RCAMP GAD67 070422/low_power/D2/For analysis/SOM2"
# path = "E:/Llano Lab/SomatoSensory/2022-10-14/RCAMP GAD67 070422/low_power/D2/For analysis/OVER2"
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
somatosensory=1

# Sets mode, 0 for tonotopy, 1 for noise
mode = 1

# Create a class to store various information in
class info_storage:
    def __init__(self):
        self.path         = path
        self.gauss_filter = gauss_filter
        self.threshold    = threshold
        self.mode         = mode
        self.somatosensory = somatosensory

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

# Creates graphs for traces of individual cells
cell_grapher(data,tonotopy_info)

# Analyzes response of cell populations
# population_analysis(data,tonotopy_info)

# Makes an Excel Sheet of the Data 
df = multisensory_integration(data,tonotopy_info)

# Extracts the Onset and Offset of the Data across the entire time frame
data_onset,data_offset = onset_offset_extractor(data)

# Extracts the data to contain only the first two trials across the entire time
data_first_two = first_2_trials_extractor(data)

# Graphs the first 2 trials across the entire timeframe 
tonotopy_info = cell_flagger(data_first_two,tonotopy_info)
first_2_grapher(data_first_two,tonotopy_info) 

# Updates data_first_two variable to be first 2 trials of onset data
data_first_two = first_2_trials_extractor(data_onset)

# Graphs the onset_latency map of all trials 
tonotopy_info = cell_flagger(data_onset,tonotopy_info)
latency_map_onset(data_onset,tonotopy_info,1)

# Graphs the onset latency map of first two trials 
tonotopy_info = cell_flagger(data_first_two,tonotopy_info)
latency_map_onset(data_first_two,tonotopy_info,2)

# Updates data_first_two variable to be first 2 trials of offset data
data_first_two = first_2_trials_extractor(data_offset)

# Graphs the offset latency map 
tonotopy_info = cell_flagger(data_offset,tonotopy_info)
latency_map_offset(data_offset,tonotopy_info,1)

# Graphs the offset latency map of the first two trials 
tonotopy_info = cell_flagger(data_first_two,tonotopy_info)
latency_map_offset(data_first_two,tonotopy_info,2)

# Analyzes receptive field sum
# receptive_field_sum_analysis(tonotopy_info)

# Creates a correlation matrix between cells
# correlation_matrix(path,data,cell_flags,framerate_information,extra_flag,mode)

# Various debugging tools
# r_histogram_creator(tonotopy_info)

# Extracts latency data and puts it into a dataframe

# Creates a dataframe to make latency chart
tonotopy_info = latency_df_maker(tonotopy_info)

#Creates map based on latency
tonotopy_info = latency_response_mapper(tonotopy_info)

# Announces that analysis is finished
print(f"Analysis finished for {path}")

# Changes directory to main so deleting folders does not interfere with rerunning the program
os.chdir(path)

