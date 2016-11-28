#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
from os import listdir
from os.path import isdir,isfile
import subprocess# run bash
import os,re
import time
import logging
import logging.handlers

from review_stars import review_stars
from load_books import load_folder
import db

## set log
LOG_FILE = 'tst.log'  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # instantialize handler   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
  
formatter = logging.Formatter(fmt)   # instantialize formatter  
handler.setFormatter(formatter)      # set formatter  
  
logger = logging.getLogger('tst')    # get/load logger  
logger.addHandler(handler)           # add handler  
logger.setLevel(logging.DEBUG)  

def _open_ebook(path):
    # open a book using absolute path
    print 'path 1 ',path
    fn,ext=os.path.splitext(path)
    
    if re.match('.*(pdf)', ext, re.I):
        p=subprocess.Popen(['/usr/bin/evince',str(path)])
        print p.pid
    if re.match('.*(epub|mobi|azw3)', ext, re.I):
        p=subprocess.Popen(['/usr/bin/ebook-viewer',str(path),'&'])
        print p.pid
    
    
def get_book_list(path):
    lists=[]
    L=listdir(path)
    
    for i in L:
        #print i
        lists.append(path+i)
    return lists   

def init_db():
    '''
    initialize database. Run only once.
    '''
    db.create_engine('testuser', 'test623', 'bookmanager')
    db.update('drop table if exists books')

    db.update('create table books (id varchar(50) primary key, name text, path text, desciption text, score int, tags text, last_modified real)')

    
class mainWindow():
    
    def __init__(self,master):
        self.master=master
        
        #layout components
        FmLeft=tk.Frame(master,width=400,height=500)
        FmLeft.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmLeft.grid_columnconfigure(0,weight=1)
        FmLeft.grid_rowconfigure(1,weight=1)
        
        FmRight=tk.Frame(master,width=300,height=500)
        FmRight.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmRight.grid_columnconfigure(0,weight=1)
        FmRight.grid_rowconfigure(0,weight=1)
        
        master.grid_columnconfigure(0,weight=2)
        master.grid_columnconfigure(1,weight=1)
        master.grid_rowconfigure(0,weight=1)
        ###################################Left Frame###########################################
        # search entry and button
        FmLS=tk.Frame(FmLeft)
        FmLS.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        En1=tk.Entry(FmLS,text="Search")
        En1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
        
        Btn1=tk.Button(FmLS,text='Search name')
        Btn1.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
        
        En2=tk.Entry(FmLS)
        En2.grid(row=0,column=3,sticky=(tk.N,tk.S,tk.E),padx=5,pady=2)
        
        Btn2=tk.Button(FmLS,text='Search tags')
        Btn2.grid(row=0,column=4,sticky=(tk.N,tk.S,tk.E),padx=5,pady=2)
        
        FmLS.grid_columnconfigure(2, weight=1)
        
        #scrollbar and listbox
        FmLL=tk.Frame(FmLeft)
        FmLL.grid(row=1,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmLL.grid_columnconfigure(0,weight=1)
        FmLL.grid_rowconfigure(0,weight=1)
        
        sld=tk.Scrollbar(FmLL)
        lbx=tk.Listbox(FmLL)
        
        sld['command']=lbx.yview
        lbx['yscrollcommand']=sld.set
        lbx['width']=80
        
        for i in booklist:
            lbx.insert(tk.END,str(i))
        #the default selection is set to 0, i.e., the first book
        lbx.select_set(0)
        lbx.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        sld.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W,tk.E))
        lbx.grid_rowconfigure(0, weight=1)
        sld.grid_rowconfigure(0, weight=1)
        
        #show total book number
        totalboks=tk.Label(FmLeft,text='%d books in database.' % len(booklist))
        totalboks.grid(row=2,column=0,sticky=(tk.N,tk.S,tk.W))
        ####################################Right Frame#############################################################
        FmRR=tk.Frame(FmRight)
        FmRR.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        FmRR1=tk.Frame(FmRR)
        FmRR1.grid(row=0,column=0)
        
        #show review score, drawed by canvas
        review=review_stars(FmRR1)
        
        #button to open the selected book
        read=tk.Button(FmRR,text='Read',command=self.open_callback)
        read.grid(row=0,column=2,sticky=(tk.N,tk.S,tk.E))
        FmRR.grid_columnconfigure(1, weight=1)
        
        FmRLoad=tk.Frame(FmRight)
        FmRLoad.grid(row=2,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        #load books from a folder to database
        Lb1=tk.Label(FmRLoad,text='Load folder:')
        En3=tk.Entry(FmRLoad)
        Btn3=tk.Button(FmRLoad,text='Load',command=self.load_folder)
        
        Lb1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        En3.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W,tk.E))
        Btn3.grid(row=0,column=2,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmRLoad.grid_columnconfigure(1, weight=1)
        
        
        desp=tk.Text(FmRight)
        desp.insert(tk.INSERT, '编程啊,快来呀...Hello, this is a book. sdflnklsdfnm,.sdfnmwepfjpcmwmfs.,dnc pi\n')
        desp.insert(tk.END,'Goodbye!')
        desp['width']=40
        desp.grid(row=3,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        
        self.FmLeft=FmLeft
        self.FmRight=FmRight
        self.lbx=lbx
        self.sld=sld
        self.read=read
        self.EntryFolder=En3
        # selection of the listbox
        self._sel=''

    def poll(self):
            self.lbx.after(500, self.poll)            
            ind=self.lbx.curselection()
            for a in ind:
                self._sel=booklist[a]
                #update review,description,tags

    def open_callback(self):
        try:
            _open_ebook(self._sel)
        except:
            print "Please select a book first."       
    
    def load_folder(self):
        path=self.EntryFolder.get()
        if not isdir(path):
            print 'The folder is not valid!'
            return 1
        logger.info('Database loads folder : %s' % path)
        print path
        PATH,FileName,EXT=load_folder(path)
        
        for i in range(len(PATH)):
            #db.update('create table books (id text primary key, name text, path text, desciption text, score int, tags text, last_modified real)')
            book1 = dict(id=db.next_id(), name=FileName[i], path=PATH[i]+FileName[i]+'.'+EXT[i],
                         desciption=FileName[i], score=3, tags='',last_modified=time.time())
            db.insert('books', **book1)
        logger.info('Database added %d books.' % len(PATH))
        #add a progress bar here
        pass
    
    def get_booklist(self):
        pass

# run once init_db()    
#init_db()    

path1='/home/changjie/Downloads/Python进阶.epub'
path2='/home/changjie/Downloads/KAN/KanCloud3/'
booklist=get_book_list(path2)
             
root=tk.Tk()
root.title('Book Manager')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frame=tk.Frame(root)
frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

app=mainWindow(frame)
app.poll()

root.mainloop()
        
