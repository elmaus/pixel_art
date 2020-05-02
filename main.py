
import tkinter as tk
from tkinter import colorchooser
import pickle

import threading
import time
import pad

import sys
sys.setrecursionlimit(20000)


FONT_LABEL = ('Roboto', 11)

selected_color = ''
pallet_dict = {}

with open('pallet.pickle', 'rb') as file:
    pallet_dict = pickle.load(file)


class ExportDialog(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self)

        self.configure(padx=20, pady=20)

        self.lbl = tk.Label(self, text='Export to')
        self.lbl.grid(row=0, column=0, columnspan=2, pady=10)

        self.png = tk.Button(self, text='PNG', width=20, command=lambda:self.export('png'))
        self.png.grid(row=1, column=0)

        self.jpg = tk.Button(self, text='JPG', width=20, command=lambda:self.export('jpg'))
        self.jpg.grid(row=1, column=1)

        self.parent = args[0]

    def export(self, ext):
        self.parent.export(ext)
        self.destroy()


class NewDialog(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self)
        self.configure(padx=40)
        self.configure(pady=40)

        self.parent = args[0]

        self.col = 0
        self.row = 0
        self.title = ''

        self.name_lbl = tk.Label(self, text='Name:', font=FONT_LABEL)
        self.name_lbl.grid(row=0, column=0)

        self.name_ent = tk.Entry(self, width=50)
        self.name_ent.grid(row=0, column=1, columnspan=4)

        self.width_lbl = tk.Label(self, text='Width', font=FONT_LABEL)
        self.width_lbl.grid(row=1, column=1, columnspan=2)

        self.height_lbl = tk.Label(self, text='Height', font=FONT_LABEL)
        self.height_lbl.grid(row=1, column=3, columnspan=2)

        self.pixel_lbl = tk.Label(self, text='Pixel', font=FONT_LABEL)
        self.pixel_lbl.grid(row=2, column=0)

        self.wp = tk.Entry(self, width=25, justify='center')
        self.wp.grid(row=2, column=1, columnspan=2)

        self.hp = tk.Entry(self, width=25, justify='center')
        self.hp.grid(row=2, column=3, columnspan=2)

        self.ok_btn = tk.Button(self, text='OK', width=6, font=FONT_LABEL, command=lambda:self.ok())
        self.ok_btn.grid(row=3, column=3, pady=10)

        self.cancel_btn = tk.Button(self, text='CANCEL', width=6, font=FONT_LABEL, command=lambda: self.destroy())
        self.cancel_btn.grid(row=3, column=4, pady=10)

    def ok(self):
        name = self.name_ent.get()
        width = int(self.wp.get())
        height = int(self.hp.get())

        self.parent.new(name, width, height)
        self.destroy()



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
        self.resizable(50, 50)

        self.current_color = None
        self.variable = tk.StringVar()
        self.variable.set('1.0')

        self._pen_tool = []

        ##### ----------------------------------- IMAGES -------------------------------- #####
        self.new_image = tk.PhotoImage(file='images/new.png')
        self.new_icon = self.new_image.subsample(3, 3)

        self.open_image = tk.PhotoImage(file='images/open.png')
        self.open_icon = self.open_image.subsample(3, 3)

        self.save_image = tk.PhotoImage(file='images/save.png')
        self.save_icon = self.save_image.subsample(3, 3)

        self.save_as_image = tk.PhotoImage(file='images/saveas.png')
        self.save_as_icon = self.save_as_image.subsample(3, 3)

        self.export_image = tk.PhotoImage(file='images/export.png')
        self.export_icon = self.export_image.subsample(3, 3)

        self.brush_image = tk.PhotoImage(file='images/brush.png')
        self.brush_icon = self.brush_image.subsample(3, 3)

        self.paint_image = tk.PhotoImage(file='images/paint.png')
        self.paint_icon = self.paint_image.subsample(3, 3)

        self.eraser_image = tk.PhotoImage(file='images/eraser.png')
        self.eraser_icon = self.eraser_image.subsample(3, 3)

        self.zoom_in_image = tk.PhotoImage(file='images/zoom-in.png')
        self.zoom_in_icon = self.zoom_in_image.subsample(3, 3)

        self.zoom_out_image = tk.PhotoImage(file='images/zoom-out.png')
        self.zoom_out_icon = self.zoom_out_image.subsample(3, 3)
        ##### ----------------------------------- IMAGES -------------------------------- #####



        ##### ----------------------------------- GUI -------------------------------- #####
        self.frame = tk.Frame(self, relief='raised', bd=2, width=600)
        self.frame.pack(side='top', fill='y', anchor='nw', pady=5, padx=10)

        self.new_btn = tk.Button(self.frame, width=50, image=self.new_icon, text='New', command=lambda: NewDialog(self))
        self.new_btn.grid(row=0, column=0, sticky='nw')

        self.open_btn = tk.Button(self.frame, width=50, image=self.open_icon, text='Open', command=lambda:self.save())
        self.open_btn.grid(row=0, column=1, sticky='nw')

        self.save_btn = tk.Button(self.frame, width=50, image=self.save_icon, text='Save')
        self.save_btn.grid(row=0, column=2, sticky='nw')

        self.save_as_btn = tk.Button(self.frame, width=50, image=self.save_as_icon, text='Save as')
        self.save_as_btn.grid(row=0, column=3, sticky='nw')

        self.export_btn = tk.Button(self.frame, width=50, image=self.export_icon, text='Export',command=lambda:ExportDialog(self))
        self.export_btn.grid(row=0, column=4, sticky='nw')

        # frame for pallet
        self.frame1 = tk.Frame(self, relief='groove', bd=3)
        self.frame1.pack(side='left', anchor='nw', padx=10)

        # frame for tools
        self.frame2 = tk.Frame(self, relief='groove', bd=3)
        self.frame2.pack(side='right', anchor='nw', padx=10)

        self.option = tk.OptionMenu(self.frame2, self.variable, '1.0', '2.0', '3.0', '4.0')
        self.option.grid(row=0, column=0)
        self.option.configure(width=6)

        self.brush_btn = tk.Button(self.frame2, width=50, relief='sunken', image=self.brush_icon, text='Brush', command=lambda:self.tool('brush', 0))
        self.brush_btn.grid(row=1, column=0)
        self._pen_tool.append(self.brush_btn)

        self.paint_btn = tk.Button(self.frame2, width=50, image=self.paint_icon, text='Paint', command=lambda:self.tool('paint', 1))
        self.paint_btn.grid(row=2, column=0)
        self._pen_tool.append(self.paint_btn)

        self.erase_btn = tk.Button(self.frame2, width=50, image=self.eraser_icon, text='Erase', command=lambda:self.tool('erase', 2))
        self.erase_btn.grid(row=3, column=0)
        self._pen_tool.append(self.erase_btn)

        self.zoom_in_btn = tk.Button(self.frame2, width=50, image=self.zoom_in_icon, text='Zoom +', command=lambda:self.zoom_in('+'))
        self.zoom_in_btn.grid(row=4, column=0)

        self.zoom_out_btn = tk.Button(self.frame2, width=50, image=self.zoom_out_icon, text='Zoom -', command=lambda:self.zoom_in('-'))
        self.zoom_out_btn.grid(row=5, column=0)

        self.pad_ = pad.DrawingPad(self, selected_color, self.variable)
        self.pad_.pack(side='left', anchor='nw')
        self.pad_.add_welcome()
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


    def new(self, name, w, h):

        ''' new file creation '''

        self.pad_.add_tab(name, w, h)



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



    def tool(self, tool, index):
        for p in self._pen_tool:
            p.configure(relief='raised')

        self.pad_.tool(tool)

        self._pen_tool[index].configure(relief='sunken')

    def export(self, ext):
        self.pad_.export(ext)

    def zoom_in(self, z):
        self.pad_.zoom_in(z)



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
