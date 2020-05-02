import tkinter as tk
import tkinter.ttk as ttk


# ListPad(root, content, args[padx, pady, width, anchor, bd]

selected_color = ''
tools = 'brush'
pen_size = '1.0'

class Pixel:
    def __init__(self, *args, **kwargs):
        self.parent = args[0]
        self.row = kwargs['row']
        self.col = kwargs['col']
        self.fill = kwargs['fill']
        self.outline = kwargs['outline']

        self.parent.create_rectangle(self.row, self.col, self.row + 10, self.col + 10, fill=self.fill, outline=self.outline)



class Pad(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, args[0], bg='grey')


        self.name = kwargs['name']

        self.pixels = [] # list of all pixels
        self.color_recursion = ''
        self.ar = [-1, 0, +1, 0]
        self.ac = [0, +1, 0, -1]
        self.ai = [-10, 0, +10, 0]
        self.aj = [0, +10, 0, -10]

        self.frame_main = tk.Canvas(self)

        self.main_canvas = tk.Canvas(self.frame_main, width=800, height=600)

        self.vbar = tk.Scrollbar(self, orient='vertical', command=self.main_canvas.yview)
        self.hbar = tk.Scrollbar(self, orient='horizontal', command=self.main_canvas.xview)

        self.main_canvas.configure(yscrollcommand=self.vbar.set)
        self.main_canvas.configure(xscrollcommand=self.hbar.set)

        self.vbar.pack(side='right', fill='y')
        self.hbar.pack(side='bottom', anchor='sw', fill='x')
        self.frame_main.pack(side='left')

        self.main_canvas.pack(side='top', expand='yes')


        self.scroll_frame = tk.Frame(self.main_canvas)
        self.scroll_frame.pack(fill='both', anchor='nw', expand='yes')
        self.scroll_frame.bind("<Configure>", lambda e: self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.canvas = tk.Canvas(self.scroll_frame, width=800, height=500, bg='grey')
        self.canvas.pack(side='top', anchor='nw')

        self.CreatePixel()

    def CreatePixel(self):

        ''' Creating pixel canvas '''
        row = 2
        for i in range(800):
            rows = []
            col = 2
            for j in range(600):
                pix = self.canvas.create_rectangle(row, col, row+10, col+10, fill='white', outline='dark grey')
                self.canvas.tag_bind(pix, '<Button-1>', self.tap)
                rows.append(pix)
                col += 10
            row += 10
            self.pixels.append(rows)


    def tap(self, event):

        ''' coloring the selected pixel '''

        x = event.x//10
        y = event.y//10

        pixel = int(float(pen_size.get()))

        # collecting all pixels included based on the size of the pen
        pixels = []
        for i in range(pixel):
            for j in range(pixel):
                pixels.append(self.pixels[i + x][j + y])

        if tools == 'brush':
            for p in pixels:
                self.canvas.itemconfigure(p, fill=selected_color, outline=selected_color)

        if tools == 'erase':
            for p in pixels:
                self.canvas.itemconfigure(p, fill='white', outline='dark grey')

        if tools == 'paint':
            item = self.pixels[x][y]
            self.color_recursion = self.canvas.itemcget(item, "fill")
            self.paint(self.color_recursion, item, y, x)


    def paint(self, color, item, row, col):

        ''' paint recursion '''

        if color == self.color_recursion:
            self.canvas.itemconfigure(item, fill=selected_color, outline=selected_color)
            for i, j, in zip(self.ar, self.ac):
                r = row + j
                c = col + i
                if c >=0 and c + j <= 100 and r + i >= 0 and r + i <= 100:
                    p = self.pixels[c][r]
                    p_color = self.canvas.itemcget(p, 'fill')
                    # self.canvas.itemconfigure(p, fill='red', outline=selected_color)
                    self.paint(p_color, p, r, c)
                else:
                    return
        else:
            return



class DrawingPad(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""
    __initialized = False
    def __init__(self, *args, **kwargs):
        global bg, padx, pady, width, bd, fg, cg, selected_color, pen_size

        self.maseter = args[0]
        selected_color = args[1]
        pen_size = args[2]

        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, **kwargs)

        self.tab_list = [] # list of indexes of opened tab
        self.tab_dict = {} # dictionary of opened note tab {directory name and text content}
        self.active_tab = 0 # index of current active note tab
        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
        if 'label' in element:
            self.active_tab = self.index("@%d,%d" % (event.x, event.y))

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            # removing tab in the window
            self.hide(index)
            # removing tab in the opened tab dictionary
            del self.tab_dict[index]
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

    def add_tab(self):

        ''' creating new empty tab '''

        pad = Pad(self.master, name='New')
        pad.pack(side='top', anchor='nw', expand='yes', fill='both')
        self.add(pad, text='New')


    def change_color(self, color):

        '''
        changing color direct from the main app
        pass the color value to the variable selected_color
        to be access by the the tab
        '''

        global selected_color
        selected_color = color


    def tool(self, tool):

        ''' changing the tool value represent the function of the mouse pointer when pressed '''

        global tools
        tools = tool

