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
import copy
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
    print path
    fn,ext=os.path.splitext(path)
    
    if re.match('.*(pdf)', ext, re.I):
        print ext
        p=subprocess.Popen(['/usr/bin/evince',path])
        print p.pid
    if re.match('.*(epub|mobi|azw3)', ext, re.I):
        p=subprocess.Popen(['/usr/bin/ebook-viewer',path,'&'])
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
    create database engine
    '''
    db.create_engine('testuser', 'test623', 'bookmanager')
    # uncomment the following code when running the first time to create a table
    #db.update('drop table if exists books')
    #db.update('create table books (id varchar(50) primary key, name text, path text, description text, score int, tags text, last_modified real)')

    
class mainWindow():
    
    def __init__(self,master):
        self.master=master
        
        #load books from database
        self.booklist=self.get_booklist()
        
        #showlist is the book list shwon in the listbox
        self.showlist=copy.deepcopy(self.booklist)        
        
        ##layout components
        #FmLeft:left frame
        FmLeft=tk.Frame(master,width=400,height=500)
        FmLeft.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmLeft.grid_columnconfigure(0,weight=1)
        FmLeft.grid_rowconfigure(1,weight=1)
        
        #FmRight: right frame
        FmRight=tk.Frame(master,width=300,height=500)
        FmRight.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmRight.grid_columnconfigure(0,weight=1)
        FmRight.grid_rowconfigure(0,weight=1)
        
        #make window resizable
        master.grid_columnconfigure(0,weight=2)
        master.grid_columnconfigure(1,weight=1)
        master.grid_rowconfigure(0,weight=1)
        
        #### to do ####
        # write some subclasses to layout this main window into modules
        ###################################Left Frame###########################################
        ## search entry and button
        #FmLS: search bar on the Left Frame
        FmLS=tk.Frame(FmLeft)
        FmLS.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        En1=tk.Entry(FmLS,text="Search")
        En1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
        
        Btn1=tk.Button(FmLS,text='Search name',command=self.searchName)
        Btn1.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
        
        En2=tk.Entry(FmLS)
        En2.grid(row=0,column=3,sticky=(tk.N,tk.S,tk.E),padx=5,pady=2)
        
        Btn2=tk.Button(FmLS,text='Search tags',command=self.searchTag)
        Btn2.grid(row=0,column=4,sticky=(tk.N,tk.S,tk.E),padx=5,pady=2)
        
        #make the bar resizable
        FmLS.grid_columnconfigure(2, weight=1)
        
        ##scrollbar and listbox
        #FmLL: Listbox on the Left Frame
        FmLL=tk.Frame(FmLeft)
        FmLL.grid(row=1,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmLL.grid_columnconfigure(0,weight=1)
        FmLL.grid_rowconfigure(0,weight=1)
        
        sld=tk.Scrollbar(FmLL)
        lbx=tk.Listbox(FmLL)
        
        sld['command']=lbx.yview
        lbx['yscrollcommand']=sld.set
        lbx['width']=80
        
        #for book in self.booklist:
        #    lbx.insert(tk.END,book.path)
        #the default selection is set to 0, i.e., the first book
        #lbx.select_set(0)
        
        lbx.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        sld.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W,tk.E))
        lbx.grid_rowconfigure(0, weight=1)
        sld.grid_rowconfigure(0, weight=1)
        
        #show total book number
        totalboks=tk.Label(FmLeft,text='%d books in database.' % len(self.booklist))
        totalboks.grid(row=2,column=0,sticky=(tk.N,tk.S,tk.W))
        ####################################Right Frame#############################################################
        FmRR=tk.Frame(FmRight)
        FmRR.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        FmRR1=tk.Frame(FmRR)
        FmRR1.grid(row=0,column=0)
        
        ##show review score, drawed by canvas
        review=review_stars(FmRR1)
        #button to open the selected book
        read=tk.Button(FmRR,text='Read',command=self.open_callback)
        read.grid(row=0,column=3,sticky=(tk.N,tk.S,tk.E))
        FmRR.grid_columnconfigure(1, weight=1)
                
        ##show tags
        FmRTags=tk.Frame(FmRight)
        FmRTags.grid(row=2,column=0,sticky=(tk.N,tk.S,tk.E,tk.W),pady=5)
        labelTag=tk.Label(FmRTags,text='Tags:')
        labelTag.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W))
        tags=tk.Label(FmRTags,bg='gray')
        tags.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W))

        
        ##load a folder
        FmRLoad=tk.Frame(FmRight)
        FmRLoad.grid(row=3,column=0,sticky=(tk.N,tk.S,tk.W,tk.E),pady=5)
        
        #load books from a folder to database
        Lb1=tk.Label(FmRLoad,text='Load folder:')
        En3=tk.Entry(FmRLoad)
        Btn3=tk.Button(FmRLoad,text='Load',command=self.load_folder)
        
        Lb1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        En3.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W,tk.E))
        Btn3.grid(row=0,column=2,sticky=(tk.N,tk.S,tk.W,tk.E))
        FmRLoad.grid_columnconfigure(1, weight=1)
        
        ##description
        desp=tk.Text(FmRight)
        desp.insert(tk.INSERT, '编程啊,快来呀...Hello, this is a book. sdflnklsdfnm,.sdfnmwepfjpcmwmfs.,dnc pi\n')
        desp.insert(tk.END,'Goodbye!')
        desp['width']=40
        desp.grid(row=4,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        ##edit and submit description
        FmRSD=tk.Frame(FmRight)
        FmRSD.grid(row=5,column=0)
        Btn4=tk.Button(FmRSD,text='Submit edit')
        Btn4.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        
        ####################The GUI layout is done!###########################
        
        self.FmLeft=FmLeft
        self.FmRight=FmRight
        self.lbx=lbx
        self.sld=sld
        self.review=review
        self.desp=desp
        
        self.SName=En1
        self.STag=En2
        self.tags=tags
        self.read=read
        self.EntryFolder=En3
        self.totalbooks=totalboks
        
        # selection of the listbox
        self._sel=''
        
        # set default view
        self.set_default_display()
        
        
    def poll(self):
            self.lbx.after(500, self.poll)            
            ind=self.lbx.curselection()
            
            #get the selected book path
            for a in ind:
                self._sel=self.showlist[a].path
                self.setDisplay(self.showlist[a].id)
                #update review,description,tags
            
            # stop searching by name and restore the default view
            if len(self.SName.get())==0:
                self.showlist=copy.deepcopy(self.booklist)
                self.set_default_display()
                
    def open_callback(self):
        '''
        open an ebook, in formats: pdf,epub,mobi,azw3
        '''
        try:
            _open_ebook(self._sel)
        except:
            print "Please select a book first."       
    
    def load_folder(self):
        '''
        Get ebooks from a folder and add them to database.
        '''
        path=self.EntryFolder.get()
        if not isdir(path):
            print 'The folder is not valid!'
            return 1
        logger.info('Database loads folder : %s' % path)
        print path
        PATH,FileName,EXT=load_folder(path)
        
        for i in range(len(PATH)):
            #db.update('create table books (id text primary key, name text, path text, description text, score int, tags text, last_modified real)')
            book1 = dict(id=db.next_id(), name=FileName[i], path=PATH[i]+FileName[i]+'.'+EXT[i],
                         description=FileName[i], score=3, tags='',last_modified=time.time())
            db.insert('books', **book1)
        logger.info('Database added %d books.' % len(PATH))
        #add a progress bar here
        pass
    
    def get_booklist(self):
        booklist=db.select('select * from books')
        
        return booklist
    
    def set_default_display(self):
        
        self.lbx.delete(0, tk.END)
        for book in self.showlist:
            self.lbx.insert(tk.END,book.path)
        #the default selection is set to 0, i.e., the first book
        self.lbx.select_set(0)        
        
        self.setDisplay(self.booklist[0].id)
        
    def setDisplay(self,id):
        #print 'id =',id
        book1=db.select_one("select * from books where id like '%s'" % id)
        
        # set description
        self.desp.delete('1.0', tk.END)
        #print book1.description
        self.desp.insert(tk.INSERT,book1.description)
        
        # set score
        self.review.draw(book1.score)
        
        # set tags
        self.tags['text']=book1.tags
        
        # set total book number
        self.totalbooks['text']='%d books in database.' % len(self.showlist)
        
    def searchName(self):
        s=self.SName.get()
        self.showlist=db.select('select * from books where name like ?','%'+s+'%')
        self.set_default_display()
        
        pass
    
    def searchTag(self):
        pass   
    
# run once init_db()    
init_db()    

          
root=tk.Tk()
root.title('Book Manager')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frame=tk.Frame(root)
frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

app=mainWindow(frame)
app.poll()

root.mainloop()
        
