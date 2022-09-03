# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:46:44 2019

@author: Yoshi
"""

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



def tonotopy_analyzer(path,gauss_filter="Default",threshold=0.6):
    
    # Sets mode to new tonotopy analysis
    mode = 0
    
    # Stabilizes and filters images
    raw_images,filtered_images,folders_list = motion_corrector(path,gauss_filter,mode)
    
    # Extracts the data from the images
    extra_flag,cell_locations,cell_flags,data,framerate_information,key,frequencies,frequency_unit,intensities,intensity_unit = data_extractor_subtraction(path,filtered_images,folders_list,mode)
    
    # Flags cells based on their responsiveness
    cell_flags,correlation_coefficients,areas_under_curves = cell_flagger(path,cell_flags,key,frequencies,intensities,data,framerate_information,mode,threshold)
    
    # Creates tonotopic map based on cell flags
    canvas,width,height,scale,radius = tonotopic_map_generator(path,cell_locations,frequencies,frequency_unit,cell_flags,extra_flag,mode)
    
    # Creates graphs for traces of individual cells
    cell_grapher(path,data,cell_flags,correlation_coefficients,areas_under_curves,framerate_information,key,frequencies,frequency_unit,intensities,intensity_unit,mode,threshold)
    
    # Analyzes response of cell populations
    population_analysis(path,data,cell_flags,framerate_information,key,frequencies,frequency_unit,intensities,intensity_unit,extra_flag,mode)
    
    # Analyzes receptive field sum
    receptive_field_sum_analysis(path,key,cell_flags,extra_flag,correlation_coefficients,areas_under_curves,frequencies,frequency_unit,intensities,intensity_unit,canvas,width,height,cell_locations,scale,radius,threshold)
    
    # Creates a correlation matrix between cells
    # correlation_matrix(path,data,cell_flags,framerate_information,extra_flag,mode)
    
    # Various debugging tools
    r_histogram_creator(path,correlation_coefficients)
    
    # Announces that analysis is finished
    print(f"Analysis finished for {path}")
    
    # Changes directory to main so deleting folders does not interfere with rerunning the program
    os.chdir(path)
    
    return


# tonotopy_analyzer("D:/Llano Lab/Tonotopic Analysis/Noise Exposure",(2,2,2))


base_path = "E:/Llano Lab/Sex Difference (Austin)/2022-09-02/RCAMP CBA 022822 (+000,+000,-196)/Tonotopy"

tonotopy_analyzer(f"{base_path}")


# base_path = "D:/Llano Lab/Tonotopic Analysis/Axon Imaging"

# tonotopy_analyzer(f"{base_path}/2021-09-03/2021-09-03 CBA Axons Modulation",(2,2,2))
# tonotopy_analyzer(f"{base_path}/2021-09-03/2021-09-03 CBA Axons Tonotopy",(2,2,2))


# base_path = "D:/Llano Lab/Tonotopic Analysis/PCB Toxicity Data"

# tonotopy_analyzer(f"{base_path}/Group 1/2021-05-02/A4NON Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 1/2021-05-02/A4NON Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 1/2021-05-04/A6NON Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 1/2021-05-16/A3NON Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 1/2021-05-17/A7NON S with PA Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 1/2021-05-30/AA8NON Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 1/2021-06-19/AA1NON Tonotopy",(2,2,2))

# tonotopy_analyzer(f"{base_path}/Group 2/2021-04-30/B1NON Tonotopic",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 2/2021-05-09/B7NON Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 2/2021-05-09/B7NON Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 2/2021-05-10/B1NON Off-target Lateral Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 2 Tonotopy",(2,2,2))

# tonotopy_analyzer(f"{base_path}/Group 3/2021-05-03/A5N Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 3/2021-05-03/A5N Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 3/2021-05-06/A6N Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 3/2021-05-06/A6N Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 3 Tonotopy",(2,2,2))

# tonotopy_analyzer(f"{base_path}/Group 4/2021-04-24/B7N Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 4/2021-04-24/B7N Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 4/2021-04-27/B5N Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 4/2021-04-27/B5N Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 4/2021-05-08/B7N Data Set 1 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 4/2021-05-08/B7N Data Set 2 Tonotopy",(2,2,2))
# tonotopy_analyzer(f"{base_path}/Group 4/2021-05-18/BB4N Tonotopy",(2,2,2))

# tonotopy_analyzer(f"{base_path}/Group 5/2021-05-29/AA5NON Tonotopy",(2,2,2))


# base_path = "D:/Llano Lab/Tonotopic Analysis/Surface Tonotopy Data/5 RCAMP GAD67 Crossbreeding"

# tonotopy_analyzer(f"{base_path}/2021-04-11/2021-04-11 Tonotopy")
# tonotopy_analyzer(f"{base_path}/2021-04-18/2021-04-18 Tonotopy",True,(2,2,2))
# tonotopy_analyzer(f"{base_path}/2021-04-20/2021-04-20 Tonotopy",threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-01/2021-06-01 000dy_022z Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-01/2021-06-01 300dy_066z Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-01/2021-06-01 382dy_100z Tonotopy",False,(1,1,2),threshold=0.75)
# tonotopy_analyzer(f"{base_path}/2021-06-01/2021-06-01 513dy_200z Tonotopy",False,(2,2,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-08/2021-06-08 (000,000) Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-08/2021-06-08 (058,200) Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-08/2021-06-08 (361,088) Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-08/2021-06-08 (570,140) Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-08/2021-06-08 (762,173) Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-08/2021-06-08 (853,109) Tonotopy",False,(1,1,2),threshold=0.6)
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 000x_206z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 096x_145z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 208x_084z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 386x_075z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 519x_104z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 614x_124z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 700x_190z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-15/2021-06-15 754x_250z Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Tonotopy",False,(1,1,2))
# tonotopy_analyzer(f"{base_path}/2021-07-09/2021-07-09 Tonotopy",False,(2,2,2))
# tonotopy_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Tonotopy",True,(2,2,2))

# base_path = "D:/Llano Lab/Tonotopic Analysis/Surface Tonotopy Data/4 Collection Improvement"

# tonotopy_analyzer(f"{base_path}/2021-01-17/2021-01-17 Lateral Surface")
# tonotopy_analyzer(f"{base_path}/2021-01-26/2021-01-26 Before Noise Exposure")
# tonotopy_analyzer(f"{base_path}/2021-01-26/2021-01-26 After Noise Exposure")
# tonotopy_analyzer(f"{base_path}/2021-02-06/2021-02-06 Lateral Surface at 22μm")
# tonotopy_analyzer(f"{base_path}/2021-02-06/2021-02-06 Lateral Surface at 39μm")


# base_path = "D:/Llano Lab/Tonotopic Analysis/Surface Tonotopy Data/1 Experimentation"

# tonotopy_analyzer(f"{base_path}/2019-07-18/2019-07-18 Anesthetized IC Area 1")


# base_path = "D:/Llano Lab/Miscellaneous/Single Photon Calcium Imaging"

# tonotopy_analyzer(f"{base_path}/2018-02-07")
# tonotopy_analyzer(f"{base_path}/2018-02-10")
# tonotopy_analyzer(f"{base_path}/2018-02-13")
# tonotopy_analyzer(f"{base_path}/2018-02-19")
# tonotopy_analyzer(f"{base_path}/2018-02-19 V")
# tonotopy_analyzer(f"{base_path}/2018-05-10")
# tonotopy_analyzer(f"{base_path}/2018-08-06")
