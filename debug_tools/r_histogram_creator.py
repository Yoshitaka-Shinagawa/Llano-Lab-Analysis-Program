# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:26:23 2020

@author: Yoshi
"""

import os
import shutil
import matplotlib.pyplot as plt



def r_histogram_creator(info_storage):
    
    """
    This is the debug function used to create a histogram of the correlation
    coefficients for the data set. The histogram allows users to determine how
    responsive the cells were overall at a glance. If all of the correlation
    coefficients are gathered around 0, it means that the cells were
    unreponsive or the SNR was too low for the signal to be detectable, but if
    the correlation coefficients are trailing towards 1, then it means at least
    some of the cells were responsive.
    
    Parameters
    ----------
    info_storage : The class used to store most of the variables that are used
        in the analysis program.
    
    Returns
    -------
    none
    """
    
    # Extracts variables from the info_storage class
    path                     = info_storage.path
    correlation_coefficients = info_storage.correlation_coefficients
    
    # Creates and changes to output directory
    graph_output_path = path + "/Output/Debug/Histograms"
    if os.path.exists(graph_output_path) == True:
        shutil.rmtree(graph_output_path)
    if os.path.exists(graph_output_path) == False:
        os.mkdir(graph_output_path)
    os.chdir(graph_output_path)
    
    # Empty list for storing all correlation coefficients in
    correlation_coefficient_list = []
    
    # Goes through each cell and sample to add correlation coefficient to list
    cells = correlation_coefficients.shape[0]
    samples = correlation_coefficients.shape[1]
    for cell in range(cells):
        for sample in range(samples):
            correlation_coefficient_list.append(
                correlation_coefficients[cell,sample,0])
    
    # Creates bins so that all graphs are easy to look at.
    x_bins = []
    for i in range(-10,21):
        x_bins.append(i*0.05)
    
    # Creates histogram
    plt.hist(correlation_coefficient_list,bins=x_bins)
    plt.title("Histogram of Correlation Coefficients")
    plt.savefig("Histogram of Correlation Coefficients.png")
    plt.close()
    plt.clf()
    
    return