# Llano-Lab-Analysis-Program

Test


## Installation
### Required Packages
* CaImAn
* Read-ROI
* Shapely

## To-do list
### In progress
* Rewrite the program with class
* Improve comments
* Make sure lines do not go over the 80 char limit
### Future plans
* Change flag for noise response from "Yes" to "Responsive"
* Change noise analysis so that it's generic and can be used for single stimulus analysis
* Make the contamination ratio specifiable
* Create documentation for how to use the program
* Add a way to classify cells based on their response type
* Include an example data set for people to use if there is an easy way to distribute it
* Add a debug function to visualize raw, unfiltered data
* Finish the debug feature for best angles
* Separate out the maps for receptive field and modulation indices
* Rewrite the correlation matrix function to accept raw data
* Find a better way to fix the negative values from motion correction
* Convert program to a library
* Give the program a cool name and logo
* Possibly use the GPU for motion correction to speed it up
* Possibly add a way to process other types of ROIs
* Possibly add a way to scale rectangular and polygonal ROIs
* Possibly add a way to process other types of images
* Possibly add a GUI to make it easier to use

motion_corrector
96+97: Change to folder_name
106: Change warning to "No tiffs found"
161: Change to one line
164-168: Comments to be clearer
171: Supposed to be commented out

xyz_gaussian_filter
Fix to 80 char limit
39-40: Loop constants are not necessary
44: Change to row_data
47: Might be applying gaussian_filter1d twice
