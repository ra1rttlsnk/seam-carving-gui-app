import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import matplotlib.pyplot as plt
import numpy as np
import SeamCarver

class GUI(tk.Frame):
    def __init__(self, parent = None):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.img_path = ''
        self.save_path = ''

        self.frame0 = tk.Frame(self, bd = 10)
        self.frame0.pack()
        self.path_label = tk.Label(self.frame0, text = '')
        self.path_label.pack(side='left')
        self.browseButton = tk.Button(self.frame0, text = 'Browse', command = self.openfile)
        self.browseButton.pack(side = 'left')

        self.frame1 = tk.Frame(self, bd=10)
        self.frame1.pack(anchor = tk.W)
        tk.Label(self.frame1, text = "Number of vertical seams to be removed: ").pack(side='left')
        self.v_entry = tk.Entry(self.frame1)
        self.v_entry.pack(side = 'right', anchor = tk.E) 

        self.frame2 = tk.Frame(self, bd = 10)
        self.frame2.pack(anchor = tk.W)
        tk.Label(self.frame2, text = "Number of horizontal seams to be removed: ").pack(side='left')
        self.h_entry = tk.Entry(self.frame2)
        self.h_entry.pack(side='right', anchor = tk.E)

        self.progress = ttk.Progressbar(self, length = 300, mode = 'determinate')
        self.progress.pack()

        self.goButton = tk.Button(self, text = 'Go', command = self.go, width = 20)
        self.goButton.pack(pady = 10)

        self.saveButton = tk.Button(self, text = 'Save as...', command = self.savefile, width = 20)
        self.saveButton.pack(pady = 10)

    def go(self):
        if (len(self.img_path) == 0):
            mb.showinfo('No image selected', 'Please browse an image to be resized')
            return
        img = plt.imread(self.img_path)
        if('.png' in self.img_path):
            img = np.array(img*255, dtype='uint8')
        sc = SeamCarver.SeamCarver(img)
        v_seams = int(self.v_entry.get())
        h_seams = int(self.v_entry.get())
        prg = 0
        total = v_seams + h_seams

        for i in range(v_seams):
            sc.removeSeam()
            prg += 1
            self.progress['value'] = prg/total*100
            self.parent.update_idletasks()
        
        img = sc.getImage()
        img = np.transpose(img, (1,0,2))

        sc = SeamCarver.SeamCarver(img)

        for i in range(h_seams):
            sc.removeSeam()
            prg += 1
            self.progress['value'] = prg/total*100
            self.parent.update_idletasks()
        img = sc.getImage()
        self.img = np.transpose(img, (1,0,2))
    def openfile(self):
        self.img_path = fd.askopenfilename()
        self.path_label.config(text = self.img_path) 

    def savefile(self):
        self.save_path = fd.asksaveasfilename()
        if len(self.save_path) == 0 :
            mb.showinfo('Give destination', 'Please give a destination path')
            return

        plt.imsave(self.save_path, self.img) 

if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    gui.pack()
    root.mainloop()
    