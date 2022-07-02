# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 01:23:18 2021

@author: Yoshi
"""

import warnings
warnings.simplefilter(action="ignore",category=FutureWarning)

import os



program_path = os.getcwd()

os.chdir(f"{program_path}/motion_corrector")
from motion_corrector import *
os.chdir(f"{program_path}/data_extractor_subtraction")
from data_extractor_subtraction import *
os.chdir(f"{program_path}/cell_flagger")
from cell_flagger import *
os.chdir(f"{program_path}/map_generators")
from tonotopic_map_generator import *
os.chdir(f"{program_path}/cell_grapher")
from cell_grapher import *
os.chdir(f"{program_path}/population_analysis")
from population_analysis import *
os.chdir(f"{program_path}/receptive_field_sum_analysis")
from receptive_field_sum_analysis import *
os.chdir(f"{program_path}/correlation_matrix")
from correlation_matrix import *
os.chdir(f"{program_path}/debug_tools")
from r_histogram_creator import *
os.chdir(f"{program_path}/modulation_index_analysis")
from modulation_index_analysis import *



def combined_analyzer(path,gauss_filter="Default",threshold=0.6):
    
    # Sets mode to new tonotopy analysis
    mode = 0
    
    # Modulation Analysis
    modulation_path = f"{path}/Modulation"
    
    # Stabilizes and filters images
    modulation_raw_images,modulation_filtered_images,modulation_folders_list = motion_corrector(modulation_path,gauss_filter,mode)
    
    # Extracts the data from the images
    modulation_extra_flag,modulation_cell_locations,modulation_cell_flags,modulation_data,modulation_framerate_information,modulation_key,modulation_frequencies,modulation_frequency_unit,modulation_intensities,modulation_intensity_unit = data_extractor_subtraction(modulation_path,modulation_filtered_images,modulation_folders_list,mode)
    
    # Flags cells based on their responsiveness
    modulation_cell_flags,modulation_correlation_coefficients,modulation_areas_under_curves = cell_flagger(modulation_path,modulation_cell_flags,modulation_key,modulation_frequencies,modulation_intensities,modulation_data,modulation_framerate_information,mode,threshold)
    
    # Creates tonotopic map based on cell flags
    modulation_canvas,modulation_width,modulation_height,modulation_scale,modulation_radius = tonotopic_map_generator(modulation_path,modulation_cell_locations,modulation_frequencies,modulation_frequency_unit,modulation_cell_flags,modulation_extra_flag,mode)
    
    # Creates graphs for traces of individual cells
    cell_grapher(modulation_path,modulation_data,modulation_cell_flags,modulation_correlation_coefficients,modulation_areas_under_curves,modulation_framerate_information,modulation_key,modulation_frequencies,modulation_frequency_unit,modulation_intensities,modulation_intensity_unit,mode,threshold)
    
    # Analyzes response of cell populations
    population_analysis(modulation_path,modulation_data,modulation_cell_flags,modulation_framerate_information,modulation_key,modulation_frequencies,modulation_frequency_unit,modulation_intensities,modulation_intensity_unit,modulation_extra_flag,mode)
    
    # Various debugging tools
    r_histogram_creator(modulation_path,modulation_correlation_coefficients)
    
    # Ttonotopy Analysis
    tonotopy_path = f"{path}/Tonotopy"
    
    # Stabilizes and filters images
    tonotopy_raw_images,tonotopy_filtered_images,tonotopy_folders_list = motion_corrector(tonotopy_path,gauss_filter,mode)
    
    # Extracts the data from the images
    tonotopy_extra_flag,tonotopy_cell_locations,tonotopy_cell_flags,tonotopy_data,tonotopy_framerate_information,tonotopy_key,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit = data_extractor_subtraction(tonotopy_path,tonotopy_filtered_images,tonotopy_folders_list,mode)
    
    # Flags cells based on their responsiveness
    tonotopy_cell_flags,tonotopy_correlation_coefficients,tonotopy_areas_under_curves = cell_flagger(tonotopy_path,tonotopy_cell_flags,tonotopy_key,tonotopy_frequencies,tonotopy_intensities,tonotopy_data,tonotopy_framerate_information,mode,threshold)
    
    # Creates tonotopic map based on cell flags
    tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_scale,tonotopy_radius = tonotopic_map_generator(tonotopy_path,tonotopy_cell_locations,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_cell_flags,tonotopy_extra_flag,mode)
    
    # Creates graphs for traces of individual cells
    cell_grapher(tonotopy_path,tonotopy_data,tonotopy_cell_flags,tonotopy_correlation_coefficients,tonotopy_areas_under_curves,tonotopy_framerate_information,tonotopy_key,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit,mode,threshold)
    
    # Analyzes response of cell populations
    population_analysis(tonotopy_path,tonotopy_data,tonotopy_cell_flags,tonotopy_framerate_information,tonotopy_key,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit,tonotopy_extra_flag,mode)
    
    # Analyzes receptive field sum
    receptive_field_sum_analysis(tonotopy_path,tonotopy_key,tonotopy_cell_flags,tonotopy_extra_flag,tonotopy_correlation_coefficients,tonotopy_areas_under_curves,tonotopy_frequencies,tonotopy_frequency_unit,tonotopy_intensities,tonotopy_intensity_unit,tonotopy_canvas,tonotopy_width,tonotopy_height,tonotopy_cell_locations,tonotopy_scale,tonotopy_radius,threshold)
    
    # Various debugging tools
    r_histogram_creator(tonotopy_path,tonotopy_correlation_coefficients)
    
    # Performs combined analysis of tonotopy and modulation
    modulation_index_analysis(path,threshold,modulation_cell_flags,tonotopy_cell_flags,tonotopy_extra_flag,
                              modulation_correlation_coefficients,tonotopy_correlation_coefficients,
                              modulation_areas_under_curves,tonotopy_areas_under_curves,
                              modulation_key,tonotopy_key,modulation_frequencies,tonotopy_frequencies,
                              modulation_frequency_unit,tonotopy_frequency_unit,
                              modulation_intensities,tonotopy_intensities,
                              modulation_intensity_unit,tonotopy_intensity_unit,
                              tonotopy_canvas,tonotopy_width,tonotopy_height,
                              tonotopy_cell_locations,tonotopy_scale,tonotopy_radius)
    
    # Announces that analysis is finished
    print(f"Analysis finished for {path}")
    
    # Changes directory to main so deleting folders does not interfere with rerunning the program
    os.chdir(path)



# base_path = "D:/Llano Lab/Tonotopic Analysis/Module Project/Prism View"

# combined_analyzer(f"{base_path}/2021-09-04/Prism GAD67xRCAMP M 051621 Data Set 1",(2,2,2))
# combined_analyzer(f"{base_path}/2021-09-04/Prism GAD67xRCAMP M 051621 Data Set 2",(2,2,2))
# combined_analyzer(f"{base_path}/2021-10-14/GAD67 neo RCAMP",(2,2,2))
# combined_analyzer(f"{base_path}/2021-10-26/GAD67 neo RCAMP 00824 F Prism",(2,2,2))
# combined_analyzer(f"{base_path}/2021-10-28/GAD67 neo RCAMP 00915 M Prism Caudal",(2,2,2))
# combined_analyzer(f"{base_path}/2021-10-28/GAD67 neo RCAMP 00915 M Prism Rostral",(2,2,2))
# combined_analyzer(f"{base_path}/2021-11-20/GAD67 neo RCAMP 00921 M Prism Rostral",(2,2,2))
# combined_analyzer(f"{base_path}/2021-11-24/GAD67 x RCAMP 00824 M Prism",(2,2,2))
# combined_analyzer(f"{base_path}/2021-11-25/GAD67 x RCAMP 00824 M Prism NEG 1",(2,2,2))
# combined_analyzer(f"{base_path}/2021-11-25/GAD67 x RCAMP 00824 M Prism NEG 2",(2,2,2))
# combined_analyzer(f"{base_path}/2021-11-25/GAD67 x RCAMP 00824 M Prism NEG 3",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-05/GAD67xRCAMP 120521 M Prism Data Set 1",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-05/GAD67xRCAMP 120521 M Prism Data Set 2",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-11/GAD67xRCAMP 120521 M Prism",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-12/GAD67xRCAMP 120521 M Prism Dataset D",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-12/GAD67xRCAMP 120521 M Prism Dataset DV",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-12/GAD67xRCAMP 120521 M Prism Dataset V",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-14/GAD67xRCAMP 011622 M Prism Dataset DC",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-14/GAD67xRCAMP 011622 M Prism Dataset DR",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-15/GAD67xRCAMP 011622 M Prism Dataset DC",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-15/GAD67xRCAMP 011622 M Prism Dataset DCR",(2,2,2))
# combined_analyzer(f"{base_path}/2022-04-15/GAD67xRCAMP 011622 M Prism Dataset DR",(2,2,2))


base_path = "D:/Llano Lab/Tonotopic Analysis/Module Project/Surface View"

# combined_analyzer(f"{base_path}/2021-10-05/RCAMPxGAD67 0630 M Brown (+000,+000,-157)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-05/RCAMPxGAD67 0630 M Brown (+299,-020,-132)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-05/RCAMPxGAD67 0630 M Brown (+510,-023,-138)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-05/RCAMPxGAD67 0630 M Brown (+613,+005,-276)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-08/RCAMPxGAD67 0630 M Brown (+000,+000,-187)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-08/RCAMPxGAD67 0630 M Brown (+269,-007,-170)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-08/RCAMPxGAD67 0630 M Brown (+423,-045,-116)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-08/RCAMPxGAD67 0630 M Brown (+547,-024,-155)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-08/RCAMPxGAD67 0630 M Brown (+665,-009,-239)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-11/RCAMPxGAD67 0816 M Brown (+000,+000,-137)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-11/RCAMPxGAD67 0816 M Brown (+300,-050,-080)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-11/RCAMPxGAD67 0816 M Brown (+508,-034,-120)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-11/RCAMPxGAD67 0816 M Brown (+631,-047,-195)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-11/RCAMPxGAD67 0816 M Brown (+763,-036,-240)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-15/RCAMPxGAD67 0724 F Brown (+000,+000,-291)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-15/RCAMPxGAD67 0724 F Brown (+200,-050,-191)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-15/RCAMPxGAD67 0724 F Brown (+325,-050,-120)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-15/RCAMPxGAD67 0724 F Brown (+425,-100,-099)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-15/RCAMPxGAD67 0724 F Brown (+550,+000,-150)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-10-15/RCAMPxGAD67 0724 F Brown (+625,+025,-200)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-03/RCAMPxGAD67 0709 M Brown (+000,+000,-195)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-03/RCAMPxGAD67 0709 M Brown (+244,-051,-155)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-03/RCAMPxGAD67 0709 M Brown (+410,-105,-095)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-03/RCAMPxGAD67 0709 M Brown (+609,-162,-040)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-03/RCAMPxGAD67 0709 M Brown (+760,-100,-135)",(1,1,2))

combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+000,+000,-160)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+256,-014,-116)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+423,-046,-125)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+617,-038,-160)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+768,-020,-230)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (-124,-062,-275)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+000,+000,-132)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+240,+000,-113)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+371,-033,-088)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+554,+090,-192)",(1,1,2))
combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+651,+155,-231)",(1,1,2))
combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-170,+398,-049)",(1,1,2))
combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-184,+200,+002)",(1,1,2))
combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-207,+000,+000)",(1,1,2))
combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-250,+502,-009)",(1,1,2))
combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-280,-059,+023)",(1,1,2))
combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-313,+589,+015)",(1,1,2))
combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+000,+000,+160)",(1,1,2))
combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+209,+003,+135)",(1,1,2))
combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+400,-039,+098)",(1,1,2))
combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+595,-055,+152)",(1,1,2))
combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+732,-088,+169)",(1,1,2))

