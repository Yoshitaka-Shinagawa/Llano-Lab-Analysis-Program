# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:09:08 2019

@author: Yoshi
"""

from key_reader import *
from cell_excitatory_flagger import *

def cell_flagger(path,cell_flags,key,frequencies,decibels,data):
    
    # Declares start of cell flagging
    print('Starting cell flagging')
    
    # Goes through each cell
    cell_total = data.shape[0]
    for cell_number in range(cell_total):
        
        # Finds best frequency and characteristic frequency of each cell
        best_frequency,characteristic_frequency = cell_excitatory_flagger(cell_number,data,key,frequencies,decibels)
        cell_flags[cell_number].append(best_frequency)
        cell_flags[cell_number].append(characteristic_frequency)
    
    # Declares end of cell flagging
    print('Finished cell flagging')
    
    return cell_flags