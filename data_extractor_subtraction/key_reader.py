# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:32:31 2019

@author: Yoshi
"""

import csv



def key_reader(path):
    
    """
    This is the function used to read the sample key for the data. It contains
    the order (sample number) in which the combination of frequencies and
    amplitudes were used to stimulate the mouse.
    
    Parameters
    ----------
    path: The path to the parent folder of the data folder.
    
    Returns
    -------
    key: A dictionary of frequencies containing the dictionary of amplitudes
        containing the sample numbers. The sample number can be found by
        inputting the frequency, then the amplitude.
    frequencies: A list containing all of the frequencies used to stimulate the
        mouse.
    frequency_unit: A string representing the unit of frequency used to
        stimulate the mouse.
    intensities: A list containing all of the amplitudes used to stimulate the
        mouse.
    intensity_unit: A string representing the unit of amplitude used to
        stimulate the mouse.
    """
    
    # Creates a list for frequencies and intensities
    frequencies = []
    intensities = []
    
    # Creates an empty dict for the key
    key = {}
    
    # Opens key
    open_key_file = open(path)
    key_file = csv.reader(open_key_file)
    
    # Reads content of key
    row_count = 0
    for row in key_file:
        row_length = len(row)
        if row_count == 0:
            intensity_unit,frequency_unit = row[0].split('\\')
            for column in range(1,row_length):
                frequencies.append(row[column])
                key[row[column]] = {}
        else:
            for column in range(row_length):
                if column == 0:
                    intensities.append(row[column])
                else:
                    key[frequencies[column-1]][intensities[row_count-1]] = int(row[column])-1
        row_count += 1
    
    # Close file
    open_key_file.close()
    
    return key,frequencies,frequency_unit,intensities,intensity_unit