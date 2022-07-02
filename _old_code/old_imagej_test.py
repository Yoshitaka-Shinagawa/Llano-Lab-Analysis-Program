# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:22:44 2019

@author: Yoshi
"""



import imagej
#ij = imagej.init('D:/Program Files/fiji-win64/Fiji.app')#,headless=False)
#ij.ui().showUI()


image = ij.op().image().histogram(folder_data[0])