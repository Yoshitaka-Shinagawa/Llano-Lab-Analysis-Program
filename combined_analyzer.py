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
os.chdir(f"{program_path}/machine_learning")
from sample_averaging import *


def combined_analyzer(path,gauss_filter="Default",threshold=0.6):
    
    # Sets mode to new tonotopy analysis
    mode = 0
    
    # Create a class to store various information in
    class info_storage:
        def __init__(self):
            self.gauss_filter = gauss_filter
            self.threshold    = threshold
            self.mode         = mode
    
    # Create an instance of the class
    modulation_info = info_storage()

    # Modulation Analysis
    modulation_info.path = f"{path}/Modulation"
    
    # Stabilizes and filters images
    m_raw_images,m_filtered_images,modulation_info = motion_corrector(modulation_info)
    
    # Extracts the data from the images
    m_data,modulation_info = data_extractor_subtraction(m_filtered_images,modulation_info)
    
    # Flags cells based on their responsiveness
    modulation_info = cell_flagger(m_data,modulation_info)
    
    #Finds average of the samples
    modulation_info = sample_averaging(m_data,modulation_info)
    
    # Creates tonotopic map based on cell flags
    modulation_info = tonotopic_map_generator(modulation_info)
    
    # Creates graphs for traces of individual cells
    cell_grapher(m_data,modulation_info)
    
    # Analyzes response of cell populations
    population_analysis(m_data,modulation_info)
    
    # Creates a correlation matrix between cells
    # correlation_matrix(modulation_path,modulation_data,modulation_cell_flags,modulation_framerate_information,modulation_extra_flag,mode)
    
    # Various debugging tools
    r_histogram_creator(modulation_info)
    
    
    # Create an instance of the class
    tonotopy_info = info_storage()
    
    # Tonotopy Analysis
    tonotopy_info.path = f"{path}/Tonotopy"
    
    # Stabilizes and filters images
    t_raw_images,t_filtered_images,tonotopy_info = motion_corrector(tonotopy_info)
    
    # Extracts the data from the images
    t_data,tonotopy_info = data_extractor_subtraction(t_filtered_images,tonotopy_info)
    
    # Flags cells based on their responsiveness
    tonotopy_info = cell_flagger(t_data,tonotopy_info)
    
    # Creates tonotopic map based on cell 
    tonotopy_info = tonotopic_map_generator(tonotopy_info)
    
    # Creates graphs for traces of individual cells
    cell_grapher(t_data,tonotopy_info)
    
    # Analyzes response of cell populations
    population_analysis(t_data,tonotopy_info)
    
    # Analyzes receptive field sum
    receptive_field_sum_analysis(tonotopy_info)
    
    # Creates a correlation matrix between cells
    # correlation_matrix(tonotopy_path,tonotopy_data,tonotopy_cell_flags,tonotopy_framerate_information,tonotopy_extra_flag,mode)
    
    # Various debugging tools
    r_histogram_creator(tonotopy_info)
    
    # Performs combined analysis of tonotopy and modulation
    modulation_index_analysis(path,modulation_info,tonotopy_info)
    
    # Announces that analysis is finished
    print(f"Analysis finished for {path}")
    
    # Changes directory to main so deleting folders does not interfere with rerunning the program
    os.chdir(path)



# base_path = "E:/Llano Lab/Injected Mice"

# combined_analyzer(f"{base_path}/2022-06-20/GAD Injected 030422 M",(1,1,2))
# combined_analyzer(f"{base_path}/2022-06-23/GAD Injected 030622 M 99 um",(1,1,2))
# combined_analyzer(f"{base_path}/2022-06-23/GAD Injected 030622 M 169 um",(1,1,2))
# combined_analyzer(f"{base_path}/2022-06-24/GAD Injected 030622 M",(1,1,2))
# combined_analyzer(f"{base_path}/2022-06-27/GAD Injected 030622 M 88 um",(1,1,2))
# combined_analyzer(f"{base_path}/2022-06-27/GAD Injected 030622 M 95 um",(1,1,2))

base_path = "E:/Llano Lab/Sex Difference"

# combined_analyzer(f"{base_path}/2022-08-17/RCAMP CBA 022822 F (+000,+000,-196)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-17/RCAMP CBA 022822 F (+234,-024,-133)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-17/RCAMP CBA 022822 F (+434,-052,-086)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-17/RCAMP CBA 022822 F (+600,-027,-103)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-17/RCAMP CBA 022822 F (+768,-026,-120)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-17/RCAMP CBA 022822 F (+892,+004,-128)",(1,1,2))
combined_analyzer(f"{base_path}/2022-08-24/RCAMP CBA 032722 F (+000,+000,-127)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-24/RCAMP CBA 032722 F (+287,-006,-094)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-24/RCAMP CBA 032722 F (+461,+006,-089)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-24/RCAMP CBA 032722 F (+573,-028,-111)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-24/RCAMP CBA 032722 F (+670,-040,-181)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-08-24/RCAMP CBA 032722 F (+790,-064,-214)",(1,1,2))




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


# base_path = "D:/Llano Lab/Tonotopic Analysis/Module Project/Surface View"

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

# combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+000,+000,-160)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+256,-014,-116)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+423,-046,-125)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+617,-038,-160)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (+768,-020,-230)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-16/GAD67 neo RCAMP 00917 M (-124,-062,-275)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+000,+000,-132)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+240,+000,-113)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+371,-033,-088)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+554,+090,-192)",(1,1,2))
# combined_analyzer(f"{base_path}/2021-11-20/GAD67 RCAMP 00921 M (+651,+155,-231)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-170,+398,-049)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-184,+200,+002)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-207,+000,+000)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-250,+502,-009)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-280,-059,+023)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-01-04/GAD67 neo RCAMP 112421 M (-313,+589,+015)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+000,+000,+160)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+209,+003,+135)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+400,-039,+098)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+595,-055,+152)",(1,1,2))
# combined_analyzer(f"{base_path}/2022-04-26/CBAxRCAMP 022822 M (+732,-088,+169)",(1,1,2))

