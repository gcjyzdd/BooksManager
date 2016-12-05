#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__="Changjie Guan"

import Tkinter as tk


class Tags(tk.Frame):
	'''
	Define a tag class that shows tags dynamically and set/update tags 
	'''
	
	def __init__(self,master,tagStr=''):
		self.master=master
		tk.Frame.__init__(self, master)
		
		self.showTags(tagStr)
		
		pass
	
	def showTags(self,tagStr=None):
		lb1=tk.Label(self,borderwidth=2,relief="groove",text='Tags:')
		lb1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E),padx=5,pady=2)
		
		
		self.tagLabel=lb1
		
		# display tags in multiple rows
		i=0
		for item in tagStr.split():
			tk.Label(self,borderwidth=2,bg='white',text=item).grid(row=0,column=i+1,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
			i+=1
			pass
		pass
		
		# change position accordingly
		en1=tk.Entry(self)
		en1.grid(row=0,column=i+1,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
		
		self.setTagEn=en1
		
	def setTag(self):
		pass
	
def main():
	root=tk.Tk()
	
	a=Tags(root,'ABC DEF')
	a.grid(row=0,column=0)
	
	root.mainloop()
	


if __name__=="__main__":
	main()