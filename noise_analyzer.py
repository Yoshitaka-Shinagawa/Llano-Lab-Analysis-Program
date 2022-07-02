# -*- coding: utf-8 -*-
"""
Created on Fri May 21 11:00:57 2021

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
os.chdir(f"{program_path}/correlation_matrix")
from correlation_matrix import *
os.chdir(f"{program_path}/debug_tools")
from r_histogram_creator import *



def noise_analyzer(path,gauss_filter="Default",threshold=0.6):
    
    # Sets mode to noise analysis
    mode = 1
    
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
    
    # Creates a correlation matrix between cells
    # correlation_matrix(path,data,cell_flags,framerate_information,extra_flag,mode)
    
    # Various debugging tools
    r_histogram_creator(path,correlation_coefficients)
    
    # Announces that analysis is finished
    print(f"Analysis finished for {path}")
    
    # Changes directory to main so deleting folders does not interfere with rerunning the program
    os.chdir(path)
    
    return



base_path = "D:/Llano Lab/Tonotopic Analysis/PCB Toxicity Data"

# noise_analyzer(f"{base_path}/Group 1/2021-05-02/A4NON Data Set 1 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-02/A4NON Data Set 2 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-16/A3NON Modulated Noise 40dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-16/A3NON Modulated Noise 50dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-16/A3NON Modulated Noise 60dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-16/A3NON Modulated Noise 70dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-16/A3NON Modulated Noise 80dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-17/A7NON S with PA Modulated Noise 40dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-17/A7NON S with PA Modulated Noise 50dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-17/A7NON S with PA Modulated Noise 60dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-17/A7NON S with PA Modulated Noise 70dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-17/A7NON S with PA Modulated Noise 80dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-30/AA8NON Modulated Noise 40dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-30/AA8NON Modulated Noise 50dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-30/AA8NON Modulated Noise 60dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-30/AA8NON Modulated Noise 70dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-05-30/AA8NON Modulated Noise 80dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-06-19/AA1NON Modulated Noise 40dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-06-19/AA1NON Modulated Noise 50dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-06-19/AA1NON Modulated Noise 60dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-06-19/AA1NON Modulated Noise 70dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 1/2021-06-19/AA1NON Modulated Noise 80dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-04-30/B1NON Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-09/B7NON Data Set 1 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-09/B7NON Data Set 2 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-10/B1NON Off-target Lateral Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 1 Modulated Noise 40dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 1 Modulated Noise 50dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 1 Modulated Noise 60dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 1 Modulated Noise 70dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 1 Modulated Noise 80dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 2 Modulated Noise 40dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 2 Modulated Noise 50dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 2 Modulated Noise 60dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 2 Modulated Noise 70dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 2/2021-05-23/BB7NON-2 Data Set 2 Modulated Noise 80dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-03/A5N Data Set 1 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-03/A5N Data Set 2 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-06/A6N Data Set 1 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-06/A6N Data Set 2 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 1 Modulated Noise 40 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 1 Modulated Noise 50 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 1 Modulated Noise 60 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 1 Modulated Noise 70 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 1 Modulated Noise 80 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 2 Modulated Noise 40 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 2 Modulated Noise 50 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 2 Modulated Noise 60 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 2 Modulated Noise 70 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 2 Modulated Noise 80 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 3 Modulated Noise 40 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 3 Modulated Noise 50 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 3 Modulated Noise 60 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 3 Modulated Noise 70 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 3/2021-05-28/AA1N Data Set 3 Modulated Noise 80 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 4/2021-04-24/B7N Data Set 1 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 4/2021-04-24/B7N Data Set 2 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 4/2021-04-27/B5N Data Set 1 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 4/2021-04-27/B5N Data Set 2 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 4/2021-05-08/B7N Data Set 1 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 4/2021-05-08/B7N Data Set 2 Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-04/A6NON Modulated Noise",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-18/BB4N Modulated Noise 50 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-18/BB4N Modulated Noise 60 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-18/BB4N Modulated Noise 70 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-18/BB4N Modulated Noise 80 dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-29/AA5NON Modulated Noise 40dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-29/AA5NON Modulated Noise 50dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-29/AA5NON Modulated Noise 60dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-29/AA5NON Modulated Noise 70dB",(2,2,2))
# noise_analyzer(f"{base_path}/Group 5/2021-05-29/AA5NON Modulated Noise 80dB",(2,2,2))


# base_path = "D:/Llano Lab/Tonotopic Analysis/Surface Tonotopy Data/5 RCAMP GAD67 Crossbreeding"

# noise_analyzer(f"{base_path}/2021-04-11/2021-04-11 Chirps")
# noise_analyzer(f"{base_path}/2021-04-11/2021-04-11 Modulated Noise")
# noise_analyzer(f"{base_path}/2021-04-18/2021-04-18 Chirps",threshold=0.4)#,True,(2,2,2))
# noise_analyzer(f"{base_path}/2021-04-18/2021-04-18 Modulated Noise",threshold=0.4)#,True,(2,2,2))
# noise_analyzer(f"{base_path}/2021-04-20/2021-04-20 Chirps",True,(2,2,2))
# noise_analyzer(f"{base_path}/2021-04-20/2021-04-20 Modulated Noise",True,(2,2,2))
# noise_analyzer(f"{base_path}/2021-04-20/2021-04-20 Mouse Voice")
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (000,000) Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (000,000) Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (058,200) Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (058,200) Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (361,088) Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (361,088) Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (570,140) Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (570,140) Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (762,173) Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (762,173) Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (853,109) Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-08/2021-06-08 (853,109) Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 000x_206z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 000x_206z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 096x_145z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 096x_145z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 208x_084z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 208x_084z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 386x_075z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 386x_075z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 519x_104z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 519x_104z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 614x_124z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 614x_124z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 700x_190z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 700x_190z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 754x_250z Chirps",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-15/2021-06-15 754x_250z Modulated Noise",True,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory 0500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory 1000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory 1500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0005",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0010",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0020",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0050",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0100",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0250",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 0500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Somatosensory Sound 1000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0005",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0010",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0020",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0050",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0100",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0250",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 0500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 1 Sound Modulation 1000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory 0500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory 1000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory 1500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0005",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0010",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0020",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0050",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0100",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0250",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 0500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Somatosensory Sound 1000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0005",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0010",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0020",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0050",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0100",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0250",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 0500",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-06-26/2021-06-26 Data Set 2 Sound Modulation 1000",False,(1,1,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 000",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 002",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 004",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 008",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 016",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 032",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 064",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 128",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-09/2021-07-09 Modulated Noise 256",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 000",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 002",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 004",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 008",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 016",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 032",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 064",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 128",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female Modulated Noise 256",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female S+S MN0",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female S+S MN0-500ms SS-500ms",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female S+S SS-500ms",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female S+S SS-500ms MN0-500ms",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female S+S SS-500ms MN0-500ms Matching",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female S+S SS-1000ms",False,(2,2,2))
# noise_analyzer(f"{base_path}/2021-07-14/2021-07-14 Injection RCAMP Neo Female S+S SS-1000ms MN0-500ms",False,(2,2,2))


