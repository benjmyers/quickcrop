from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
Image.MAX_IMAGE_PIXELS = 1000000000

from os import listdir
from os.path import isfile, join


def crop():
    print("CROP!")

root = Tk()
root.title("QuickCrop")

m1 = PanedWindow()
m1.pack(fill=BOTH, expand=1)

left = Label(m1, text="left pane")
mypath = '/Users/ben/odrive/benj.e.myers/Photos'
ct = 1
for file in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
    ttk.Label(left, text=file).grid(column=1, row=ct, sticky=W)
    ct = ct + 1
m1.add(left)

m2 = PanedWindow(m1)
m1.add(m2)

center = Label(m2, text="center")


#Create a canvas
canvas = Canvas(root, width=600, height=800)
canvas.pack()

size = 600, 800

# Load the image file
im = Image.open('/Users/ben/odrive/benj.e.myers/Photos/wrm_mrk.jpeg')
im.thumbnail(size)
# Put the image into a canvas compatible class, and stick in an
# arbitrary variable to the garbage collector doesn't destroy it
canvas.image = ImageTk.PhotoImage(im)
# Add the image to the canvas, and set the anchor to the top left / north west corner
canvas.create_image(0, 0, image=canvas.image, anchor='nw')


m2.add(canvas)

# #The Pack geometry manager packs widgets in rows or columns.
#center.pack(side = "bottom", fill = "both", expand = "yes")

right = Label(m2, text="left")
m2.add(right)

ttk.Button(right, text="Crop", command=crop).grid(column=3, row=3, sticky=W)

root.mainloop()