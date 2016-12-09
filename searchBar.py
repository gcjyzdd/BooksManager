#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="Changjie Guan"

import Tkinter as tk
from entry_auto_completion import AutocompleteEntry

class searchBar(tk.Frame):
    '''
    define a search bar for book manager. It supports search-by-name and search-by-tag
    '''
    def __init__(self,master,listAuto,**kw):
        #self.master=master
        #apply(tk.Frame.__init__,(self,master),kw)
        tk.Frame.__init__(self, master, **kw)
        en1=tk.Entry(self)
        en1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
        
        btn1=tk.Button(self,text='Search name')
        btn1.grid(row=0,column=1,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
                
        #en2=tk.Entry(self)
        en2=AutocompleteEntry(self,listAuto)
        en2.grid(row=0,column=3,sticky=(tk.N,tk.S,tk.E),padx=5,pady=2)
        
        btn2=tk.Button(self,text='Search Tag')
        btn2.grid(row=0,column=4,sticky=(tk.N,tk.S,tk.E),padx=5,pady=2)
        
        self.grid_columnconfigure(2, weight=1)
        
        self.sNameEn=en1
        self.sNameBtn=btn1
        self.sTagEn=en2
        self.sTagBtn=btn2
            

def main():
    root=tk.Tk()
    root.title("SearchBar")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    frame=tk.Frame(root,bg='yellow')
    frame.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
    frame.grid_columnconfigure(0,weight=1)
    
    f1=tk.Frame(frame,bg='white')
    f2=tk.Frame(frame)
    f1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
    f2.grid(row=1,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
    
    f1.grid_columnconfigure(0,weight=1)
    f2.grid_columnconfigure(0,weight=1)
    
    a=searchBar(f1)
    b=searchBar(f2)
    a.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
    b.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E))
    
    root.mainloop()
    

if __name__=="__main__":
    main() 