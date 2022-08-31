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

def modulation_index_analysis(path,modulation_info,tonotopy_info):
    
    """
    This is the function used to calculate the temporal and spectral modulation
    index for each cell and creates a map and histogram, then exports the data
    to an Excel spreadsheet. The temporal modulation index is calculated using
    the formula temporal_modulation_index = (modulated_aoc-unmodulated_aoc) /
    (modulated_aoc+unmodulated_aoc), where modulated_aoc is the area under the
    curve of the most responsive modulated noise stimulus and unmodulated_aoc
    is the area under the curve of the unmodulated noise stimulus. The spectral
    modulation index is calculated using the formula spectral_modulation_index
    = (puretone_aoc-unmodulated_aoc) / (puretone_aoc+unmodulated_aoc), where
    puretone_aoc is the area under the curve of the most responsive puretone
    stimulus and unmodulated_aoc is the area under the curve of the unmodulated
    noise stimulus. The function first checks to see if the cell is responsive
    to modulated noise, unmodulated noise, and puretone noise before
    calculating the temporal and spectral modulation indices. It then exports
    all of the data to anExcel spreadsheet, creates a histogram for the
    modulation indices of the cells, and creates a map depicting the location
    of the cell and their modulation indices value.
    
    Parameters
    ----------
    path : The path to the parent folder of the modulation data and tonotopy
        data.
    modulation_info : The class used to store most of the variables for the
        modulation data that are used in the analysis program.
    tonotopy_info : The class used to store most of the variables for the
        tonotopy data that are used in the analysis program.
    
    Returns
    -------
    none
    """
    
    # Extracts variables from the info_storage class
    threshold                  = tonotopy_info.threshold
    intensity_unit             = tonotopy_info.intensity_unit
    m_cell_flags               = modulation_info.cell_flags
    m_correlation_coefficients = modulation_info.correlation_coefficients
    m_areas_under_curves       = modulation_info.areas_under_curves
    m_key                      = modulation_info.key
    m_frequencies              = modulation_info.frequencies
    m_intensities              = modulation_info.intensities
    t_cell_flags               = tonotopy_info.cell_flags
    t_correlation_coefficients = tonotopy_info.correlation_coefficients
    t_areas_under_curves       = tonotopy_info.areas_under_curves
    t_key                      = tonotopy_info.key
    t_frequencies              = tonotopy_info.frequencies
    t_intensities              = tonotopy_info.intensities
    
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
        temporal_modulation_indices_output = \
            f"{modulation_index_output_path}"+\
            "/Modulation Indices/Temporal Modulation Indices"
        os.mkdir(temporal_modulation_indices_output)
        os.mkdir(f"{temporal_modulation_indices_output}/Spreadsheets")
        spectral_modulation_indices_output = \
            f"{modulation_index_output_path}"+\
            "/Modulation Indices/Spectral Modulation Indices"
        os.mkdir(spectral_modulation_indices_output)
        os.mkdir(f"{spectral_modulation_indices_output}/Spreadsheets")
    
    # Checks to make sure that intensity lists match
    if m_intensities == t_intensities:
        intensities = m_intensities
    else:
        return
    
    # Checks to make sure that number of cells match
    if len(m_cell_flags) != len(t_cell_flags):
        return
    cells_total = len(m_cell_flags)
    
    # Set up empty lists to store modulation indices in
    temporal_modulation_indices = []
    spectral_modulation_indices = []
    
    # Modify frequency list to remove unmodulated noise
    modified_frequencies_list = m_frequencies.copy()
    modified_frequencies_list.remove("0")
    
    # Excel spreadsheet writers
    writer_temporal = pd.ExcelWriter(f"{temporal_modulation_indices_output}"+
        "/Spreadsheets/Temporal Modulation Indices Analysis.xlsx")
    writer_spectral = pd.ExcelWriter(f"{spectral_modulation_indices_output}"+
        "/Spreadsheets/Spectral Modulation Indices Analysis.xlsx")
    
    # Goes through each intensity
    for intensity in intensities:
        
        # Blank lists to store data to
        temporal_modulation_cell_numbers = []
        temporal_modulation_indices_list = []
        temporal_m_cell_flags = []
        spectral_modulation_cell_numbers = []
        spectral_modulation_indices_list = []
        spectral_m_cell_flags = []
        
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
            if m_cell_flags[cell_number][0] == "N/A":
                unflagged_cells_total += 1
            else:
                flagged_cells_total += 1
            
            # Checks for responsiveness to unmodulated noise and area under
            # curve
            unmodulated_response = False
            unmodulated_sample_number = m_key["0"][intensity]
            if m_correlation_coefficients[cell_number][
                unmodulated_sample_number] > threshold:
                unmodulated_response = True
                if m_cell_flags[cell_number][0] == "N/A":
                    unflagged_unmodulated_cells += 1
                else:
                    flagged_unmodulated_cells += 1
            unmodulated_aoc = float(m_areas_under_curves[cell_number][
                unmodulated_sample_number])
            if unmodulated_aoc < 0:
                unmodulated_aoc = 0
            
            # Checks for responsiveness to modulated noise and area under curve
            modulated_response = False
            modulated_r_list = []
            modulated_aoc_list = []
            for frequency in modified_frequencies_list:
                modulated_sample_number = m_key[frequency][intensity]
                modulated_r_list.append(m_correlation_coefficients[cell_number]
                                        [modulated_sample_number])
                modulated_aoc_list.append(m_areas_under_curves[cell_number][
                    modulated_sample_number])
            if max(modulated_r_list) > threshold:
                modulated_response = True
                if m_cell_flags[cell_number][0] == "N/A":
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
            for frequency in t_frequencies:
                puretone_sample_number = t_key[frequency][intensity]
                puretone_r_list.append(t_correlation_coefficients[cell_number][
                    puretone_sample_number])
                puretone_aoc_list.append(t_areas_under_curves[cell_number][
                    puretone_sample_number])
            if max(puretone_r_list) > threshold:
                puretone_response = True
                if m_cell_flags[cell_number][0] == "N/A":
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
                    temporal_modulation_index = \
                        (modulated_aoc-unmodulated_aoc) / \
                        (modulated_aoc+unmodulated_aoc)
                else:
                    temporal_modulation_index = 0
                temporal_modulation_indices_list.append(
                    temporal_modulation_index)
                temporal_m_cell_flags.append(m_cell_flags[cell_number][0])
            
            # Calculates spectral modulation index and adds to list
            if unmodulated_response == True or puretone_response == True:
                spectral_modulation_cell_numbers.append(cell_number+1)
                if puretone_aoc+unmodulated_aoc != 0:
                    spectral_modulation_index = \
                        (puretone_aoc-unmodulated_aoc) / \
                        (puretone_aoc+unmodulated_aoc)
                else:
                    spectral_modulation_index = 0
                spectral_modulation_indices_list.append(
                    spectral_modulation_index)
                spectral_m_cell_flags.append(t_cell_flags[cell_number][0])
            
        # Compiles list
        temporal_modulation_indices.append([temporal_modulation_cell_numbers,
                                            temporal_m_cell_flags,
                                            temporal_modulation_indices_list])
        spectral_modulation_indices.append([spectral_modulation_cell_numbers,
                                            spectral_m_cell_flags,
                                            spectral_modulation_indices_list])
        
        # Exports statistics to excel spreadsheet
        statistics = {"Unmodulated": [unflagged_unmodulated_cells,
                                      flagged_unmodulated_cells],
                      "Modulated": [unflagged_modulated_cells,
                                    flagged_modulated_cells],
                      "Puretone": [unflagged_puretone_cells,
                                   flagged_puretone_cells],
                      "Total": [unflagged_cells_total,flagged_cells_total]}
        statistics = pd.DataFrame(statistics,index=["Unflagged","Flagged"])
        statistics.to_excel(f"{modulation_index_output_path}/Statistics/"+
                            f"{intensity} {intensity_unit}.xlsx")
        
    # Generates a color key for modulation indices map
    color_key = modulation_color_key_generator()
    
    # Creates histograms and maps for temporal modulation indices
    temporal_title = "Temporal Modulation Indices"
    modulation_index_histogram(temporal_modulation_indices_output,
                               writer_temporal,temporal_modulation_indices,
                               temporal_title,color_key,tonotopy_info)
    
    # Creates histograms and maps for spectral modulation indices
    spectral_title = "Spectral Modulation Indices"
    modulation_index_histogram(spectral_modulation_indices_output,
                               writer_spectral,spectral_modulation_indices,
                               spectral_title,color_key,tonotopy_info)
    
    # Close pandas writers
    writer_temporal.save()
    writer_temporal.close()
    writer_spectral.save()
    writer_spectral.close()
    
    # Declares end of modulation index analysis
    print("Finished modulation index analysis")
    
    return