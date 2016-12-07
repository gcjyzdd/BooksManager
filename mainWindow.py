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
from searchBar import searchBar
from Tags import Tags
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
    '''
     open a book using absolute path
     '''
    
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
    '''
    get all items in a folder.
    '''
    lists=[]
    L=listdir(path)
    
    return [path+i for i in L]
 

def init_db():
    '''
    create database engine to connect to the database.
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
        # set searchBar
        sBar=searchBar(FmLeft);
        sBar.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        sBar.sNameBtn['command']=self.searchName
        sBar.sNameEn.bind('<Return>',lambda event:(self.searchName()))
        sBar.sTagBtn['command']=self.searchTag
        
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
        FmLE=tk.Frame(FmLeft)
        FmLE.grid(row=2,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        totalboks=tk.Label(FmLE,text='%d books in database.' % len(self.booklist))
        totalboks.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W))
        rv=tk.Button(FmLE,text='Reverse',command=self.reverse_order)
        rv.grid(row=0,column=2,sticky=(tk.N,tk.S,tk.E),pady=2)
        FmLE.grid_columnconfigure(1, weight=1)
        
        ####################################Right Frame#############################################################
        FmRR=tk.Frame(FmRight)
        FmRR.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
        
        FmRR1=tk.Frame(FmRR)
        FmRR1.grid(row=0,column=0)
        
        ##show review score, drawed by canvas
        review=review_stars(FmRR1)
        rvCallbacks=map(self.setScore,list(range(5)))
        for i in range(5):
            review.stars[i].bind('<Button-1>',rvCallbacks[i])
        
        
        #button to open the selected book
        read=tk.Button(FmRR,text='Read',command=self.open_callback)
        read.grid(row=0,column=3,sticky=(tk.N,tk.S,tk.E))
        FmRR.grid_columnconfigure(1, weight=1)
                
        ##show tags
        
        
        FmRTags=tk.Frame(FmRight)
        FmRTags.grid(row=2,column=0,sticky=(tk.N,tk.S,tk.E,tk.W),pady=5)
        tags=Tags(FmRTags,'C Python')
        tags.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W))
        tags.setTagEn.bind('<Return>',self.setTag)
        
        
        ##load a folder
        FmRLoad=tk.Frame(FmRight)
        FmRLoad.grid(row=3,column=0,sticky=(tk.N,tk.S,tk.W,tk.E),pady=5)
        
        #load books from a folder and save to database
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
        Btn4=tk.Button(FmRSD,text='Submit edit',command=self.updateDescription)
        Btn4.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        
        ####################The GUI layout is done!###########################
        
        self.FmLeft=FmLeft
        self.FmRight=FmRight
        self.lbx=lbx
        self.sld=sld
        self.review=review
        self.desp=desp
        self.submitDesp=Btn4
        
        self.reverse=rv
        self.sBar=sBar
        self.tags=tags
        self.read=read
        self.EntryFolder=En3
        self.totalbooks=totalboks
        
        # selection of the listbox
        self._sel=''
        self._curSelNum=0
        self._preSel='x'
        self._curID=''
        self._curBook=''
        self._allTags=''    #store all tags of all books
        
        # flag to restore search by name
        self.SNFlag=False
        # set default view
        self.set_default_display()
        
        
    def poll(self):
            self.lbx.after(500, self.poll)            
            ind=self.lbx.curselection()
            
            #get the selected book path
            for a in ind:
                self._curSelNum=a                                                                   
                self._sel=self.showlist[a].path
                self._curID=self.showlist[a].id
                self._curBook=db.select('SELECT * FROM books WHERE id like ?',self.showlist[self._curSelNum].id)[0]
                
                if self._sel!=self._preSel:     
                    self.setDisplay(self.showlist[a].id)
                    #update review,description,tags
                    self._preSel=self._sel
                            
            # stop searching by name and restore the default view
            if len(self.sBar.sNameEn.get())==0 and self.SNFlag:
                self.SNFlag=False
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
            book1 = dict(id=db.next_id(), name=FileName[i], path=PATH[i]+FileName[i]+'.'+EXT[i],
                         description=FileName[i], score=3, tags='',last_modified=time.time())
            db.insert('books', **book1)
        logger.info('Database added %d books.' % len(PATH))
        #add a progress bar here
        self.set_default_display()
        
        pass
    
    def get_booklist(self):
        booklist=db.select('select * from books')
        
        return booklist
    
    def set_default_display(self,sel=0):
        
        self.lbx.delete(0, tk.END)
        for book in self.showlist:
            self.lbx.insert(tk.END,book.path)
        #the default selection is set to 0, i.e., the first book
        self.lbx.select_set(sel)        
        
        self.setDisplay(self.booklist[sel].id)
        self._curBook=db.select('SELECT * FROM books WHERE id like ?',self.booklist[sel].id)[0]
        
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
        self.tags.showTags(book1.tags)
        #self.tags.showTags('C++ Python')
        
        # set total book number
        self.totalbooks['text']='%d books in database.' % len(self.showlist)
        
    def searchName(self):
        self.SNFlag=True
        s=self.sBar.sNameEn.get()
        
        self.showlist=db.select('select * from books where name like ?','%'+s+'%')
        self.set_default_display()
                
    
    def searchTag(self):
        pass   
    
    def updateDescription(self):
        data=self.desp.get(1.0, tk.END)        
        #print data
        #print 'id ',self._curID
        #print 'UPDATE books SET description="%s" where id LIKE "%s"' %(data,self._curID)
        
        db.update('UPDATE books SET description=? where id LIKE ?',data, self._curID)        
        
    
    
    def updateDisplay(self):
        
        pass
    
    
    def test(self,event):
        print 'Entered!!'
        
    
    def setScore(self,i):
        def _wrapper(event):
            self.review.draw(i+1)
            # update score
            db.update('UPDATE books SET score=? where id LIKE ?',i+1,self._curID)
        return _wrapper    
        
    def setTag(self,event):
        print 'hello'
        tag=self.tags.setTagEn.get()
        curTag=db.select('select tags from books where id like ?',self._curID)[0]['tags']
        print tag
        print 'searched:',curTag
        if not re.match('.*('+tag+').*',curTag,re.I):
            print 'Set tag...'
            db.update('UPDATE books SET tags=? WHERE id LIKE ?',curTag+' '+tag,self._curID)
        else:
            print '%s already exists' % tag
        
        self.updateDB()
        self.updateCurBook()
        self.tags.showTags(self._curBook.tags)
        
    def reverse_order(self):
        self.showlist=list(reversed(self.showlist))
        self.set_default_display()
            
    def updateDB(self):
        self.booklist=self.get_booklist()
        if self.SNFlag:
            s=self.sBar.sNameEn.get()
            self.showlist=db.select('select * from books where name like ?','%'+s+'%')
        pass
    
    def updateCurBook(self):
        self._curBook=db.select('SELECT * FROM books WHERE id like ?',self.showlist[self._curSelNum].id)[0]
        