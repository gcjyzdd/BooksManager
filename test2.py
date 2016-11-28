#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
from os import listdir
import subprocess# run bash
import os,re

def open_ebook(path):
    # use absolute path
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

_sel=''

def poll():
    lbx.after(500, poll)
    global _sel
    ind=lbx.curselection()
    for a in ind:
        _sel=booklist[a]
        
def open_callback():
    open_ebook(_sel)

        
path1='/home/changjie/Downloads/Python进阶.epub'
path2='/home/changjie/Downloads/KanCloud2/'

root=tk.Tk()
root.title('Books Manager!')
content=tk.Frame(root)


en1=tk.Entry(content)
bt1=tk.Button(content)
bt1['text']='Search'

sld=tk.Scrollbar(content)
lbx=tk.Listbox(content)

sld['command']=lbx.yview
lbx['yscrollcommand']=sld.set
lbx['width']=80

booklist=get_book_list(path2)
for i in booklist:
    lbx.insert(tk.END,str(i))


l1=tk.Label(content)
l1['text']='5 stars'

desp=tk.Text(content)
desp.insert(tk.INSERT, '编程啊,快来呀...Hello, this is a book. sdflnklsdfnm,.sdfnmwepfjpcmwmfs.,dnc pi')
desp.insert(tk.END,'Goodbye!')
desp['width']=40

bt2=tk.Button(content,command=open_callback)
bt2['text']='Open'

# grid frame1
content.grid(column=0,row=0)

en1.grid(row=0,columnspan=5,sticky=(tk.W,tk.N,tk.S))
bt1.grid(row=0,column=5,columnspan=2,sticky=(tk.E,tk.N))
lbx.grid(row=1,column=0,rowspan=6,columnspan=6,sticky=(tk.W,tk.N,tk.S))
sld.grid(row=1,column=6,rowspan=6,sticky=(tk.N,tk.S,tk.E))

# grid frame2
l1.grid(row=0,column=7,columnspan=3,sticky=(tk.W,tk.E))
desp.grid(row=1,column=7,columnspan=3,rowspan=3,sticky=(tk.N,tk.S,tk.W,tk.E))
bt2.grid(row=4,column=7,columnspan=3)
#bt2['command']=open_callback(_sel)

poll()

root.mainloop()
