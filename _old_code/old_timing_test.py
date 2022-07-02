# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:26:51 2019

@author: Yoshi
"""

import timeit
from skimage.metrics import structural_similarity as ssim
from skimage.measure import compare_ssim

from image_rounder import *

rounded_average = image_rounder(image_average)
rounded_filtered = image_rounder(filtered_data[0])

def ssim_time():
    score = ssim(rounded_average,rounded_filtered)
    return score

def compare_ssim_time():
    score = compare_ssim(rounded_average,rounded_filtered)
    return score

print(timeit.timeit(ssim_time,number=100))
print(timeit.timeit(compare_ssim_time,number=100))
