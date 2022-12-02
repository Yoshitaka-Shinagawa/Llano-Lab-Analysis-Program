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


def tonotopy_analyzer(path,gauss_filter="Default",threshold=0.6,somatosensory=1):
    
    """
    This is the main analysis program for analyzing tonotpy for 2p data. It
    automatically stabilizes, filters, and analyzes images, and creates visuals
    that make interpretation of data easier, as well as Excel spreadsheets that
    output data for statistical analyses.
    
    Parameters
    ----------
    path : The path to the parent folder of the data folder. If running on
        Windows, ensure that all "\" are replaced with "/" to avoid escape
        characters.
    gauss_filter : The sigma values for the gaussian filter that will be used
        to filter the data. It is a tuple of three positive floats/integers,
        (x,y,z), where x is the sigma value for the up-down axis, y is the
        sigma value for the left-right axis, and z is the sigma value in the
        temporal axis. Use the lowest value where noise is eliminated, as high
        values will result in artifacts. If left unspecified, default values
        based on the resolution and frequency of the image will be used.
    threshold : The threshold for the average correlation coefficient used to
        determine whether a cell is responsive to a particular combination
        of frequencies and amplitudes. It is a float value between 0 and 1. Use
        the highest possible value where visual inspection of the graph results
        in as little false positives as possible without false negatives, but
        should be above 0.5 if possible. If left unspecified, 0.6 will be used
        as the threshold.
    
    Returns
    -------
    none
    """
    
    # Sets mode to new tonotopy analysis
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
    population_analysis(data,tonotopy_info)
    
    # Analyzes receptive field sum
    # receptive_field_sum_analysis(tonotopy_info)
    
    # Creates a correlation matrix between cells
    # correlation_matrix(path,data,cell_flags,framerate_information,extra_flag,mode)
    
    # Various debugging tools
    # r_histogram_creator(tonotopy_info)
    
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

    # Creates a dataframe to make latency chart
    tonotopy_info = latency_df_maker(tonotopy_info)
    
    #Creates map based on latency
    tonotopy_info = latency_response_mapper(tonotopy_info)
    
    # Announces that analysis is finished
    print(f"Analysis finished for {path}")
    
    # Changes directory to main so deleting folders does not interfere with rerunning the program
    os.chdir(path)
    
    return


base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/101422_RCAMPxgad67_070422_SOMATO_side/Somato_HP/D1/For analysis"

# tonotopy_analyzer(f'{base_path}/OVER1',(2,2,2),somatosensory=1) #green 120
tonotopy_analyzer(f'{base_path}/SO1',(2,2,2),somatosensory=2) #yellow 60
tonotopy_analyzer(f'{base_path}/SOM1',(2,2,2),somatosensory=3) #light blue 240 lower saturation

base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/101422_RCAMPxgad67_070422_SOMATO_side/Somato_LP/D1/For analysis"

tonotopy_analyzer(f'{base_path}/OVER1',(2,2,2),somatosensory=1)
tonotopy_analyzer(f'{base_path}/SO1',(2,2,2),somatosensory=2)
tonotopy_analyzer(f'{base_path}/SOM1',(2,2,2),somatosensory=3)

base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/101422_RCAMPxgad67_070422_SOMATO_side/Somato_LP/D2/For analysis"

tonotopy_analyzer(f'{base_path}/OVER2',(2,2,2),somatosensory=1)
tonotopy_analyzer(f'{base_path}/SO2',(2,2,2),somatosensory=2)
tonotopy_analyzer(f'{base_path}/SOM2',(2,2,2),somatosensory=3)

base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/102222_RCAMPxgad67_070422_SOMATO_side/Somato_LP/D1/For analysis"

tonotopy_analyzer(f'{base_path}/OVER1',(2,2,2),somatosensory=1)
tonotopy_analyzer(f'{base_path}/SO1_2',(2,2,2),somatosensory=2)
tonotopy_analyzer(f'{base_path}/SOM1_2',(2,2,2),somatosensory=3)

base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/102222_RCAMPxgad67_070422_SOMATO_side/Somato_LP/D3/For analysis"

tonotopy_analyzer(f'{base_path}/OVER3',(2,2,2),somatosensory=1)
tonotopy_analyzer(f'{base_path}/SO3',(2,2,2),somatosensory=2)
tonotopy_analyzer(f'{base_path}/SOM3',(2,2,2),somatosensory=3)

base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/102422_RCAMPxgad67_070422_SOMATO_side_20%/Somato_LP/D1/For analysis"

tonotopy_analyzer(f'{base_path}/OVER1',(2,2,2),somatosensory=1)
tonotopy_analyzer(f'{base_path}/SO1',(2,2,2),somatosensory=2)
tonotopy_analyzer(f'{base_path}/SOM1_2',(2,2,2),somatosensory=3)

base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/110222_RCAMPxgad67_081522_SOMATO_side/Somato_LP/D1/For analysis"

tonotopy_analyzer(f'{base_path}/OVER1',(2,2,2),somatosensory=1)
tonotopy_analyzer(f'{base_path}/SO1',(2,2,2),somatosensory=2)
tonotopy_analyzer(f'{base_path}/SOM1',(2,2,2),somatosensory=3)

base_path = "E:/Llano Lab/SomatoSensory/2022-11-23/110222_RCAMPxgad67_081522_SOMATO_side/Somato_LP/D2/For analysis"

tonotopy_analyzer(f'{base_path}/OVER2',(2,2,2),somatosensory=1)
tonotopy_analyzer(f'{base_path}/SO2',(2,2,2),somatosensory=2)
tonotopy_analyzer(f'{base_path}/SOM2_1',(2,2,2),somatosensory=3)

# tonotopy_analyzer("D:/Llano Lab/Tonotopic Analysis/Noise Exposure",(2,2,2))


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