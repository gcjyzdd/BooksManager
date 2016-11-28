#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

class review_stars():
    '''
    create 5 stars showing the review score of a book,
    the user can also set review score for a book 
    '''
    def __init__(self,master):
        print "height2: ",master.winfo_height()
        self.stars=[]
        for i in range(5):
            self.stars.append(tk.Canvas(master,width=20,height=20))
            self.stars[i].grid(row=0,column=i,sticky=(tk.N,tk.S,tk.W,tk.E))
            # set score and write to database
            pass
            
        label=tk.Label(master,text='Reivew')
        label.grid(row=0,column=5,columnspan=3,sticky=(tk.N,tk.S,tk.W,tk.E),padx=10)
        self.label=label
        
        print "height3: ",self.stars[0].winfo_height()
        self.update()
        print "height4: ",self.stars[0].winfo_height()
        self.draw(0)
        
    def draw(self,score):
        print 'height',self.stars[0].winfo_height()
        #coordinates of a star
        verts = [10,40,40,40,50,10,60,40,90,40,65,60,75,90,50,70,25,90,35,60]
        for i in range(len(verts)): 
            verts[i] *=20.0/90#(self.stars[0].winfo_height()/90.0)
        for i in range(score):
            self.stars[i].create_polygon(verts, fill='orange', outline='red')
        
        for i in range(score,5):
            self.stars[i].create_polygon(verts, fill='white', outline='red')
            
    def update(self):
        for i in range(5):
            self.stars[i].update()
        self.label.update()


class FBtn():
    '''
    four buttons, just a test
    '''
    def __init__(self,master):
        self.btns=[]
        for i in range(4):
            self.btns.append(tk.Button(master,text="button"+str(i)))        
            self.btns[i].grid(row=0,column=i)

if __name__=='__main__':
    root=tk.Tk()
    root.title('stars')
    
    FmLeft=tk.Frame(root,bg='white',width=800,height=100,padx=5,pady=5)
    FmLeft.grid(row=0,column=0)
    FmLeft.update()
    
    FmBottom=tk.Frame(root,width=800,height=100)
    FmBottom.grid(row=1,column=0)
    FBtn(FmBottom)
    
    print 'height1: ',FmLeft.winfo_height()
    review_stars(FmLeft)
    root.mainloop()
            