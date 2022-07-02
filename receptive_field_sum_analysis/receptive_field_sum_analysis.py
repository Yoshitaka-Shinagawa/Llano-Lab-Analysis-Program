# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 19:59:44 2022

@author: Yoshi
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



from rfs_mapper import *
os.chdir("../map_generators")
from color_key_generator import *

def receptive_field_sum_analysis(path,key,cell_flags,extra_flag,correlation_coefficients,areas_under_curves,frequencies,frequency_unit,intensities,intensity_unit,canvas,width,height,cell_locations,scale,radius,threshold):
    
    # Declares start of receptive field sum analysis
    print("Starting receptive field sum analysis")
    
    # Disable Spyder plot window
    plt.ioff()
    
    # Deletes bandwidth analysis folder if it is found
    bandwidth_output_path = f"{path}/Output/Bandwidth Analysis"
    if os.path.exists(bandwidth_output_path) == True:
        shutil.rmtree(bandwidth_output_path)
    
    # Creates and changes to output directory
    receptive_field_sum_output_path = f"{path}/Output/Receptive Field Sum Analysis"
    if os.path.exists(receptive_field_sum_output_path) == True:
        shutil.rmtree(receptive_field_sum_output_path)
    if os.path.exists(receptive_field_sum_output_path) == False:
        os.mkdir(receptive_field_sum_output_path)
        os.mkdir(f"{receptive_field_sum_output_path}/Binary")
        os.mkdir(f"{receptive_field_sum_output_path}/Binary/Histograms")
        os.mkdir(f"{receptive_field_sum_output_path}/Binary/Spreadsheets")
        os.mkdir(f"{receptive_field_sum_output_path}/Binary/Maps")
        os.mkdir(f"{receptive_field_sum_output_path}/Normal")
        os.mkdir(f"{receptive_field_sum_output_path}/Normal/Histograms")
        os.mkdir(f"{receptive_field_sum_output_path}/Normal/Spreadsheets")
        os.mkdir(f"{receptive_field_sum_output_path}/Normal/Maps")
        os.mkdir(f"{receptive_field_sum_output_path}/Responsive Frequencies")
    
    # Constants for loops
    cell_total = correlation_coefficients.shape[0]
    
    # Excel spreadsheet writers
    writer_binary = pd.ExcelWriter(f"{receptive_field_sum_output_path}/Binary/Spreadsheets/Receptive Field Sum Analysis.xlsx")
    writer_normal = pd.ExcelWriter(f"{receptive_field_sum_output_path}/Normal/Spreadsheets/Receptive Field Sum Analysis.xlsx")
    writer_fr = pd.ExcelWriter(f"{receptive_field_sum_output_path}/Responsive Frequencies/Responsive Frequencies.xlsx")
    
    # Empty lists and arrays to store data in
    cell_numbers = []
    cell_flags_list = []
    receptive_field_sums_binary = []
    receptive_field_sums_normal = []
    cell_numbers_fr = []
    cell_flags_list_fr = []
    array_fr = np.zeros((len(frequencies),cell_total))
    
    # Combined RFS analysis
    if True:
    
        # Goes through each cell
        for cell_number in range(cell_total):
            
            # Tracker for receptive field sum
            receptive_field_sum_binary = 0
            receptive_field_sum_normal = 0
            max_receptive_field = 0
            
            # Add cell numbers and flags to frequency response list
            cell_numbers_fr.append(cell_number+1)
            cell_flags_list_fr.append(cell_flags[cell_number][0])
            
            # Goes through each intensity
            for intensity in intensities:
                
                # Goes through each frequency
                for frequency_index,frequency in enumerate(frequencies):
                    
                    # Obtains sample number from key
                    sample_number = key[frequency][intensity]
                    
                    # Determines if the cell is responsive to the frequency and amplitude
                    if correlation_coefficients[cell_number][sample_number] > threshold:
                        
                        # Add one to tracker
                        receptive_field_sum_binary += 1
                        
                        # Add area under curve to tracker
                        area_under_curve = areas_under_curves[cell_number][sample_number][0]
                        receptive_field_sum_normal += area_under_curve
                        if area_under_curve > max_receptive_field:
                            max_receptive_field = area_under_curve
                        
                        # Change response to frequency to 1
                        array_fr[frequency_index,cell_number] = 1
            
            # Normalize receptive field sum
            if max_receptive_field != 0:
                receptive_field_sum_normal = receptive_field_sum_normal / max_receptive_field
            
            # If receptive field sum is not zero, store its data
            if receptive_field_sum_binary > 0:
                cell_numbers.append(cell_number+1)
                cell_flags_list.append(cell_flags[cell_number][0])
                receptive_field_sums_binary.append(receptive_field_sum_binary)
                receptive_field_sums_normal.append(receptive_field_sum_normal)
            
        # Calculate what percentage of cells were used
        percentage = round(len(cell_numbers)*100/cell_total,2)
        
        # Makes histograms, spreadsheets, and maps for binary and normal RFS
        for rfs_type in ["Binary","Normal"]:
            
            # Retrieve data
            receptive_field_sums = locals()[f"receptive_field_sums_{rfs_type.lower()}"]
            
            # Creates a histogram
            plt.hist(receptive_field_sums)
            # receptive_field_sums_mean = round(np.average(receptive_field_sums),2)
            # receptive_field_sums_standard_deviation = round(np.std(receptive_field_sums),2)
            
            # Creates a title
            plt.title(f"Receptive Field Sum\nPercentage of responsive cells: {percentage}%")
            #\nMean: {receptive_field_sums_mean}  Standard Deviation: {receptive_field_sums_standard_deviation}")
            
            # Saves the figure and closes it
            plt.savefig(f"{receptive_field_sum_output_path}/{rfs_type}/Histograms/Combined")
            plt.close()
            plt.clf()
            
            # Exports dataframe to excel spreadsheet
            dataframe = {"Cell Number":cell_numbers,"Cell Flag":cell_flags_list,"Receptive Field Sum":receptive_field_sums}
            dataframe = pd.DataFrame(dataframe)
            dataframe.to_excel(locals()[f"writer_{rfs_type.lower()}"],sheet_name="Combined",index=False)
            
            # Generates a color key for the RFS map
            rfs_steps = []
            intensity_levels = len(intensities)
            for frequency_index,frequency in enumerate(frequencies):
                rfs_steps.append((frequency_index+1)*intensity_levels)
            color_key = color_key_generator(rfs_steps)
            
            # Creates a map based on the RFS values
            map_output_path = f"{receptive_field_sum_output_path}/{rfs_type}/Maps"
            rfs_max = len(frequencies) * len(intensities)
            title = "Combined"
            rfs_mapper(map_output_path,canvas,width,height,cell_locations,scale,radius,color_key,cell_flags,extra_flag,cell_numbers,receptive_field_sums,title,rfs_max)
        
        # Exports frequency response data to excel spreadsheet
        dataframe_fr = {"Cell Number":cell_numbers_fr,"Cell Flag":cell_flags_list_fr}
        for frequency_index,frequency in enumerate(frequencies):
            dataframe_fr[f"{frequency} {frequency_unit}"] = array_fr[frequency_index]
        dataframe_fr = pd.DataFrame(dataframe_fr)
        dataframe_fr.to_excel(writer_fr,sheet_name=f"Combined",index=False)
    
    # Goes through each intensity
    for intensity in intensities:
        
        # Empty lists to store data in
        cell_numbers = []
        cell_flags_list = []
        receptive_field_sums_binary = []
        receptive_field_sums_normal = []
        array_fr = np.zeros((len(frequencies),cell_total))
        
        # Goes through each cell
        for cell_number in range(cell_total):
            
            # Tracker for receptive field sum
            receptive_field_sum_binary = 0
            receptive_field_sum_normal = 0
            max_receptive_field = 0
            
            # Goes through each frequency
            for frequency_index,frequency in enumerate(frequencies):
                
                # Obtains sample number from key
                sample_number = key[frequency][intensity]
                
                # Determines if the cell is responsive to the frequency and amplitude
                if correlation_coefficients[cell_number][sample_number] > threshold:
                    
                    # Add one to tracker
                    receptive_field_sum_binary += 1
                    
                    # Add area under curve to tracker
                    area_under_curve = areas_under_curves[cell_number][sample_number][0]
                    receptive_field_sum_normal += area_under_curve
                    if area_under_curve > max_receptive_field:
                        max_receptive_field = area_under_curve
                    
                    # Change response to frequency to 1
                    array_fr[frequency_index,cell_number] = 1
            
            # Normalize receptive field sum
            if max_receptive_field != 0:
                receptive_field_sum_normal = receptive_field_sum_normal / max_receptive_field
            
            # If receptive field sum is not zero, store its data
            if receptive_field_sum_binary > 0:
                cell_numbers.append(cell_number+1)
                cell_flags_list.append(cell_flags[cell_number][0])
                receptive_field_sums_binary.append(receptive_field_sum_binary)
                receptive_field_sums_normal.append(receptive_field_sum_normal)
        
        # Calculate what percentage of cells were used
        percentage = round(len(cell_numbers)*100/cell_total,2)
        
        # Makes histograms and export data for binary and normal
        for rfs_type in ["Binary","Normal"]:
            
            # Retrieve data
            receptive_field_sums = locals()[f"receptive_field_sums_{rfs_type.lower()}"]
            
            # Creates a histogram
            plt.hist(receptive_field_sums)
            # receptive_field_sums_mean = round(np.average(receptive_field_sums),2)
            # receptive_field_sums_standard_deviation = round(np.std(receptive_field_sums),2)
            
            # Creates a title
            plt.title(f"Receptive Field Sum\nPercentage of responsive cells: {percentage}%")
            #\nMean: {receptive_field_sums_mean}  Standard Deviation: {receptive_field_sums_standard_deviation}")
            
            # Saves the figure and closes it
            plt.savefig(f"{receptive_field_sum_output_path}/{rfs_type}/Histograms/{intensity} {intensity_unit}")
            plt.close()
            plt.clf()
            
            # Exports dataframe to excel spreadsheet
            dataframe = {"Cell Number":cell_numbers,"Cell Flag":cell_flags_list,"Receptive Field Sum":receptive_field_sums}
            dataframe = pd.DataFrame(dataframe)
            dataframe.to_excel(locals()[f"writer_{rfs_type.lower()}"],sheet_name=f"{intensity} {intensity_unit}",index=False)
            
            # Generates a color key for the RFS map
            rfs_steps = []
            for frequency_index,frequency in enumerate(frequencies):
                rfs_steps.append(frequency_index+1)
            color_key = color_key_generator(rfs_steps)
            
            # Creates a map based on the RFS values
            map_output_path = f"{receptive_field_sum_output_path}/{rfs_type}/Maps"
            rfs_max = len(frequencies)
            title = f"{intensity} {intensity_unit}"
            rfs_mapper(map_output_path,canvas,width,height,cell_locations,scale,radius,color_key,cell_flags,extra_flag,cell_numbers,receptive_field_sums,title,rfs_max)
        
        # Exports frequency response data to excel spreadsheet
        dataframe_fr = {"Cell Number":cell_numbers_fr,"Cell Flag":cell_flags_list_fr}
        for frequency_index,frequency in enumerate(frequencies):
            dataframe_fr[f"{frequency} {frequency_unit}"] = array_fr[frequency_index]
        dataframe_fr = pd.DataFrame(dataframe_fr)
        dataframe_fr.to_excel(writer_fr,sheet_name=f"{intensity} {intensity_unit}",index=False)
    
    # Close pandas writers
    writer_binary.save()
    writer_binary.close()
    writer_normal.save()
    writer_normal.close()
    writer_fr.save()
    writer_fr.close()
    
    # Declares end of receptive field sum analysis
    print("Finished receptive field sum analysis")
    
    return 