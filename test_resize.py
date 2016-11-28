#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk



class LeftTitle():
    
    def __init__(self,master):
        Entry1=tk.Entry(master)
        Entry1.grid(row=0,column=0)
        
        Btn1=tk.Button(master)
        Btn1.grid(row=0,column=2)
        
        Entry2=tk.Entry(master)
        Entry2.grid(row=0,column=4)
        
        tk.Grid.columnconfigure(master,1,weight=1)
        tk.Grid.columnconfigure(master,3,weight=1)
        

root=tk.Tk()
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)

frame=tk.Frame(root)
frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

LeftTitle(frame)

root.mainloop()        