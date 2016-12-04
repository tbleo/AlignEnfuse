import os

from subprocess import call

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

expw = 1.0
satw = 0.2
conw = 0.0
outname = "Test.jpg"
jpgquality = 92

root = Tk()

filelist = () 

numfiles = StringVar()
numfiles.set("0")

def run():
  call(["align_image_stack", "-v", "-C", "-aalign"] + list(filelist))
  alignfilelist = []
  for element in range(len(filelist)):
    alignfilelist += ["align"+'{0:04d}'.format(element)+".tif",]
  call(["enfuse","--exposure-weight="+str(expw),"--saturation-weight="+str(satw),"--contrast-weight="+str(conw),"--output="+outname.replace("jpg","tif")]+alignfilelist)
  call(["convert","-quality",str(jpgquality),outname.replace("jpg","tif"),outname])
  call(["rm",outname.replace("jpg","tif")]+alignfilelist)

def selectfiles():
  global filelist
  filelist = filedialog.askopenfilenames(initialdir=os.getenv("PWD"))
  numfiles.set(str(len(filelist)))
  if int(len(filelist)) > 1:
    runButton.state(['!disabled'])
  else:
    runButton.state(['disabled'])

ttk.Label(root, textvariable=numfiles).grid(column=1,row=2)
ttk.Label(root, text="files selected").grid(column=2,row=2)

loadButton = ttk.Button(root, text="Select Files", command=selectfiles)
loadButton.grid(column=1,row=2)

runButton = ttk.Button(root, text="Do Something", command=run,state='disabled')
runButton.grid(column=2,row=3)

treeview = ttk.Treeview(root)
treeview.grid(column=1, row=1)

root.mainloop()
