#!/usr/bin/python
# -*- coding: utf-8 -*-


from os import listdir
from os.path import isfile, join
import os
import re,sys



def load_folder(path):
    print path
    ls=listdir(path)
    for files in ls:
        #print files
        if isfile(path+files):
            fileName,fileExtension = os.path.splitext(files)
            
            print fileName
            print fileExtension
            if re.match('[epub]+|[pdf]+|[mobi]',fileExtension):
                print fileExtension   # Print File Extensions
                print fileName
    




def main():
    load_folder('/home/changjie/Downloads/')
    
    
if __name__=='__main__':
    main()    
    