import os
from tkinter import *
from tkinter.filedialog import askopenfilename
import MovelistParser




class GUI_MoveViewer:
    def __init__(self, master):
        self.master = master
        self.master.geometry(str(1920) + 'x' + str(720))
        master.title("SCUFFLE Move Viewer")

        self.movelist_name_var = StringVar()
        self.movelist_name_var.set('???')

        self.load_movelist('movelists/seong_mina_movelist.m0000')

        self.master.rowconfigure(0, weight=1)

        self.master.columnconfigure(0, weight=1)

        self.scrollable_frame = Canvas(master)
        self.scrollable_frame.grid(sticky=N+S+E+W, row = 0, column = 0)

        #SCROLLING TOO HARD; CODE HULK NOT UNDERSTAND; CODE HULK SMASH TKINTER
        #self.xscrlbr = Scrollbar(master, orient='horizontal')
        #self.xscrlbr.grid(column=0, row=1, sticky='ew', columnspan=2)
        #self.yscrlbr = Scrollbar(master)
        #self.yscrlbr.grid(column=1, row=0, sticky='ns')

        #self.scrollable_frame.configure(yscrollcommand=self.yscrlbr.set)
        #self.scrollable_frame.configure(xscrollcommand=self.xscrlbr.set)
        #self.xscrlbr.config(command = self.scrollable_frame.xview)
        #self.yscrlbr.config(command=self.scrollable_frame.yview)
        #self.scrollable_frame.configure(scrollregion=self.scrollable_frame.bbox("all"))

        loader_frame = Frame(self.scrollable_frame)
        loader_frame.grid(sticky=N+W)


        self.label = Label(loader_frame, textvariable=self.movelist_name_var)
        self.label.pack()

        e = Entry(loader_frame)
        e.pack()

        e.delete(0, END)
        e.insert(0, "0")

        self.load_button = Button(loader_frame, text="Load", command=lambda: self.load_moveid(e.get()))
        self.load_button.pack()

        self.load_button = Button(loader_frame, text="Load Movelist", command=lambda: self.load_movelist_dialog())
        self.load_button.pack()

        self.close_button = Button(loader_frame, text="Close", command=master.quit)
        self.close_button.pack()

        display_frame = Frame(self.scrollable_frame)
        display_frame.grid(sticky=S + E + W)

        self.move_raw = Text(display_frame, height=24, width=12)
        self.move_raw .grid(sticky = N+W, row = 0, column = 0)

        self.move_intr = Text(display_frame, wrap="none", height=24, width=32)
        self.move_intr.grid(sticky=N+W, row=0, column=1)


        hitbox_frame = Frame(display_frame)
        hitbox_frame.grid(sticky=N+W, row = 0, column = 2)

        hitbox_frame_header = Frame(hitbox_frame)
        hitbox_frame_header.grid(sticky=N+W, row=0, column=0)

        self.hitbox_index = 0
        self.hitboxes_data = []

        self.hitbox_index_var = StringVar()
        self.hitbox_index_var.set('0/0')

        self.hitbox_id_var = StringVar()
        self.hitbox_id_var.set('-1')

        self.next_hitbox_button = Button(hitbox_frame_header, text=">", command=lambda: self.next_hitbox_command())
        self.prev_hitbox_button = Button(hitbox_frame_header, text="<", command=lambda: self.next_hitbox_command())
        self.hitbox_label = Label(hitbox_frame_header, textvariable = self.hitbox_index_var)
        self.hitbox_id_label = Label(hitbox_frame_header, textvariable=self.hitbox_id_var)

        self.prev_hitbox_button.grid(sticky=N+W, row=0, column=0)
        self.hitbox_label.grid(sticky=N+W, row=0, column=1)
        self.next_hitbox_button.grid(sticky=N+W, row = 0, column=2)
        self.hitbox_id_label.grid(sticky=N + W, row=0, column=3)


        self.hitboxes_raw = []
        self.hitboxes_intr = []

        for _ in range(1):
            self.hitboxes_raw.append(Text(hitbox_frame, wrap='none', height=36, width=18))
            self.hitboxes_intr.append(Text(hitbox_frame, wrap='none', height=36, width=32))

        for i, text in enumerate(self.hitboxes_raw):
            text.grid(sticky=W, row=1, column=i * 2)

        for i, text in enumerate(self.hitboxes_intr):
            text.grid(sticky=W, row=1, column=i * 2 + 1)

        self.cancel_frame = Frame(display_frame)
        self.cancel_frame.grid(sticky=W+E+N+S, row = 0, column = 3)

        self.cp = ScrolledTextPair(self.cancel_frame, wrap='none', height=36, width = 66)
        self.cp.grid(sticky=N+W, row = 0, column = 0)

        self.cancel_raw = self.cp.left
        self.cancel_intr = self.cp.right


        #self.cancel_raw = Text(self.cancel_frame, wrap='none', height=36, width=90)
        #self.cancel_intr = Text(self.cancel_frame, wrap='none', height=36, width=36)

        #self.cancel_raw.grid(sticky=W, row=0, column = 0)
        #self.cancel_intr.grid(sticky=W, row=0, column = 1)

    def load_movelist(self, path):
        try:
            self.movelist = MovelistParser.Movelist.from_file(path)
            self.movelist_name_var.set(self.movelist.name)
        except Exception as e:
            print(e)


    def next_hitbox_command(self):
        self.hitbox_index += 1
        if self.hitbox_index >= len(self.hitboxes_data):
            self.hitbox_index = 0
        self.load_hitbox()

    def prev_hitbox_command(self):
        self.hitbox_index -= 1
        if self.hitbox_index < 0:
            self.hitbox_index = 0
        self.load_hitbox()

    def load_moveid(self, move_id):
        try:
            id = int(move_id)
        except:
            print('unrecognized move_id: {}'.format(move_id))
            return

        if id < len(self.movelist.all_moves):
            move = self.movelist.all_moves[id]
            bytes, guide = move.get_gui_guide()

            raw, intr = self.apply_guide(bytes, guide)

            self.move_raw.delete(1.0, END)
            self.move_raw.insert(END, raw)

            self.move_intr.delete(1.0, END)
            self.move_intr.insert(END, intr)

            self.hitbox_index = 0
            self.hitboxes_data = []

            for i, attack in enumerate(move.attacks):
                bytes, guide = attack.get_gui_guide()
                raw, intr = self.apply_guide(bytes, guide)
                self.hitboxes_data.append((raw, intr, move.attack_indexes[i]))
            self.load_hitbox()

            cancel_guide = move.cancel.get_gui_guide()
            #for bytes in cancel_guide:

            raw = ''
            intr = ''
            for bytes, desc in cancel_guide:
                raw = '{}{}\n'.format(raw, bytes)
                intr = '{}{}\n'.format(intr, desc)


            self.cancel_raw.delete(1.0, END)
            self.cancel_raw.insert(END, raw)
            self.cancel_intr.delete(1.0, END)
            self.cancel_intr.insert(END, intr)

            GUI_MoveViewer.alternating_gray(self.cancel_raw)
            GUI_MoveViewer.alternating_gray(self.cancel_intr)

    def load_hitbox(self):
        i = self.hitbox_index
        if i < len(self.hitboxes_data):
            self.hitboxes_raw[0].delete(1.0, END)
            self.hitboxes_raw[0].insert(END, self.hitboxes_data[i][0])

            self.hitboxes_intr[0].delete(1.0, END)
            self.hitboxes_intr[0].insert(END, self.hitboxes_data[i][1])
        self.update_hitbox_var()

    def update_hitbox_var(self):
        self.hitbox_index_var.set('{}/{}'.format(self.hitbox_index + 1, len(self.hitboxes_data)))
        if len(self.hitboxes_data) > 0:
            self.hitbox_id_var.set(str(self.hitboxes_data[self.hitbox_index][2]))

    def load_movelist_dialog(self):
        #Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

        filename = askopenfilename(initialdir = '{}/{}'.format(os.getcwd(), '/movelists'))  # show an "Open" dialog box and return the path to the selected file
        self.load_movelist(filename)

    def apply_guide(self, bytes, guide):
        raw = ''
        intr = ''
        for start, stop, func, info in guide:
            slice = bytes[start:stop]
            raw += ('{}\n'.format(MovelistParser.Movelist.bytes_as_string(slice)))
            try:
                intr += ('{} : {}\n'.format(func(slice, 0), info))
            except:
                intr += 'ERROR\n'
        return raw, intr

    #https://stackoverflow.com/questions/26348989/changing-background-color-for-every-other-line-of-text-in-a-tkinter-text-box-wid
    def alternating_gray(text):
        lastline = text.index("end-1c").split(".")[0]
        tag = "odd"
        for i in range(1, int(lastline)):
            text.tag_add(tag, "%s.0" % i, "%s.0" % (i + 1))
            tag = "even" if tag == "odd" else "odd"


#https://stackoverflow.com/questions/32038701/python-tkinter-making-two-text-widgets-scrolling-synchronize
class ScrolledTextPair(Frame):
    '''Two Text widgets and a Scrollbar in a Frame'''

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master) # no need for super

        # Different default width
        if 'width' not in kwargs:
            kwargs['width'] = 30

        # Creating the widgets
        self.left = Text(self, **kwargs)
        self.left.pack(side=LEFT, fill=BOTH, expand=True)
        self.right = Text(self, **kwargs)
        self.right.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        #Styling
        self.left.tag_configure("even", background="#f0f0f0")
        self.left.tag_configure("odd", background="#ffffff")

        self.right.tag_configure("even", background="#f0f0f0")
        self.right.tag_configure("odd", background="#ffffff")

        # Changing the settings to make the scrolling work
        self.scrollbar['command'] = self.on_scrollbar
        self.left['yscrollcommand'] = self.on_textscroll
        self.right['yscrollcommand'] = self.on_textscroll

    def on_scrollbar(self, *args):
        '''Scrolls both text widgets when the scrollbar is moved'''
        self.left.yview(*args)
        self.right.yview(*args)

    def on_textscroll(self, *args):
        '''Moves the scrollbar and scrolls text widgets when the mousewheel
        is moved on a text widget'''
        self.scrollbar.set(*args)
        self.on_scrollbar('moveto', args[0])


if __name__ == '__main__':
    root = Tk()
    my_gui = GUI_MoveViewer(root)
    root.mainloop()