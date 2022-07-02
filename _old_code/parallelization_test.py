# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:48:44 2020

@author: Yoshi
"""
import numpy as np
from joblib import Parallel, delayed



def shift_scaler(shift,power):
    return shift*2**-power

def joblib_loop():
    # Sets maximum zoom in and zoom out
    start_power = -1
    max_zoom = 2
    
    # Creates dictionary for scaled shifts
    simple_shifts = [(0,0),(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1)]
    simple_shifts = np.array(simple_shifts)
    zoom_shifts = {}
    for power in range(start_power,max_zoom+1):
        zoom_shifts[power] = Parallel(n_jobs=9)(delayed(shift_scaler)(simple_shift,power) for simple_shift in simple_shifts)
    return zoom_shifts

zoom_shifts = joblib_loop()