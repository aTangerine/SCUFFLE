import os
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import MovelistParser




class GUI_MoveViewer:
    def __init__(self, master):
        self.master = master
        self.master.geometry(str(1850) + 'x' + str(990))
        master.title("SCUFFLE Move Viewer")
        master.iconbitmap('Data/icon.ico')

        self.movelist_name_var = StringVar()
        self.movelist_name_var.set('???')

        self.load_movelist('movelists/seong_mina_movelist.m0000')

        self.master.rowconfigure(0, weight=1)

        self.master.columnconfigure(0, weight=1)

        self.main_window = self.create_window_in_scrollable_viewport(master)

        loader_frame = Frame(self.main_window)
        loader_frame.grid(sticky=N+W, row = 0, column=0)

        self.label = Label(loader_frame, textvariable=self.movelist_name_var)
        self.label.pack()


        self.load_movelist_button = Button(loader_frame, text="Load Movelist", command=lambda: self.load_movelist_dialog())
        self.load_movelist_button.pack()

        self.save_movelist_button = Button(loader_frame, text="Save Movelist", command=lambda: self.save_movelist_dialog())
        self.save_movelist_button.pack()

        #self.close_button = Button(loader_frame, text="Close", command=master.quit)
        #self.close_button.pack()

        display_frame = Frame(self.main_window)
        display_frame.grid(sticky=S + E + W, row = 0, column = 1)

        move_frame = Frame(display_frame)
        move_frame.grid(sticky=N+E , row = 0, column = 0)

        move_id_entry_container = Frame(move_frame)
        move_id_entry_container.grid(row=0, column=0)

        move_id_entry = Entry(move_id_entry_container)
        move_id_entry.bind('<Return>', lambda x: self.load_moveid(move_id_entry.get()))
        move_id_entry.pack()



        self.move_id_textvar = StringVar()
        self.move_id_textvar.set('-')
        self.move_id_label = Label(move_id_entry_container, textvariable=self.move_id_textvar)
        self.move_id_label.pack()

        self.load_button = Button(move_id_entry_container, text="Load", command=lambda: self.load_moveid(move_id_entry.get()))
        self.load_button.pack()

        self.next_move_id_button = Button(move_id_entry_container, text="+", command=lambda: self.next_move_id_command())
        self.prev_move_id_button = Button(move_id_entry_container, text="-", command=lambda: self.prev_move_id_command())

        self.next_move_id_button.pack()
        self.prev_move_id_button.pack()

        self.move_raw = Text(move_frame, height=24, width=12)
        self.move_raw .grid(sticky = N+W, row = 0, column = 1)

        self.move_intr = Text(move_frame, wrap="none", height=24, width=32)
        self.move_intr.grid(sticky=N+W, row=0, column=2)


        hitbox_frame = Frame(display_frame)
        hitbox_frame.grid(sticky=N+E, row = 1, column = 0)

        hitbox_frame_header = Frame(hitbox_frame)
        hitbox_frame_header.grid(sticky=N+W, row=0, column=0)

        self.hitbox_index = 0
        self.hitboxes_data = []

        self.hitbox_index_var = StringVar()
        self.hitbox_index_var.set('0/0')

        self.hitbox_id_var = StringVar()
        self.hitbox_id_var.set('-1')

        self.next_hitbox_button = Button(hitbox_frame_header, text="+", command=lambda: self.next_hitbox_command())
        self.prev_hitbox_button = Button(hitbox_frame_header, text="-", command=lambda: self.prev_hitbox_command())
        self.hitbox_label = Label(hitbox_frame_header, textvariable = self.hitbox_index_var)
        self.hitbox_id_label = Label(hitbox_frame_header, textvariable=self.hitbox_id_var)

        self.prev_hitbox_button.grid(sticky=N, row=3, column=0)
        self.hitbox_label.grid(sticky=N, row=0, column=0)
        self.next_hitbox_button.grid(sticky=N, row = 2, column=0)
        self.hitbox_id_label.grid(sticky=N, row=1, column=0)


        #self.hitbox_raw = Text(hitbox_frame, wrap='none', height=36, width=18)
        #self.hitbox_intr = Text(hitbox_frame, wrap='none', height=36, width=32)
        #self.hitbox_raw.grid(sticky=W, row=0, column=1)
        #self.hitbox_intr.grid(sticky=W, row=0, column=2)

        self.hitbox_pair = ScrolledTextPair(hitbox_frame, (18, 32), 36, True)
        self.hitbox_pair.grid(sticky=W, row=0, column=1)
        self.hitbox_raw = self.hitbox_pair.left
        self.hitbox_intr = self.hitbox_pair.right



        self.cancel_frame = Frame(self.main_window)
        self.cancel_frame.grid(sticky=W+E+N+S, row = 0, column = 3)

        self.cp = ScrolledTextPair(self.cancel_frame,  (70, 50), 40)
        self.cp.grid(sticky=N+W, row = 0, column = 0)

        self.cancel_raw = self.cp.left
        self.cancel_intr = self.cp.right


        self.link_frame = Frame(self.cancel_frame)
        self.link_frame.grid(sticky=W+E+N+S, row = 1, column = 0)

        self.frame_data_intr = Text(self.link_frame, width=120, height=1)
        self.frame_data_intr.grid(sticky=W + E + N + S, row=0, column=0, columnspan=2)

        self.link_intr = Text(self.link_frame, width=80, height=18)
        self.link_intr.grid(sticky=W + E + N + S, row=1, column=0)



        self.clipboard_hitbox_button = Button(hitbox_frame_header, text="Copy Hitbox to Clipboard", command=lambda:GUI_MoveViewer.copy_to_clipboard_and_strip(self.hitbox_raw.get('1.0', END)))
        self.clipboard_hitbox_button.grid(sticky=N+W+E, row=4, column=0)

        self.clipboard_move_button = Button(move_id_entry_container, text="Copy Move to Clipboard", command=lambda: GUI_MoveViewer.copy_to_clipboard_and_strip(self.move_raw.get('1.0', END)))
        self.clipboard_move_button.pack()

        self.clipboard_cancel_button = Button(self.link_frame, text="Copy Cancel to Clipboard", command=lambda: GUI_MoveViewer.copy_to_clipboard_and_strip(self.cancel_raw.get('1.0', END)))
        self.clipboard_cancel_button.grid(sticky=N+W, row = 1, column =1)

        self.cancel_intr.tag_configure("bold", font="Helvetica 9 bold")
        self.cancel_intr.tag_configure("soulcharge", font="Helvetica 9 bold", foreground='#2C75FF')

        self.link_intr.tag_configure("bold", font="Helvetica 9 bold")


    def create_window_in_scrollable_viewport(self, master):
        scrollable_frame = Canvas(master, width=1850, height=990, scrollregion=(0, 0, 1850, 990))
        main_window = Frame(master)

        xscrlbr = Scrollbar(master, orient='horizontal')
        xscrlbr.grid(column=0, row=1, sticky='ew', columnspan=2)
        yscrlbr = Scrollbar(master, orient='vertical')
        yscrlbr.grid(column=1, row=0, sticky='ns')

        xscrlbr.config(command=scrollable_frame.xview)
        yscrlbr.config(command=scrollable_frame.yview)
        scrollable_frame.configure(yscrollcommand=yscrlbr.set)
        scrollable_frame.configure(xscrollcommand=xscrlbr.set)
        scrollable_frame.config(width=1850, height=990)

        # self.scrollable_frame.configure(scrollregion=self.scrollable_frame.bbox("all"))
        scrollable_frame.grid(sticky=N + S + E + W, row=0, column=0)
        scrollable_frame.create_window((0, 0), window=main_window, anchor="nw")
        return main_window

    def load_movelist(self, path):
        try:
            self.movelist = MovelistParser.Movelist.from_file(path)
            self.movelist_name_var.set(self.movelist.name)
        except Exception as e:
            print(e)

    def set_movelist(self, movelist):
        self.movelist = movelist
        self.movelist_name_var.set(self.movelist.name)



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

    def next_move_id_command(self):
        self.load_moveid(int(self.move_id_textvar.get().split(':')[1]) + 1)

    def prev_move_id_command(self):
        self.load_moveid(int(self.move_id_textvar.get().split(':')[1]) - 1)

    def load_moveid(self, move_id):
        try:
            id = int(move_id)
        except:
            print('unrecognized move_id: {}'.format(move_id))
            return

        if id < len(self.movelist.all_moves) and id >= 0:
            self.move_id_textvar.set('move id: {}'.format(id))
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

            highlight_tag_and_remove(self.cancel_intr, '<sc>', 'soulcharge')
            highlight_tag_and_remove(self.cancel_intr, '<b>', 'bold')


            GUI_MoveViewer.alternating_gray(self.cancel_raw)
            GUI_MoveViewer.alternating_gray(self.cancel_intr)


            links = '\n'.join([str(x) for x in move.cancel.links])
            self.link_intr.delete(1.0, END)
            self.link_intr.insert(END, links)
            highlight_tag_and_remove(self.link_intr, '<b>', 'bold')

            self.frame_data_intr.delete(1.0, END)
            self.frame_data_intr.insert(END, ' | '.join([str(x) for x in move.get_frame_data()]))


    def load_hitbox(self):
        i = self.hitbox_index
        if len(self.hitboxes_data) == 0:
            self.hitbox_raw.delete(1.0, END)
            self.hitbox_intr.delete(1.0, END)
        elif i < len(self.hitboxes_data):
            self.hitbox_raw.delete(1.0, END)
            self.hitbox_raw.insert(END, self.hitboxes_data[i][0])

            self.hitbox_intr.delete(1.0, END)
            self.hitbox_intr.insert(END, self.hitboxes_data[i][1])
        self.update_hitbox_var()

    def update_hitbox_var(self):
        self.hitbox_index_var.set('{}/{}'.format(self.hitbox_index + 1, len(self.hitboxes_data)))
        if len(self.hitboxes_data) > 0:
            self.hitbox_id_var.set('attack index: {}'.format(self.hitboxes_data[self.hitbox_index][2]))

    def load_movelist_dialog(self):
        #Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

        filename = askopenfilename(initialdir = '{}/{}'.format(os.getcwd(), '/movelists'))  # show an "Open" dialog box and return the path to the selected file
        self.load_movelist(filename)

    def save_movelist_dialog(self):
        filename = asksaveasfilename(defaultextension=".sc6_movelist")
        if filename == '':
            return
        else:
            with open(filename, 'wb') as fw:
                fw.write(self.movelist.bytes)



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

    def copy_to_clipboard_and_strip(text):
            clip = Tk()
            clip.withdraw()
            clip.clipboard_clear()
            clip.clipboard_append(text.replace('\n', ''))
            clip.destroy()




#https://stackoverflow.com/questions/32038701/python-tkinter-making-two-text-widgets-scrolling-synchronize
class ScrolledTextPair(Frame):
    '''Two Text widgets and a Scrollbar in a Frame'''

    def __init__(self, master, width_lr, h, hide_scrollbar=False):
        Frame.__init__(self, master) # no need for super


        # Creating the widgets
        self.left = Text(self, width = width_lr[0], wrap='none', height=h)
        self.left.pack(side=LEFT, fill=BOTH, expand=True)
        self.right = Text(self, width = width_lr[1], wrap='none', height=h)
        self.right.pack(side=LEFT,  fill=BOTH, expand=True)
        self.scrollbar = Scrollbar(self)
        if not hide_scrollbar:
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




def highlight_tag_and_remove(tw, marker, highlight):
    regex = '{}.*?{}'.format(marker, marker).replace('>', '\>').replace('<', '\<')
    highlight_pattern_in_text_widget(tw, regex, marker, highlight, regexp=True)


def highlight_pattern_in_text_widget(tw, pattern, marker, tag, start="1.0", end="end",
                      regexp=False):
    '''Apply the given tag to all text that matches the given pattern

    If 'regexp' is set to True, pattern will be treated as a regular
    expression according to Tcl's regular expression syntax.
    '''

    start = tw.index(start)
    end = tw.index(end)
    tw.mark_set("matchStart", start)
    tw.mark_set("matchEnd", start)
    tw.mark_set("searchLimit", end)

    matches = []

    count = IntVar()
    while True:
        index = tw.search(pattern, "matchEnd", "searchLimit",
                            count=count, regexp=regexp)
        if index == "": break
        if count.get() == 0: break  # degenerate pattern which matches zero-length strings
        tw.mark_set("matchStart", index)
        tw.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
        tw.tag_add(tag, "matchStart", "matchEnd")

        size = len(marker)

        tw.delete('{}-{}c'.format('matchEnd', size), "matchEnd")
        tw.delete("matchStart", '{}+{}c'.format('matchStart', size))


if __name__ == '__main__':
    root = Tk()
    my_gui = GUI_MoveViewer(root)
    root.mainloop()