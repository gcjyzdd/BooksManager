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
		self.setTagEn=None
		self.tagLabel=None
		self.labels=[]
		
				
		lb1=tk.Label(self,borderwidth=2,relief="groove",text='Tags:')
		lb1.grid(row=0,column=0,sticky=(tk.N,tk.S,tk.W,tk.E),padx=5,pady=2)
		self.tagLabel=lb1
		
		self.setTagEn=tk.Entry(self,width=6)
		
		self.showTags(tagStr)
		
		pass
	
	def showTags(self,tagStr=None):
		self.destroyLabels()		
		
		# display tags in multiple rows
		i=0
		for item in tagStr.split():			
			self.labels.append(tk.Label(self,borderwidth=2,bg='white',text=item))
			self.labels[-1].grid(row=0,column=i+1,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
			i+=1

		# change position accordingly		
		self.setTagEn.delete(0, tk.END)		
		self.setTagEn.grid(row=0,column=i+1,sticky=(tk.N,tk.S,tk.W),padx=5,pady=2)
		
		
		
		
	def destroyLabels(self):
		'''
		if self.tagLabel:
			self.tagLabel.destroy()
		
		if self.setTagEn:
			self.setTagEn.destroy()
			'''
		for item in self.labels:
			item.destroy()
			

	def setTag(self,event):
		print 'HELLO'
		pass

def testFun(event):
	print 'Hello'
		
def main():
	import time
	root=tk.Tk()
	
	f1=tk.Frame(root,bg='white')
	f2=tk.Frame(root,bg='red')
	f1.grid(row=0,column=0)
	f2.grid(row=1,column=0)
	
	a=Tags(f1,'ABC DEF')
	a.grid(row=0,column=0)
	a.setTagEn.bind('<Return>',a.setTag)
	
	time.sleep(5)
	
	Tags(f2,'DE DD A').grid()
	root.mainloop()
	


if __name__=="__main__":
	main()