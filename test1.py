#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys# os list files and change file names
import time # sleep, count time
import platform
import random# generate random number and choose randomly
import re, json
import json
from os import listdir
from os.path import isfile, join
from multiprocessing import Pool# apply pool to utilize multiprocess
import subprocess# run bash
import Tkinter as tk

#subprocess.call(['/usr/bin/nautilus','/home/changjie/MyProjects/'])

def open_ebook(path):
    # use absolute path
    p=subprocess.Popen(['/usr/bin/ebook-viewer',str(path),'&'])
    print p.pid

def test_open_ebooks():
    open_ebook('/home/changjie/Downloads/Python进阶.epub')
    subprocess.call(['/usr/bin/nautilus','/home/changjie/MyProjects/'])

def get_book_list(path):
    lists=[]
    L=listdir(path)
    for i in L:
        #print i
        lists.append(path+i)
    return lists       

path1='/home/changjie/Downloads/Python进阶.epub'
path2='/home/changjie/Downloads/KanCloud2/'


    
class tab1():
    
    def __init__(self,master):    
        self.F1=tk.Frame()
        self.s=tk.Scrollbar(self.F1)
        self.l=tk.Listbox(self.F1)
        
        self.s.pack(side=tk.RIGHT,fill=tk.Y)
        self.l.pack(side=tk.LEFT,fill=tk.Y)
        
        self.s['command']=self.l.yview
        self.l['yscrollcommand']=self.s.set
        self.l['width']=80
        
        self.lists=get_book_list(path2)
        
        for i in self.lists:
            self.l.insert(tk.END,i)
        
        self.F1.pack(side=tk.TOP)
        
        self.F2=tk.Frame(master)
        self.lb=tk.Label(self.F2)
        
        self.lb.pack()
        self.F2.pack(side=tk.TOP)
        self.poll()
        
    
    def poll(self):
        self.lb.after(200,self.poll)
        sel=self.l.curselection()
        self.lb.config(text=sel)
    
    def open_path(self):
        pass
    
    def search_str(self):
        pass
    
def main():
    top=tk.Tk()    
    top.title='Books Manager'
    fm=tk.Frame(top,width=800,height=1800)
    tab1(fm)
    top.mainloop()
    
if __name__=='__main__':
    main()


get_book_list(path2)

