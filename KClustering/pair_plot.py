# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:29:32 2022

@author: Austin
"""
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import scipy.stats as stats
import seaborn as sns
import math 

def pair_plot(df):

    
  # df = df.astype(object)  
  #Makes the index of the new DataFrame
  # cell_numbers = df['cell_number'].unique()
  # cell_uni_list = cell_numbers.tolist()
  # Index = []
  
  
  
  
  
  # n = len(cell_uni_list)
  # for i in range(n):
      # array = np.asarray(df['trial_average'][i], dtype=np.float32)
      # cell_number = np.asarray(cell_uni_list[i])
      # Index.append([cell_number,array])

      
  # Index = np.array(Index, dtype=np.float32)
      
  # plt.imshow(Index, cmap='hot', interpolation='nearest', dtype=np.float32)
  x = []
  correlation = []
  y = []
  
  
  for a in range(df.shape[0]):
      for b in range(df.shape[0]):
          x.append(df['cell_number'].iloc[a])
          y.append(df['cell_number'].iloc[b])
          npar = np.asarray(df['trial_average'].iloc[a])
          npbr = np.asarray(df['trial_average'].iloc[b])
          corr = np.corrcoef(npar, npbr)
          correlation.append(corr)
          
  df_correlation = pd.DataFrame({'x':x, 'y':y, 'correlation_coefficient': correlation})
  df_correlation['cor_avg'] = df_correlation['correlation_coefficient'].map(lambda x: x.mean())
  print(df_correlation['cor_avg'])
  plot_df = df_correlation.groupby(by = 'x')['cor_avg'].apply(list)
  plotty = []
  for p in plot_df:
      plotty.append(p)
  plotty_df = pd.DataFrame({'cor_avgs': plotty})
  plotty_df = plotty_df.reset_index(drop=False)
  sns.heatmap(plotty)
  plt.show()
  
  # df_correlation['color_values'] = df_correlation['correlation_coefficient']
  # # plt.plot(df_correlation)
  
  # df4 = df
  # i = 0
  # correlation_coefficients = []
  # first = []
  # second = []
  # sample_r_values = []

  
  # for c in range(len(df['trial_average'][0])):
  #     while i < df.shape[0]:
  #         first.append(df['trial_average'].iloc[i][c])
  #         second.append(df['trial_average'].iloc[i][c+1])
  #         r,p = stats.pearsonr(first, second)
  #         i += 1
  #         if math.isnan(r):
  #             r = 0
  #         sample_r_values.append(r)
  #         first.clear()
  #         second.clear()
  #         if len(sample_r_values) == 31:
  #           average_r = np.mean(sample_r_values)
  #           correlation_coefficients.append(average_r)
  #           sample_r_values.clear()
              
    
    
  # df4 = pd.DataFrame({'cell_number': df['cell_number'], 'correlation_coefficients':correlation_coefficients})
  
  
  return 
    
