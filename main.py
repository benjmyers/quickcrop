from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
Image.MAX_IMAGE_PIXELS = 1000000000

from os import listdir, makedirs
from os.path import isdir, isfile, join

#
FILE_ROOT = '/Users/ben/Documents/stuff/quickcrop/testpics/'#'/Users/ben/odrive/benj.e.myers/Photos'
DESTINATION_DIR = '/Users/ben/Documents/stuff/quickcrop/cropped/'
class Crop():
    def __init__(self):
        self.id = None
        self.x1 = self.x2 = self.y1 = self.y2 = None
        self.entry = None

class QuickCrop(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.window_width = self.winfo_screenwidth()
        self.window_height = self.winfo_screenheight()
        self.minsize(width=self.window_width, height=self.window_height)
        self.maxsize(width=self.window_width, height=self.window_height)
        self.title = "QuickCrop"

        self.croppers = []

        ctr = PanedWindow()
        ctr.pack(fill=BOTH, expand=1)

        ######### Display files
        self.scrollbar = Scrollbar(ctr, orient=VERTICAL)
        self.file_pane = Listbox(ctr, yscrollcommand=self.scrollbar.set)
        self.displayFiles()
        self.scrollbar.config(command=self.file_pane.yview)
        self.scrollbar.pack(side=LEFT, fill=Y)
        self.file_pane.pack(side=LEFT, fill=BOTH, expand=1)

        ctr.add(self.file_pane)

        center_ctr = PanedWindow(ctr)
        ctr.add(center_ctr)

        ######### Drawing
        self.canvas = Canvas(self, width=self.window_width * 0.66, height=self.window_height, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        

        center = Label(center_ctr, text="center")

        center_ctr.add(self.canvas)

        ######### Crop options
        self.input_ctr = Frame(center_ctr)
        center_ctr.add(self.input_ctr)
    
    def loadImage(self, event):
        # Clear out any old croppers
        self.croppers = []

        # Clear out any old inputs
        for widget in self.input_ctr.winfo_children():
            widget.destroy()

        # Clear presets
        self.x = self.y = 0
        self.current_crop = None
        self.rect = None

        self.start_x = None
        self.start_y = None
        self.orig_im_size = None
        self.ratio = None

        self.canvas.delete("all")

        # Add the crop button
        Button(self.input_ctr, text="Crop", command=self.crop).grid(column=1, row=2, sticky=W)

        self.orig_fileName = event.widget.get(event.widget.curselection()[0])
        self.im = Image.open(FILE_ROOT + self.orig_fileName)
        self.thumb = self.im.copy()
        self.orig_im_size = self.im.size

        size = self.window_width * 0.66, self.window_height - 50
        self.thumb.thumbnail(size, Image.ANTIALIAS)
        ## landscape image
        if self.orig_im_size[0] > self.orig_im_size[1]:
            ratio = self.orig_im_size[0] / (self.window_width * 0.66)
            self.ratio = ratio
        else:
            ratio = self.orig_im_size[1] / (self.window_height - 50)
            self.ratio = ratio
        self._draw_image()

    def _draw_image(self):
        self.tk_im = ImageTk.PhotoImage(self.thumb)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

    def displayFiles(self):
        ct = 1
        for file in [f for f in listdir(FILE_ROOT) if isfile(join(FILE_ROOT, f))]:
            if file != '.DS_Store':
                self.file_pane.insert(ct, file)
                ct = ct + 1
        self.file_pane.bind('<<ListboxSelect>>',self.loadImage)

    def addCrop(self):
        input_f = Frame(self.input_ctr)
        Label(input_f, text=str(len(self.croppers)) + ".").grid(column=1, row=1, sticky=W)
        
        entry = Text(input_f, height=1, width=15, bg="grey")
        entry.grid(column=2, row=1, sticky=W)
        self.croppers[self.current_crop].entry = entry
        #Button(input_f, text="x", command=self.removeCrop).grid(column=3, row=1, sticky=W)
        input_f.grid()

    def crop(self):
        print("original image size: " + str(self.orig_im_size))
        for cropper in self.croppers:
            dirName = cropper.entry.get(1.0, END).rstrip()

            if (not isdir(DESTINATION_DIR + dirName)):
                makedirs(DESTINATION_DIR + dirName)

            dirSize = str(len(listdir(DESTINATION_DIR + dirName)))
        
            x1a = cropper.x1 * self.ratio
            x2a = cropper.x2 * self.ratio
            y1a = cropper.y1 * self.ratio
            y2a = cropper.y2 * self.ratio
            print("crop bounds: " + str(x1a) + ", " + str(y1a) + ", " + str(x2a) + ", " + str(y2a))
            box = (x1a, y1a, x2a, y2a)
            region = self.im.crop(box)
            region.save(DESTINATION_DIR + dirName + "/" + dirName + "_" + dirSize + ".jpeg")
        print("DONE")

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create a new crop object
        c = Crop()
        c.id = len(self.croppers)
        self.current_crop = c.id
        c.x1 = event.x
        c.y1 = event.y
        self.croppers.append(c)

        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline="red", width=2)


    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.croppers[self.current_crop].x2 = event.x
        self.croppers[self.current_crop].y2 = event.y
        self.addCrop()
        self.canvas.create_text(self.croppers[self.current_crop].x1, self.croppers[self.current_crop].y1, text=str(len(self.croppers)))
        pass


if __name__ == "__main__":
    app = QuickCrop()
    app.mainloop()