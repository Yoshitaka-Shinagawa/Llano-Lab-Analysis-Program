# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 18:44:08 2021

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
os.chdir(f"{program_path}/modulation_index_analysis")
from modulation_index_analysis import *



path = "D:/Llano Lab/Tonotopic Analysis/Module Project/Prism View/2021-10-14/GAD67 neo RCAMP"

gauss_filter=(2,2,2)#"Default"
threshold=0.6
mode = 0

# Create a class to store various information in
class info_storage:
    def __init__(self):
        self.gauss_filter = gauss_filter
        self.threshold    = threshold
        self.mode         = mode



# Create an instance of the class
# modulation_info = info_storage()

# Modulation Analysis
# modulation_info.path = f"{path}/Modulation"

# Stabilizes and filters images
# m_raw_images,m_filtered_images,modulation_info = motion_corrector(modulation_info)

# Extracts the data from the images
# m_data,modulation_info = data_extractor_subtraction(m_filtered_images,modulation_info)

# Flags cells based on their responsiveness
# modulation_info = cell_flagger(m_data,modulation_info)

# Creates tonotopic map based on cell flags
# modulation_info = tonotopic_map_generator(modulation_info)

# Creates graphs for traces of individual cells
# cell_grapher(m_data,modulation_info)

# Analyzes response of cell populations
# population_analysis(m_data,modulation_info)

# Creates a correlation matrix between cells
# correlation_matrix(modulation_path,modulation_data,modulation_cell_flags,modulation_framerate_information,modulation_extra_flag,mode)

# Various debugging tools
# r_histogram_creator(modulation_info)



# Create an instance of the class
# tonotopy_info = info_storage()

# Tonotopy Analysis
# tonotopy_info.path = f"{path}/Tonotopy"

# Stabilizes and filters images
# t_raw_images,t_filtered_images,tonotopy_info = motion_corrector(tonotopy_info)

# Extracts the data from the images
# t_data,tonotopy_info = data_extractor_subtraction(t_filtered_images,tonotopy_info)

# Flags cells based on their responsiveness
# tonotopy_info = cell_flagger(t_data,tonotopy_info)

# Creates tonotopic map based on cell 
# tonotopy_info = tonotopic_map_generator(tonotopy_info)

# Creates graphs for traces of individual cells
# cell_grapher(t_data,tonotopy_info)

# Analyzes response of cell populations
# population_analysis(t_data,tonotopy_info)

# Analyzes receptive field sum
# receptive_field_sum_analysis(tonotopy_info)

# Creates a correlation matrix between cells
# correlation_matrix(tonotopy_path,tonotopy_data,tonotopy_cell_flags,tonotopy_framerate_information,tonotopy_extra_flag,mode)

# Various debugging tools
# r_histogram_creator(tonotopy_info)



# Performs combined analysis of tonotopy and modulation
modulation_index_analysis(path,modulation_info,tonotopy_info)


# Announces that analysis is finished
print(f"Analysis finished for {path}")

# Changes directory to main so deleting folders does not interfere with rerunning the program
os.chdir(path)

