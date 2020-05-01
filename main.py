
import tkinter as tk
from tkinter import colorchooser
import pickle

import threading
import time
import pad

import sys
sys.setrecursionlimit(20000)


selected_color = ''

pallet_dict = {}

with open('pallet.pickle', 'rb') as file:
    pallet_dict = pickle.load(file)


class Pallet(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, args[0], bd=2, relief='sunken', bg='grey', width=20, height=20)
        self.bind('<Button-1>', kwargs['bind1'])
        self.bind('<Button-3>', kwargs['bind2'])


        self.pos = '{}-{}'.format(kwargs['pos1'], kwargs['pos2'])
        self.color = self.color = pallet_dict[self.pos]
        self.load_colors()



    def load_colors(self):

        ''' loading save colors of pallets '''

        try:
            self.color = pallet_dict[self.pos]
            self.configure(bg=pallet_dict[self.pos])
        except:
            pass



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)
        self.title("Sam's Pixel Art")
        self.wm_iconbitmap('eyecon.ico')
        self.configure(bg='black')
        self.geometry('850x550')

        self.current_color = None
        self.variable = tk.StringVar()
        self.variable.set('1.0')

        ##### ----------------------------------- GUI -------------------------------- #####


        self.frame = tk.Frame(self, relief='raised', bd=2, width=600)
        self.frame.pack(side='top', fill='y', anchor='nw', pady=5, padx=10)

        self.file_btn = tk.Button(self.frame, width=10, text='File')
        self.file_btn.grid(row=0, column=0, sticky='nw')

        self.save_btn = tk.Button(self.frame, width=10, text='Save', command=lambda:self.save())
        self.save_btn.grid(row=0, column=1, sticky='nw')

        self.edit_btn = tk.Button(self.frame, width=10, text='Edit')
        self.edit_btn.grid(row=0, column=2, sticky='nw')

        self.image_btn = tk.Button(self.frame, width=10, text='Image')
        self.image_btn.grid(row=0, column=3, sticky='nw')

        self.brush_btn = tk.Button(self.frame, width=10, text='Brush')
        self.brush_btn.grid(row=0, column=4, sticky='nw')

        self.paint_btn = tk.Button(self.frame, width=10, text='Paint')
        self.paint_btn.grid(row=0, column=5, sticky='nw')

        # frame for pallet
        self.frame1 = tk.Frame(self, relief='groove', bd=3)
        self.frame1.pack(side='left', anchor='nw', padx=10)

        # frame for tools
        self.frame2 = tk.Frame(self, relief='groove', bd=3)
        self.frame2.pack(side='right', anchor='ne', padx=10)

        self.option = tk.OptionMenu(self.frame2, self.variable, '1.0', '2.0', '3.0', '4.0')
        self.option.grid(row=0, column=0)
        self.option.configure(width=6)

        self.brush_btn = tk.Button(self.frame2, width=10, text='Brush', command=lambda:self.tool('brush'))
        self.brush_btn.grid(row=1, column=0)

        self.paint_btn = tk.Button(self.frame2, width=10, text='Paint', command=lambda:self.tool('paint'))
        self.paint_btn.grid(row=2, column=0)

        self.erase_btn = tk.Button(self.frame2, width=10, text='Erase', command=lambda:self.tool('erase'))
        self.erase_btn.grid(row=3, column=0)

        self.zoom_in_btn = tk.Button(self.frame2, width=10, text='Zoom +')
        self.zoom_in_btn.grid(row=4, column=0)

        self.zoom_out_btn = tk.Button(self.frame2, width=10, text='Zoom -')
        self.zoom_out_btn.grid(row=5, column=0)

        self.pad_ = pad.DrawingPad(self, selected_color, self.variable)
        self.pad_.pack(side='top', fill='both', expand='yes')
        self.pad_.add_tab()
        ##### ----------------------------------- GUI -------------------------------- #####

        # self.CreatePixel()
        self.CreatePallete()


    def CreatePallete(self):

        ''' Creating pallete '''

        for i in range(15):
            for j in range(3):
                self.canvases = Pallet(self.frame1, bind1=self.select_color, bind2=self.pick_color, pos1=i, pos2=j)
                self.canvases.grid(row=i, column=j)

        self.selected = tk.Canvas(self.frame1, bd=2, relief='sunken', bg='grey', width=58, height=55)
        self.selected.grid(row=15, column=0, columnspan=3)


    def pick_color(self, event):

        ''' picking a color form tkinter askcolor '''

        color = tk.colorchooser.askcolor()[-1]

        event.widget.configure(bg=color)
        event.widget.color = color
        self.selected.configure(bg=color)
        pallet_dict[event.widget.pos] = color
        self.pad_.change_color(event.widget.color)

        # saving color to the file
        with open('pallet.pickle', 'wb') as file:
            pickle.dump(pallet_dict, file)


    def select_color(self, event):

        ''' selecting a color of from the pallet '''

        global selected_color
        self.selected.configure(bg=event.widget.color)
        self.pad_.change_color(event.widget.color)
        pallet_dict[event.widget.pos] = event.widget.color

        # saving the current color
        with open('pallet.pickle', 'wb') as file:
            pall = pickle.dump(pallet_dict, file)



    def tool(self, tool):
        self.pad_.tool(tool)

    def save(self):
        print(self.option.get())



finshed = False

def main():
    global finished

    app = App()
    finished = True
    app.mainloop()

def loading():
    while finshed == False:
        time.sleep(.50)
        print('loading')


if __name__ == '__main__':
    app = App()
    app.mainloop()
    # m = threading.Thread(target=main)
    # f = threading.Thread(target=loading)
    # m.start()
    # f.start()
