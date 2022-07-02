# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 19:07:55 2021

@author: Yoshi
"""

import os
import shutil
import pandas as pd



from modulation_color_key_generator import *
from modulation_index_histogram import *

def modulation_index_analysis(path,threshold,
                              modulation_cell_flags,tonotopy_cell_flags,tonotopy_extra_flag,
                              modulation_correlation_coefficients,tonotopy_correlation_coefficients,
                              modulation_areas_under_curves,tonotopy_areas_under_curves,
                              modulation_key,tonotopy_key,
                              modulation_frequencies,tonotopy_frequencies,
                              modulation_frequency_unit,tonotopy_frequency_unit,
                              modulation_intensities,tonotopy_intensities,
                              modulation_intensity_unit,tonotopy_intensity_unit,
                              tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_cell_locations,tonotopy_scale,tonotopy_radius):
    
    # Declares start of modulation index analysis
    print("Starting modulation index analysis")
    
    # Creates output directory
    modulation_index_output_path = f"{path}/Combined Analysis"
    if os.path.exists(modulation_index_output_path) == True:
        shutil.rmtree(modulation_index_output_path)
    if os.path.exists(modulation_index_output_path) == False:
        os.mkdir(modulation_index_output_path)
        os.mkdir(f"{modulation_index_output_path}/Statistics")
        os.mkdir(f"{modulation_index_output_path}/Modulation Indices")
        temporal_modulation_indices_output = f"{modulation_index_output_path}/Modulation Indices/Temporal Modulation Indices"
        os.mkdir(temporal_modulation_indices_output)
        os.mkdir(f"{temporal_modulation_indices_output}/Spreadsheets")
        spectral_modulation_indices_output = f"{modulation_index_output_path}/Modulation Indices/Spectral Modulation Indices"
        os.mkdir(spectral_modulation_indices_output)
        os.mkdir(f"{spectral_modulation_indices_output}/Spreadsheets")
    
    # Checks to make sure that intensity lists match
    if modulation_intensities == tonotopy_intensities:
        intensities = modulation_intensities
    else:
        return
    
    # Checks to make sure that number of cells match
    if len(modulation_cell_flags) != len(tonotopy_cell_flags):
        return
    cells_total = len(modulation_cell_flags)
    
    # Set up empty lists to store modulation indices in
    temporal_modulation_indices = []
    spectral_modulation_indices = []
    
    # Modify frequency list to remove unmodulated noise
    modified_frequencies_list = modulation_frequencies.copy()
    modified_frequencies_list.remove("0")
    
    # Excel spreadsheet writers
    writer_temporal = pd.ExcelWriter(f"{temporal_modulation_indices_output}/Spreadsheets/Temporal Modulation Indices Analysis.xlsx")
    writer_spectral = pd.ExcelWriter(f"{spectral_modulation_indices_output}/Spreadsheets/Spectral Modulation Indices Analysis.xlsx")
    
    # Goes through each intensity
    for intensity in intensities:
        
        # Blank lists to store data to
        temporal_modulation_cell_numbers = []
        temporal_modulation_indices_list = []
        temporal_modulation_cell_flags = []
        spectral_modulation_cell_numbers = []
        spectral_modulation_indices_list = []
        spectral_modulation_cell_flags = []
        
        # Tally number of cells
        unflagged_cells_total = 0
        unflagged_unmodulated_cells = 0
        unflagged_modulated_cells = 0
        unflagged_puretone_cells = 0
        flagged_cells_total = 0
        flagged_unmodulated_cells = 0
        flagged_modulated_cells = 0
        flagged_puretone_cells = 0
        
        # Goes through each cell
        for cell_number in range(cells_total):
            
            # Count number of cells for each type
            if modulation_cell_flags[cell_number][0] == "N/A":
                unflagged_cells_total += 1
            else:
                flagged_cells_total += 1
            
            # Checks for responsiveness to unmodulated noise and area under curve
            unmodulated_response = False
            unmodulated_sample_number = modulation_key["0"][intensity]
            if modulation_correlation_coefficients[cell_number][unmodulated_sample_number] > threshold:
                unmodulated_response = True
                if modulation_cell_flags[cell_number][0] == "N/A":
                    unflagged_unmodulated_cells += 1
                else:
                    flagged_unmodulated_cells += 1
            unmodulated_aoc = float(modulation_areas_under_curves[cell_number][unmodulated_sample_number])
            if unmodulated_aoc < 0:
                unmodulated_aoc = 0
            
            # Checks for responsiveness to modulated noise and area under curve
            modulated_response = False
            modulated_r_list = []
            modulated_aoc_list = []
            for frequency in modified_frequencies_list:
                modulated_sample_number = modulation_key[frequency][intensity]
                modulated_r_list.append(modulation_correlation_coefficients[cell_number][modulated_sample_number])
                modulated_aoc_list.append(modulation_areas_under_curves[cell_number][modulated_sample_number])
            if max(modulated_r_list) > threshold:
                modulated_response = True
                if modulation_cell_flags[cell_number][0] == "N/A":
                    unflagged_modulated_cells += 1
                else:
                    flagged_modulated_cells += 1
            modulated_aoc = float(max(modulated_aoc_list))
            if modulated_aoc < 0:
                modulated_aoc = 0
            
            # Checks for responsiveness to puretone and area under curve
            puretone_response = False
            puretone_r_list = []
            puretone_aoc_list = []
            for frequency in tonotopy_frequencies:
                puretone_sample_number = tonotopy_key[frequency][intensity]
                puretone_r_list.append(tonotopy_correlation_coefficients[cell_number][puretone_sample_number])
                puretone_aoc_list.append(tonotopy_areas_under_curves[cell_number][puretone_sample_number])
            if max(puretone_r_list) > threshold:
                puretone_response = True
                if modulation_cell_flags[cell_number][0] == "N/A":
                    unflagged_puretone_cells += 1
                else:
                    flagged_puretone_cells += 1
            puretone_aoc = float(max(puretone_aoc_list))
            if puretone_aoc < 0:
                puretone_aoc = 0
            
            # Calculates temporal modulation index and adds to list
            if unmodulated_response == True or modulated_response == True:
                temporal_modulation_cell_numbers.append(cell_number+1)
                if modulated_aoc+unmodulated_aoc != 0:
                    temporal_modulation_index = (modulated_aoc-unmodulated_aoc) / (modulated_aoc+unmodulated_aoc)
                else:
                    temporal_modulation_index = 0
                temporal_modulation_indices_list.append(temporal_modulation_index)
                temporal_modulation_cell_flags.append(modulation_cell_flags[cell_number][0])
            
            # Calculates spectral modulation index and adds to list
            if unmodulated_response == True or puretone_response == True:
                spectral_modulation_cell_numbers.append(cell_number+1)
                if puretone_aoc+unmodulated_aoc != 0:
                    spectral_modulation_index = (puretone_aoc-unmodulated_aoc) / (puretone_aoc+unmodulated_aoc)
                else:
                    spectral_modulation_index = 0
                spectral_modulation_indices_list.append(spectral_modulation_index)
                spectral_modulation_cell_flags.append(tonotopy_cell_flags[cell_number][0])
            
        # Compiles list
        temporal_modulation_indices.append([temporal_modulation_cell_numbers,temporal_modulation_cell_flags,temporal_modulation_indices_list])
        spectral_modulation_indices.append([spectral_modulation_cell_numbers,spectral_modulation_cell_flags,spectral_modulation_indices_list])
        
        # Exports statistics to excel spreadsheet
        statistics = {"Unmodulated": [unflagged_unmodulated_cells,flagged_unmodulated_cells],
                      "Modulated": [unflagged_modulated_cells,flagged_modulated_cells,],
                      "Puretone": [unflagged_puretone_cells,flagged_puretone_cells],
                      "Total": [unflagged_cells_total,flagged_cells_total]}
        statistics = pd.DataFrame(statistics,index=["Unflagged","Flagged"])
        statistics.to_excel(f"{modulation_index_output_path}/Statistics/{intensity} {modulation_intensity_unit}.xlsx")
        
    # Generates a color key for modulation indices map
    color_key = modulation_color_key_generator()
    
    # Creates histograms and maps for temporal modulation indices
    temporal_title = "Temporal Modulation Indices"
    modulation_index_histogram(temporal_modulation_indices_output,writer_temporal,temporal_modulation_indices,intensities,modulation_intensity_unit,temporal_title,tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_cell_locations,tonotopy_scale,tonotopy_radius,color_key,tonotopy_cell_flags,tonotopy_extra_flag)
    
    # Creates histograms and maps for spectral modulation indices
    spectral_title = "Spectral Modulation Indices"
    modulation_index_histogram(spectral_modulation_indices_output,writer_spectral,spectral_modulation_indices,intensities,modulation_intensity_unit,spectral_title,tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_cell_locations,tonotopy_scale,tonotopy_radius,color_key,tonotopy_cell_flags,tonotopy_extra_flag)
    
    # Close pandas writers
    writer_temporal.save()
    writer_temporal.close()
    writer_spectral.save()
    writer_spectral.close()
    
    # Declares end of modulation index analysis
    print("Finished modulation index analysis")
    
    return