# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:09:08 2019

@author: Yoshi
"""

from correlation_calculator import *
from area_calculator import *
from cell_excitatory_flagger import *
from cell_noise_flagger import *

def cell_flagger(path,cell_flags,key,frequencies,intensities,data,framerate_information,mode=0,threshold="Default"):
    
    # Declares start of cell flagging
    print("Starting cell flagging")
    
    # Calculates average correlation coefficients for each sample
    correlation_coefficients = correlation_calculator(data)
    
    # Calculates area under ccurve for each sample
    areas_under_curves = area_calculator(data,framerate_information)
    
    # Excitatory cell flagging
    if mode == 0:
        
        # Goes through each cell
        cell_total = data.shape[0]
        for cell_number in range(cell_total):
            
            # Finds best frequency and characteristic frequency of each cell
            best_frequency,characteristic_frequency = cell_excitatory_flagger(cell_number,correlation_coefficients,areas_under_curves,
                                                                              data,key,frequencies,intensities,threshold)
            cell_flags[cell_number].append(best_frequency)
            cell_flags[cell_number].append(characteristic_frequency)
    
    # Noise cell flagging
    if mode == 1:
        
        # Goes through each cell
        cell_total = data.shape[0]
        for cell_number in range(cell_total):
            
            # Determines if the cell is responsive to noise
            noise = cell_noise_flagger(cell_number,correlation_coefficients,threshold)
            cell_flags[cell_number].append("N/A")
            cell_flags[cell_number].append("N/A")
            cell_flags[cell_number].append(noise)
    
    # Declares end of cell flagging
    print("Finished cell flagging")
    
    return cell_flags,correlation_coefficients,areas_under_curves