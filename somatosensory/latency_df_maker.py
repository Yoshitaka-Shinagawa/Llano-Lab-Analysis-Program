# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:11:57 2022

@author: Austin
"""
import os
import shutil
import pandas as pd
import numpy as np


def latency_df_maker(info_storage):
    
    # Extracts variables from the info_storage class
    path           = info_storage.path

    
    # Creates output directories 
    latency_map_output_path = f"{path}/Output/Latency"
    if os.path.exists(f"{path}/Output/All Data") == True:
        shutil.rmtree(f"{path}/Output/All Data")
    if os.path.exists(f'{path}/Output/All Data') == False:
        excel_output_path = f"{path}/Output/All Data"
        os.mkdir(excel_output_path)
    
    #Paths to each excel sheet
    total_path =f'{path}/Output/Cell Traces/Spreadsheets/Data_by_Trial.xlsx'
    first_2_path = f'{path}/Output/First Two/Spreadsheets/Peak values.xlsx'
    onset_path =f'{path}/Output/Latency/Onset/Spreadsheets/Peak values.xlsx'
    offset_path =f'{path}/Output/Latency/Offset/Spreadsheets/Peak values.xlsx'
    onset_first_2_path = f'{path}/Output/Latency/Onset/First Two/Spreadsheets/Peak values.xlsx'
    offset_first_2_path = f'{path}/Output/Latency/Offset/First Two/Spreadsheets/Peak values.xlsx'

    # Dataframes of all Trials from Excel 
    total_df = pd.read_excel(total_path)
    first_2_df = pd.read_excel(first_2_path)
    
    # Latency dataframes from Excel
    onset_df = pd.read_excel(onset_path)
    offset_df = pd.read_excel(offset_path)
    onset_first_2_df = pd.read_excel(onset_first_2_path)
    offset_first_2_df = pd.read_excel(offset_first_2_path)

    # Renames the DataFrame columns
    total_df['responsive_all_trials'] = total_df['cell_flag']
    total_df['responsive_1_trial'] = 'N/A'
    first_2_df['responsive_f2_trials'] = first_2_df['Cell Flag']
    onset_df['onset'] = onset_df['Cell Flag']
    offset_df['offset'] = offset_df['Cell Flag']
    onset_first_2_df['onset_f2'] = onset_first_2_df['Cell Flag']
    offset_first_2_df['offset_f2'] = offset_first_2_df['Cell Flag']
    
    # Creates empty columns in the dataframe 
    total_df['latency_color_all_trials'] = np.nan
    total_df['latency_color_f2_trials'] = np.nan
    total_df['adaptive'] = np.nan 
    total_df['non-adaptive'] = np.nan 
    
    # Potential Empty Columns 
    # total_df['adaptive_onset'] = np.nan
    # total_df['non-adaptive_onset'] = np.nan
    # total_df['adaptive_offset'] = np.nan
    # total_df['non-adaptive_offset'] = np.nan
    
    # Declares variables to check True or False
    total_response = False
    f2_response = False 
    f1_response = False 
    
    onset_response = False
    offset_response = False
    
    onset_adaptive_response = False
    offset_adaptive_response = False
    
    # Iterates through rows of the dataframe and assigns colors for latency map across all Trials 
    for index in range(len(total_df)):
        
        
        # iterates through each value
        if onset_df.at[index,'onset'] == 'Yes':
            onset_response = True
        else:
            onset_response = False
        
        if offset_df.at[index,'offset'] == 'Yes':
            offset_response = True
        else:
            offset_response = False
    
            
        # Sets conditional statements for checking the Dataframe latency values
        if (onset_response == True) and (offset_response == False):
            
            total_df.at[index,'latency_color_all_trials']= 0
        
        elif (onset_response == False) and (offset_response == True):
            
            total_df.at[index,'latency_color_all_trials']= 1
        
        elif (onset_response == True) and (offset_response == True):
            
            total_df.at[index,'latency_color_all_trials'] = 2 
   
    # Iterates through rows of the dataframe and assigns colors for latency map across adaptive cells
    for index in range(len(total_df)):
         
         
         # iterates through each value
         if onset_first_2_df.at[index,'onset_f2'] == 'Yes':
             onset_adaptive_response = True
         else:
             onset_adaptive_response = False
         
         if offset_first_2_df.at[index,'offset_f2'] == 'Yes':
             offset_adaptive_response = True
         else:
             offset_adaptive_response = False
     
             
         # Sets conditional statements for checking the Dataframe latency values
         if (onset_adaptive_response == True) and (offset_adaptive_response == False):
             
             total_df.at[index,'latency_color_f2_trials']= 0
         
         elif (onset_adaptive_response == False) and (offset_adaptive_response == True):
             
             total_df.at[index,'latency_color_f2_trials']= 1
         
         elif (onset_adaptive_response == True) and (offset_adaptive_response == True):
             
             total_df.at[index,'latency_color_f2_trials'] = 2
        
    # Iterates through rows of the dataframe and assigns colors for latency map across all Trials 
    for index in range(len(total_df)):
        
        
        # iterates through each value
        if total_df.at[index,'responsive_all_trials'] == 'Yes':
            total_response = True
        else:
            total_response = False
        
        if first_2_df.at[index,'responsive_f2_trials'] == 'Yes':
            f2_response = True
        else:
            f2_response = False
            
        if total_df.at[index,'auc_1'] >= (total_df.loc[index,['auc_2','auc_3','auc_4','auc_5']].mean(axis=0))*3:
           f1_response = True
        else:
           f1_response = False
    
            
        # Sets conditional statements for checking the Dataframe latency values
        if (f2_response == True) and (total_response == False):
            
            total_df.at[index,'adaptive']= 'Yes'
        
        if (total_response == True):
            
            total_df.at[index,'non-adaptive']= 'Yes'
        
        if (f1_response == True):
            total_df.at[index,'responsive_1_trial'] = 'Yes'
    
        
    # Renames the Dataframe 
    latency_df = total_df
    
    # Stores the dataframe into info_storage
    info_storage.latency_df = latency_df
    
    writer = pd.ExcelWriter(f"{path}/Output/All Data/Data_Spreadsheet.xlsx")
    
    latency_df.to_excel(writer)
    
    writer.save()
    writer.close()
    
    
    return info_storage