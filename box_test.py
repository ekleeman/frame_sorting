
"""
Created on Mon Sep 01 10:40:57 2014

@author: Elise
"""
import cv2
import scipy.misc
import csv

#change this!! (1/4)
imgFile=r'E:\081814 Mouse Behavior\alpha2KO Experiment 1\072714 alpha2 KO exp1 ORM\ORM\hopefully all the videos\Object recognition, alpha2 experiment 1 videos\ORM testing\PNGs\C\C01000.png'
img = scipy.misc.imread(imgFile)

#change this!! (2/4)
dataFile=r'E:\081814 Mouse Behavior\alpha2KO Experiment 1\072714 alpha2 KO exp1 ORM\ORM\hopefully all the videos\Object recognition, alpha2 experiment 1 videos\ORM testing\C_Results.csv'
with open(dataFile, 'rb') as csvfile:
    data=list(csv.reader(csvfile))

#change this!! (3/4)
folders = 'C1', 'C2', 'C3', 'C4'

for arena in folders:
    
    if (arena==folders[0]):
        A_Height=int(data[1][2])
        A_Width=int(data[1][1])
        B_Height=int(data[2][2])
        B_Width=int(data[2][1])
        startFrame=int(data[1][3])
        endFrame=int(data[1][3])+int(data[1][4])
    elif (arena==folders[1]):
        A_Height=int(data[3][2])
        A_Width=int(data[3][1])
        B_Height=int(data[4][2])
        B_Width=int(data[4][1])
        startFrame=int(data[2][3])
        endFrame=int(data[2][3])+int(data[1][4])
    elif (arena==folders[2]):
        A_Height=int(data[5][2])
        A_Width=int(data[5][1])
        B_Height=int(data[6][2])
        B_Width=int(data[6][1])
        startFrame=int(data[3][3])
        endFrame=int(data[3][3])+int(data[1][4])
    elif (arena==folders[3]):
        A_Height=int(data[7][2])
        A_Width=int(data[7][1])
        B_Height=int(data[8][2])
        B_Width=int(data[8][1])
        startFrame=int(data[4][3])
        endFrame=int(data[4][3])+int(data[1][4])

    #for the coordinates, cv2 does width first:
    cv2.rectangle(img, (A_Width-31,A_Height-35), (A_Width+31,A_Height+35), (0,0,255))  
    cv2.rectangle(img, (B_Width-31,B_Height-35), (B_Width+31,B_Height+35), (0,0,255))   
    cv2.rectangle(img, (A_Width-11,A_Height-11), (A_Width+11,A_Height+11), (0,0,255))
    cv2.rectangle(img, (B_Width-11,B_Height-11), (B_Width+11,B_Height+11), (0,0,255))

#change this!! (4/4)
scipy.misc.imsave(r'E:\081814 Mouse Behavior\alpha2KO Experiment 1\072714 alpha2 KO exp1 ORM\ORM\hopefully all the videos\Object recognition, alpha2 experiment 1 videos\ORM testing\C_boxTest.png', img)
