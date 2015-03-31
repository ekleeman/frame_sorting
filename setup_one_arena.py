# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:46:51 2015

@author: Elise
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 19:27:02 2014

@author: Noah
"""

import cv2
import scipy.misc
import csv
from os.path import join
import os
from scipy import ndimage

def extract_csv(filename):
    """opens a csv file and extracts it and returns it as a list of lists"""
    with open(filename, 'rb') as csvfile:
        data=list(csv.reader(csvfile))
    return(data)
    
def criteria_info_setup(filename):
    """accepts the file name of the inclusion/exclusion criteria, and returns a list of ints 
    that represent, in order, the radius for width inclusion, for height inclusion, for width exclusion and for height exclusion
    Note that, as currently written, assumes the criteria are the same for each object type"""
    criteria_raw=extract_csv(filename)
    criteria_ints=[int(z[1]) for z in criteria_raw] #note that this requires the values be in the second column
    return(criteria_ints)

def remove_spaces(data):
    """accepts a list of lists, replaces any spaces with emptiness"""
    for i,j in enumerate(data):
        for k,l in enumerate(j):    
            new=data[i][k].replace(' ','')
            data[i][k] = new
    return() 

def listing_arenas(data, col):
    """accepts a list of lists and the column number you are interested in
    returns a list of all of the folders you need to make (all the arenas)"""
    folder_list=[]    
    column=[z[col] for z in data]
    
    for y in column:
        if len(y)!=0:
            folder_list.append(y)
    return(folder_list)

def find_col_min(data, col):
    """accepts a list of lists and the column number you are interested in
    returns the min of the column"""
    minlist=[]
    column=[z[col] for z in data]       

    for y in column:
        if len(y)!=0:
            minlist.append(int(y))
    minimum=min(minlist)
    return(minimum)

def object_info_setup(data, arenas):
    """mines the -data- list of lists for the info needed for each object in each arena. 
    Returns lists for A and B heights and widths for each arena in order. 
    NOTE: This is a smaller version of the program used in the sorting template"""
    A_Height, A_Width, B_Height, B_Width= [], [], [], []
    for a in range(len(arenas)):
        A_Height.append(int(round(float(data[1+2*a][2]))))
        A_Width.append(int(round(float(data[1+2*a][1]))))
        B_Height.append(int(round(float(data[2+2*a][2]))))
        B_Width.append(int(round(float(data[2+2*a][1]))))
    return(A_Height, A_Width, B_Height, B_Width)

def arena_info_setup(data, arena):
    """mines the -data- list of lists for the info needed for each arena's dimentions. 
    Returs lists for the arena top, bottom, left and right in order of arena."""
    top, bottom, left, right = [], [], [], []
    arena_len=len(arena)
    for a in range(arena_len):
        top.append(min(int(round(float(data[1+(arena_len+a)*2][2]))), int(round(float(data[2+(arena_len+a)*2][2])))))
        bottom.append(max(int(round(float(data[1+(arena_len+a)*2][2]))), int(round(float(data[2+(arena_len+a)*2][2])))))
        left.append(min(int(round(float(data[1+(arena_len+a)*2][1]))), int(round(float(data[2+(arena_len+a)*2][1])))))
        right.append(max(int(round(float(data[1+(arena_len+a)*2][1]))), int(round(float(data[2+(arena_len+a)*2][1])))))
    return(top, bottom, left, right)    

def image_processing(img):
    """Accepts an image, then opens it and processes it to highlight 
    (gaussian filter and thresholding). Returns processed image"""
    imgone=img[:,:,2]
    imgf=ndimage.gaussian_filter(imgone,1)
    imgft=imgf>60
    return(imgft)

def draw_boxes(test_image, arena, a_heights, a_widths, b_heights, b_widths, criteria, crop_top, crop_bottom, crop_left, crop_right):
    """Drawing inclusion and exclusion boxes, and cropping boxes around each arena"""
    for cur_arena in range(len(arena)):    
        cv2.rectangle(test_image, (a_widths[cur_arena]-criteria[0],a_heights[cur_arena]-criteria[1]), (a_widths[cur_arena]+criteria[0],a_heights[cur_arena]+criteria[1]), (0,0,255))  
        cv2.rectangle(test_image, (b_widths[cur_arena]-criteria[0],b_heights[cur_arena]-criteria[1]), (b_widths[cur_arena]+criteria[0],b_heights[cur_arena]+criteria[1]), (0,0,255))   
        cv2.rectangle(test_image, (a_widths[cur_arena]-criteria[2],a_heights[cur_arena]-criteria[3]), (a_widths[cur_arena]+criteria[2],a_heights[cur_arena]+criteria[3]), (0,0,255))
        cv2.rectangle(test_image, (b_widths[cur_arena]-criteria[2],b_heights[cur_arena]-criteria[3]), (b_widths[cur_arena]+criteria[2],b_heights[cur_arena]+criteria[3]), (0,0,255))
        cv2.rectangle(test_image, (crop_left[cur_arena], crop_top[cur_arena]), (crop_right[cur_arena], crop_bottom[cur_arena]), (0,0,255))

def turn_it_blue(image, blue):
    """Accepts the processed image (true or false (for pixels showing a "mouse")), and the original image.
    Changes the original image to show blue pixels wherever it detected a mouse. Returns nothing."""
    for x in range(len(image[:,])):
        for y in range(len(image[x,:])):
            if image[x,y]==0:
                blue[x,y]=(0,0,255)
    return()


if __name__=="__main__":
    directory=input("What is the name of the directory your files are in? Make sure to put r in front and then surround the directory with quotes. ")
    png_directory=join(directory, 'PNGs')
    prep_directory=join(directory, 'Prep data')
    criteria_file=join(prep_directory, 'criteria.csv')
    
    which_folder=input("Which folder would you like to test? Must match exactly, and be in quotes. ")
    criteria=criteria_info_setup(criteria_file)
    
    video = which_folder
    
    dataFile=join(prep_directory,video+'_results.csv')
    data=extract_csv(dataFile)
    remove_spaces(data)
    arenas=listing_arenas(data, 3)  #note that the relevant column number is hard-coded here
    a_heights, a_widths, b_heights, b_widths = object_info_setup(data, arenas)
    crop_top, crop_bottom, crop_left, crop_right=arena_info_setup(data, arenas)
    image_file=join(join(png_directory, video), video+'08991.png') #note that this image number is hard coded in
    img = scipy.misc.imread(image_file)
    processed_img=image_processing(img)
    turn_it_blue(processed_img, img)
    draw_boxes(img, arenas, a_heights, a_widths, b_heights, b_widths, criteria, crop_top, crop_bottom, crop_left, crop_right)
    scipy.misc.imsave(join(prep_directory, video+'_setup.png'), img)