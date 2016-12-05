import os

from subprocess import call

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

expw = 1.0
satw = 0.2
conw = 0.0
outname = "Test.jpg"
jpgquality = 92

root = Tk()

numfiles = StringVar()
numfiles.set("0")

def run():
  filelist = treeview.get_children()
  for filen in filelist:
    if not ("jpg" in filen or "jpeg" in filen):
      messagebox.showerror("Filetype","Cannot process file %s. Please provide only jpg image files." % filen.split("/")[-1])
      return
  call(["align_image_stack", "-v", "-C", "-aalign"] + list(filelist))
  alignfilelist = []
  for element in range(len(filelist)):
    alignfilelist += ["align"+'{0:04d}'.format(element)+".tif",]
  call(["enfuse","--exposure-weight="+str(expw),"--saturation-weight="+str(satw),"--contrast-weight="+str(conw),"--output="+outname.replace("jpg","tif")]+alignfilelist)
  call(["convert","-quality",str(jpgquality),outname.replace("jpg","tif"),outname])
  call(["rm",outname.replace("jpg","tif")]+alignfilelist)

def selectfiles():
  filelist = filedialog.askopenfilenames(initialdir=os.getenv("PWD"))
  for filen in filelist:
    itemname = filen.split("/")[-1]
    if not treeview.exists(filen):
      treeview.insert('','end',filen,text=itemname)
  updatenumfiles()

def removefiles():
  for item in treeview.selection():
    treeview.delete(item)
  updatenumfiles()

def updatenumfiles():
  filelist = treeview.get_children()
  numfiles.set(str(len(filelist)))
  if int(len(filelist)) > 1:
    runButton.state(['!disabled'])
  else:
    runButton.state(['disabled'])

ttk.Label(root, text="Select at least 2 image files").grid(row=0,columnspan=2)

loadButton = ttk.Button(root, text="Add Files", command=selectfiles)
loadButton.grid(column=0,row=2)

deleteButton = ttk.Button(root, text="Remove Selected", command=removefiles)
deleteButton.grid(column=1,row=2)

treeview = ttk.Treeview(root)
treeview.grid(columnspan=2, row=1)
treeview.heading("#0",text="Selected files")

ttk.Label(root, textvariable=numfiles).grid(column=0,row=3)
ttk.Label(root, text="files selected").grid(column=1,row=3)


runButton = ttk.Button(root, text="Do Something", command=run,state='disabled')
runButton.grid(columnspan=2,row=4)

root.mainloop()
