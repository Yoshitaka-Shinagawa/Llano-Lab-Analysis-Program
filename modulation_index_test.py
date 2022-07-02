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



# Modulation Analysis
modulation_path = f"{path}/Modulation"

# Stabilizes and filters images
modulation_raw_images,modulation_filtered_images,modulation_folders_list = motion_corrector(modulation_path,gauss_filter,mode)

# Extracts the data from the images
modulation_extra_flag,modulation_cell_locations,modulation_cell_flags,modulation_data,modulation_framerate_information,modulation_key,modulation_frequencies,modulation_frequency_unit,modulation_intensities,modulation_intensity_unit = data_extractor_subtraction(modulation_path,modulation_filtered_images,modulation_folders_list,mode)

# Flags cells based on their responsiveness
modulation_cell_flags,modulation_correlation_coefficients,modulation_areas_under_curves = cell_flagger(modulation_path,modulation_cell_flags,modulation_key,modulation_frequencies,modulation_intensities,modulation_data,modulation_framerate_information,mode,threshold)

# Creates tonotopic map based on cell flags
# modulation_canvas,modulation_width,modulation_height,modulation_scale,modulation_radius = tonotopic_map_generator(modulation_path,modulation_cell_locations,modulation_frequencies,modulation_frequency_unit,modulation_cell_flags,modulation_extra_flag,mode)

# Creates graphs for traces of individual cells
# cell_grapher(modulation_path,modulation_data,modulation_cell_flags,modulation_correlation_coefficients,modulation_areas_under_curves,modulation_framerate_information,modulation_key,modulation_frequencies,modulation_frequency_unit,modulation_intensities,modulation_intensity_unit,mode)

# Analyzes response of cell populations
# population_analysis(modulation_path,modulation_data,modulation_cell_flags,modulation_framerate_information,modulation_key,modulation_frequencies,modulation_frequency_unit,modulation_intensities,modulation_intensity_unit,modulation_extra_flag,mode)

# Creates a correlation matrix between cells
# correlation_matrix(modulation_path,modulation_data,modulation_cell_flags,modulation_framerate_information,modulation_extra_flag,mode)

# Various debugging tools
# r_histogram_creator(modulation_path,modulation_correlation_coefficients)



# Tonotopy Analysis
tonotopy_path = f"{path}/Tonotopy"

# Stabilizes and filters images
tonotopy_raw_images,tonotopy_filtered_images,tonotopy_folders_list = motion_corrector(tonotopy_path,gauss_filter,mode)

# Extracts the data from the images
tonotopy_extra_flag,tonotopy_cell_locations,tonotopy_cell_flags,tonotopy_data,tonotopy_framerate_information,tonotopy_key,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit = data_extractor_subtraction(tonotopy_path,tonotopy_filtered_images,tonotopy_folders_list,mode)

# Flags cells based on their responsiveness
tonotopy_cell_flags,tonotopy_correlation_coefficients,tonotopy_areas_under_curves = cell_flagger(tonotopy_path,tonotopy_cell_flags,tonotopy_key,tonotopy_frequencies,tonotopy_intensities,tonotopy_data,tonotopy_framerate_information,mode,threshold)

# Creates tonotopic map based on cell flags
tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_scale,tonotopy_radius = tonotopic_map_generator(tonotopy_path,tonotopy_cell_locations,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_cell_flags,tonotopy_extra_flag,mode)

# Creates graphs for traces of individual cells
# cell_grapher(tonotopy_path,tonotopy_data,tonotopy_cell_flags,tonotopy_correlation_coefficients,tonotopy_areas_under_curves,tonotopy_framerate_information,tonotopy_key,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit,mode)

# Analyzes response of cell populations
population_analysis(tonotopy_path,tonotopy_data,tonotopy_cell_flags,tonotopy_framerate_information,tonotopy_key,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit,tonotopy_extra_flag,mode)

# Analyzes receptive field sum
# receptive_field_sum_analysis(tonotopy_path,tonotopy_key,tonotopy_cell_flags,tonotopy_extra_flag,tonotopy_correlation_coefficients,tonotopy_areas_under_curves,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit,tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_cell_locations,tonotopy_scale,tonotopy_radius,threshold)

# Creates a correlation matrix between cells
# correlation_matrix(tonotopy_path,tonotopy_data,tonotopy_cell_flags,tonotopy_framerate_information,tonotopy_extra_flag,mode)

# Various debugging tools
# r_histogram_creator(tonotopy_path,tonotopy_correlation_coefficients)



# Performs combined analysis of tonotopy and modulation
# modulation_index_analysis(path,threshold,modulation_cell_flags,tonotopy_cell_flags,tonotopy_extra_flag,modulation_correlation_coefficients,tonotopy_correlation_coefficients,modulation_areas_under_curves,tonotopy_areas_under_curves,modulation_key,tonotopy_key,modulation_frequencies,tonotopy_frequencies,modulation_frequency_unit,tonotopy_frequency_unit,modulation_intensities,tonotopy_intensities,modulation_intensity_unit,tonotopy_intensity_unit,tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_cell_locations,tonotopy_scale,tonotopy_radius)


# Announces that analysis is finished
print(f"Analysis finished for {path}")

# Changes directory to main so deleting folders does not interfere with rerunning the program
os.chdir(path)

