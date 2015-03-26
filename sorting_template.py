# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
import scipy
import scipy.misc
import os
#import sys
from os.path import join
from scipy import ndimage
#import cv2

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

def folders_in_directory(directory):
    """accepts a directory, and returns a list of the folders in the directory"""
    dir_folders=os.walk(directory).next()[1]
    return(dir_folders)
    
def listing_pngs(directory):
    """goes to the file for the video being run, and returns a list of all the (png) files within"""
    list_files=os.listdir(directory)
    return (list_files)
    
def make_folders(s_directory, video, arenas):
    """makes folders to accept the sorted pngs in the sorted_directory
    checks to makes sure that the folders aren't already made, if they are returns false"""
    everything_ok=True    
    the_directory=join(s_directory, video)
    
    if not os.path.exists(the_directory):
        os.makedirs(the_directory)
    else:
        everything_ok=False
    
    for arena in arenas:
        arena_folder=join(the_directory,arena)
        if not os.path.exists(arena_folder):
            os.makedirs(arena_folder)
        else:
            everything_ok=False    
        if not os.path.exists(join(arena_folder,'ObjA')):
            os.makedirs(join(arena_folder,'ObjA'))
        else:
            everything_ok=False  
        if not os.path.exists(join(arena_folder,'ObjB')):
            os.makedirs(join(arena_folder,'ObjB'))
        else:
            everything_ok=False
        if not os.path.exists(join(arena_folder,'Both')):
            os.makedirs(join(arena_folder,'Both'))
        else:
            everything_ok=False
    
    return(everything_ok)

def object_info_setup(data, arenas):
    """mines the -data- list of lists for the info needed for each object in each arena.
    Returns lists for A and B heights and widths, and starts and ends for each arena in order"""
    A_Height, A_Width, B_Height, B_Width, startFrame, endFrame = [], [], [], [], [], []
    for a in range(len(arenas)):
        A_Height.append(int(data[1+2*a][2]))
        A_Width.append(int(data[1+2*a][1]))
        B_Height.append(int(data[2+2*a][2]))
        B_Width.append(int(data[2+2*a][1]))
        startFrame.append(int(data[1+a][4]))
        endFrame.append(int(data[1+a][4])+int(data[1][5])) #start frame+total number of frames
    return(A_Height, A_Width, B_Height, B_Width, startFrame, endFrame)

def arena_info_setup(data, arena):
    """mines the -data- list of lists for the info needed for each arena's dimentions. 
    Returs lists for the arena top, bottom, left and right in order of arena."""
    top, bottom, left, right = [], [], [], []
    arena_len=len(arena)
    for a in range(arena_len):
        top.append(min(int(data[1+(arena_len+a)*2][2]), int(data[2+(arena_len+a)*2][2])))
        bottom.append(max(int(data[1+(arena_len+a)*2][2]), int(data[2+(arena_len+a)*2][2])))
        left.append(min(int(data[1+(arena_len+a)*2][1]), int(data[2+(arena_len+a)*2][1])))
        right.append(max(int(data[1+(arena_len+a)*2][1]), int(data[2+(arena_len+a)*2][1])))
    return(top, bottom, left, right)    

def image_processing(img):
    """Accepts an image, then opens it and processes it to highlight mouse
    (gaussian filter and thresholding). Returns processed image"""
    imgone=img[:,:,2]
    imgf=ndimage.gaussian_filter(imgone,1)
    imgft=imgf>60
    return(imgft)

def is_mouse_near_object(cur_arena, a_heights, a_widths, b_heights, b_widths, criteria, image):
    """Accepts the index (number-1) of the current arena, the list of object heights and widths, 
    and the file with the inclusion/exclusion zones. Returns bool values for whether animal is near
    objects A, B, or Both"""
    testerA = False
    testerB = False
    testerBoth = False
    onTheObject = False     
    for height in range(a_heights[cur_arena]-criteria[1],a_heights[cur_arena]+criteria[1]+1):       #checking if mouse near object A
        for width in range (a_widths[cur_arena]-criteria[0],a_widths[cur_arena]+criteria[0]+1):
            if image[height,width]==0:
                testerA=True
                #debugging.write('In the A inclusion zone! height: '+str(height)+' width: '+str(width)+'\n')
                if (a_heights[cur_arena]-criteria[3])<=height<=(a_heights[cur_arena]+criteria[3]) and (a_widths[cur_arena]-criteria[2])<=width<=(a_widths[cur_arena]+criteria[2]):
                    onTheObject=True
                    #debugging.write('On the A object! height: '+str(height)+' width: '+str(width)+'\n')
                    break
        else:
            continue
        break
    if onTheObject==True:
        print "on the object!"
        testerA=False
    for height in range(b_heights[cur_arena]-criteria[1],b_heights[cur_arena]+criteria[1]+1):       #checking if mouse near object B
        for width in range (b_widths[cur_arena]-criteria[0],b_widths[cur_arena]+criteria[0]+1):
            if image[height,width]==0:
                testerB=True
                #debugging.write('In the B inclusion zone! height: '+str(height)+' width: '+str(width)+'\n')                        
                if (b_heights[cur_arena]-criteria[3])<=height<=(b_heights[cur_arena]+criteria[3]) and (b_widths[cur_arena]-criteria[2])<=width<=(b_widths[cur_arena]+criteria[2]):
                    onTheObject=True
                    #debugging.write('On the B object! height: '+str(height)+' width: '+str(width)+'\n')
                    break
        else:
            continue
        break
    if onTheObject==True:
        print "on the object!"
        testerB=False                                   
    if testerA==True and testerB==True:
        testerBoth, testerA, testerB = True, False, False
    return(testerA, testerB, testerBoth)

#def draw_boxes(test_image, arena, a_heights, a_widths, b_heights, b_widths, criteria):
#    """Drawing inclusion and exclusion boxes"""
#    for cur_arena in range(len(arena)):    
#        cv2.rectangle(test_image, (a_widths[cur_arena]-criteria[0],a_heights[cur_arena]-criteria[1]), (a_widths[cur_arena]+criteria[0],a_heights[cur_arena]+criteria[1]), (0,0,255))  
#        cv2.rectangle(test_image, (b_widths[cur_arena]-criteria[0],b_heights[cur_arena]-criteria[1]), (b_widths[cur_arena]+criteria[0],b_heights[cur_arena]+criteria[1]), (0,0,255))   
#        cv2.rectangle(test_image, (a_widths[cur_arena]-criteria[2],a_heights[cur_arena]-criteria[3]), (a_widths[cur_arena]+criteria[2],a_heights[cur_arena]+criteria[3]), (0,0,255))
#        cv2.rectangle(test_image, (b_widths[cur_arena]-criteria[2],b_heights[cur_arena]-criteria[3]), (b_widths[cur_arena]+criteria[2],b_heights[cur_arena]+criteria[3]), (0,0,255))
#    scipy.misc.imsave(r'E:\081814 Mouse Behavior 1\072714 ORM\ORM testing\Prep data\retestingbox.png', test_image)

def crop_and_save(tester_A, tester_B, tester_Both, image, cropTop, cropBottom, cropLeft, cropRight, dirFolder, cage, arena, arena_name, name):
    """Checks which object(s) the mouse is near (which tester value is true), and saves a 
    cropped version of the original image into the appropriate folder"""
    imgCrop=img[cropTop[arena]:cropBottom[arena],cropLeft[arena]:cropRight[arena]]
    if tester_Both==True:
        print "near both objects"
        scipy.misc.imsave(join(join(join(join(dirFolder,cage),arena_name), 'Both'), name), imgCrop)
    elif tester_A==1:
        print "near object A"
        scipy.misc.imsave(join(join(join(join(dirFolder,cage),arena_name), 'ObjA'), name), imgCrop)
    else:
        print "near object B" 
        scipy.misc.imsave(join(join(join(join(dirFolder,cage),arena_name), 'ObjB'), name), imgCrop)
    return()

if __name__=="__main__":
    directory=r'E:\081814 Mouse Behavior 1\072714 ORM\ORM testing'
    png_directory=join(directory, 'PNGs')
    prep_directory=join(directory, 'Prep data')
    sorted_directory=join(directory, 'Sorted images')
    criteria_file=join(prep_directory, 'criteria.csv')
    
    dir_folders=folders_in_directory(png_directory)
    criteria=criteria_info_setup(criteria_file)
    
    #debugging=open(join(prep_directory, 'debugging.txt'), 'w')
    
    for video in dir_folders:
        print "Starting video:", video    
        dataFile=join(prep_directory,video+'_results.csv')
        data=extract_csv(dataFile)
        remove_spaces(data)
        arenas=listing_arenas(data, 3)
        did_it_work=make_folders(sorted_directory, video, arenas)
        if did_it_work:
            print "We can continue!"
            video_directory=join(png_directory, video)
            list_files=os.listdir(video_directory)
            a_heights, a_widths, b_heights, b_widths, start_frame, end_frame=object_info_setup(data, arenas)        
            crop_top, crop_bottom, crop_left, crop_right=arena_info_setup(data, arenas)
            counter=find_col_min(data, 4) #note that this only works for columns w/o strings
            min_counter=counter        
            arena_counters=[]
            #did_I_make_the_test_image=False
            for y in arenas:
                arena_counters.append(0)
            for x in list_files:
                image_file=join(video_directory,x)
                img = scipy.misc.imread(image_file)
                #if did_I_make_the_test_image==False:
                    #draw_boxes(img, arenas, a_heights, a_widths, b_heights, b_widths, criteria)
                    #did_I_make_the_test_image=True
                #sys.exit("test image")
                
                fixed_image=image_processing(img)
                if counter-min_counter==250:            
                    scipy.misc.imsave(r'E:\081814 Mouse Behavior 1\072714 ORM\ORM testing\Prep data\testingthresh.png', fixed_image)
                for ar_index, ar_name in enumerate(arenas):
                    print counter-min_counter, ar_name 
                    #debugging.write('counter: '+str(counter-min_counter)+' '+ar_name+'\n')
                    if start_frame[ar_index]<=counter<end_frame[ar_index]:               
                        near_a, near_b, near_both=is_mouse_near_object(ar_index, a_heights, a_widths, b_heights, b_widths, criteria, fixed_image)
                        if near_a==True or near_b==True or near_both==True:
                            #print "near an object"                        
                            crop_and_save(near_a, near_b, near_both, img, crop_top, crop_bottom, crop_left, crop_right, sorted_directory, video, ar_index, ar_name, x)
                        else:
                            print "either on or not near an object"
                            #debugging.write("Not near an object\n")
                        arena_counters[ar_index]+=1
                counter+=1
            print "The counters for each arena are:", arena_counters
        else:
            print "There were already sorted images folders made for video",video
        
      