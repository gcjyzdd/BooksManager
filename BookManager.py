#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import mainWindow

# run once init_db()    
mainWindow.init_db()    

          
root=tk.Tk()
root.title('Book Manager')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frame=tk.Frame(root)
frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

app=mainWindow.mainWindow(frame)
app.poll()

root.mainloop()
        