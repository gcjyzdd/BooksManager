#!/usr/bin/python
# -*- coding: utf-8 -*-


from os import listdir
from os.path import isfile,isdir, join,split
import os
import re,sys


def load_folder(path):
    '''
    Load all files/directories in a path,
    and determine if they are ebooks, i.e., pdf, epub, mobi, or azw3 format.
    Return ebooks list.
    '''
    #print path
    if path[-1]!='/':
        path+='/'    
    ls=listdir(path)
    FN=[]
    EXT=[]
    PATH=[]
    for files in ls:
        #print files
        if isfile(join(path,files)):
            #print path+files
            fileName,fileExtension = os.path.splitext(files)
            
            #print fileName
            #print fileExtension
            if re.match('.(epub|pdf|mobi|azw3)',fileExtension,re.I):
                #print fileExtension   # Print File Extensions
                #print fileName
                
                FN.append(fileName)
                EXT.append(fileExtension[1:])
                PATH.append(path)
        if isdir(path+files):
            #print path+files
            A,B,C=load_folder(join(path,files))
            PATH+=A
            FN+=B
            EXT+=C
                    
    return PATH,FN,EXT

def filterFineName(path,name_list,ext_list):
    '''
    Filter filename containing special characters, like【】$, etc.
    '''
    
    pattern="[\s+\.\(\)\!\[\],\:$\^\']+|[——！（）？￥”“［］【】·；：，「～#%。《》]".decode('utf-8')
    for i in range(len(name_list)):        
        print name_list[i]
        newstr=re.sub(pattern,''.decode('utf-8'),name_list[i])
        print newstr
        os.rename(path+name_list[i]+'.'+ext_list[i], path+newstr+'.'+ext_list[i])
        
def filterBookName(name):
    '''
    Filter filename containing special characters, like【】$, etc.
    '''
    path,filename=split(name)
    fileName,fileExtension = os.path.splitext(filename)
    
    pattern="[\s+\.\(\)\!\[\],\:$\^\']+|[——！（）？￥”“［］【】·•、；：，「～#%。《》]".decode('utf-8')
    newstr=re.sub(pattern,''.decode('utf-8'),fileName.decode('utf-8'))
    os.rename(name,join(path,newstr)+fileExtension)
        
def move_files(dir1,nameList,extList,dir2):
    for i in range(len(nameList)):
        os.rename(dir1+nameList[i]+'.'+extList[i], dir2+nameList[i]+'.'+extList[i])

def changeName(path):
    #print 'path : ',path
    if path[-1]!='/':
        path+='/'
    for item in listdir(path):
        print item
        if not re.match(r'.*\..*',item):
            if re.match('.*pdf',item):
                os.rename(path+item, path+item[0:-3]+'.pdf')
                continue
            if re.match('.*epub',item):
                os.rename(path+item, path+item[0:-4]+'.epub')
                continue
            if re.match('.*mobi',item):
                os.rename(path+item, path+item[0:-4]+'.mobi')
                continue

def removeName(path,rmstr):
    
    if path[-1]!='/':
        path+='/'
    for item in listdir(path):
        print item
        os.rename(path+item,path+re.sub(rmstr,'',item.decode('utf-8')))#.decode('utf-8')

def dels(path):
    if path[-1]!='/':
        path+='/'
    for item in listdir(path):
        print item
        os.rename(path+item,path+item[1:])
                
def main():
    path='/home/changjie/Downloads/'
    path2='/home/changjie/Downloads/downloaded_ebooks/'
    FN,EXT=load_folder(path)
    #for i in range(len(FN)):
        #print FN[i]+'.'+EXT[i]
    filterFineName(path, FN, EXT)
    
    FN,EXT=load_folder(path)
    
    move_files(path, FN, EXT, path2)
    
def main2():
    #path='/home/changjie/Downloads/KanCloud2/' 
    path=r'/home/changjie/Downloads/'#.decode('utf-8')
    #changeName(path)
    #removeName(path, 'KanCloud3')
    #dels(path)
    #return 0
  
    PATH,FN,EXT=load_folder(path)
    #for i in range(len(FN)):
        #print FN[i]+'.'+EXT[i]
    #filterFineName(path, FN, EXT)
    for i in range(len(PATH)):
        print PATH[i]+'  '+FN[i]+'  '+EXT[i] 
        filterBookName(join(PATH[i],FN[i])+'.'+EXT[i])
    print '%d books found in this folder' % len(PATH)
    
    
if __name__=='__main__':
    main2()
    #main()    
    
