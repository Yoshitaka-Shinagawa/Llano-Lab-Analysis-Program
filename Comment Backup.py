# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 11:36:48 2022

@author: Yoshi
"""



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