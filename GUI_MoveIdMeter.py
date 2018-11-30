from tkinter import *
from tkinter.ttk import *

import time

import SoulCaliburGameState
import _GameStateManager

from collections import defaultdict

class GUI_MoveIdMeter:
    FRAMES = 100

    p1_symbols = {
        0: '+',
        1: '*',
        2: '.',
        3: '#',
        4: '^',
        5: '&',
        6: '@',

    }

    '''tag_colors = {
        0: '#555555',
        1: '#777777',
        2: '#999999',
        3: '#bbbbbb',
        4: '#dddddd',
        5: '#666666',
        6: '#888888',
    }'''

    tag_colors = {
        0: '#FFAAAA',
        1: '#FFFFAA',
        2: '#90EE90',
        3: '#ADD8E6',
        4: '#CCCCCC',
        5: '#FF89D2',
        6: '#E5AC67',
    }


    p2_symbols = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
        6: 'G',

    }


    def __init__(self, master):
        self.master = master
        self.master.geometry(str(1500) + 'x' + str(190))
        master.title("SCUFFLE Move-Id-Ometer")
        master.iconbitmap('Data/icon.ico')

        self.style = Style()
        self.style.configure('MoveIdOmeter.TFrame', background='black')

        self.ometer_frame = Frame(self.master)
        self.ometer_frame.pack()

        self.p1_text = Text(self.ometer_frame, font=("Consolas", 16), width=GUI_MoveIdMeter.FRAMES, height = 1)
        self.p2_text = Text(self.ometer_frame, font=("Consolas", 16), width=GUI_MoveIdMeter.FRAMES, height=1)

        self.frames_guide = Text(self.ometer_frame, font=("Consolas", 16), width=GUI_MoveIdMeter.FRAMES, height=1)

        self.p1_key = Text(self.ometer_frame, font=("Consolas", 16), width=10, height=len(GUI_MoveIdMeter.p1_symbols))
        self.p2_key = Text(self.ometer_frame, font=("Consolas", 16), width=10, height=len(GUI_MoveIdMeter.p2_symbols))

        self.selection_var = StringVar()
        self.selection_var.set('000 Frames Selected')
        self.selection_label = Label(self.ometer_frame, font=("Consolas", 16), textvariable=self.selection_var)
        self.selection_label.grid(row=3, column = 1)


        self.p1_text.grid(sticky = S, row = 0, column = 1)
        self.frames_guide.grid(row=1, column=1)
        self.p2_text.grid(sticky = N,row = 2, column = 1)
        self.p1_key.grid(row=0, column = 0, rowspan=4)
        self.p2_key.grid(row=0, column=2, rowspan=4)

        self.current_frame = -1

        self.p1_counter = 1
        self.p2_counter = 1

        self.p1_keymap = {}
        self.p2_keymap = {}
        for i in range(len(GUI_MoveIdMeter.p1_symbols)):
            self.p1_keymap[i] = -1
            self.p2_keymap[i] = -1

        guide_text = ''
        for i in range(GUI_MoveIdMeter.FRAMES):
            if i % 5 == 0:
                guide_text += '|'
            elif (i + 3) % 5 == 0:
                if (i + 3) == 5:
                    guide_text += '0'
                else:
                    guide_text += str(i + 3)[0]
            elif (i + 2) % 5 == 0:
                if (i + 2) == 5:
                    guide_text += '5'
                else:
                    guide_text += str(i + 2)[1]
            else:
                guide_text += '.'

        self.frames_guide.insert(END, guide_text)

        for i, tag_color in GUI_MoveIdMeter.tag_colors.items():
            self.p1_text.tag_config(str(i), background=tag_color)
            self.p2_text.tag_config(str(i), background=tag_color)
            self.p1_key.tag_config(str(i), background=tag_color)
            self.p2_key.tag_config(str(i), background=tag_color)

        self.p1_current_move_ids = {}
        self.p2_current_move_ids = {}


    def update_meter(self, game_state:_GameStateManager.GameStateManager):

        try:
            highest_selection = max(len(self.p1_text.selection_get()), len(self.p2_text.selection_get()))
            self.selection_var.set('{:03} Frames Selected'.format(highest_selection))
        except:
            pass



        if self.current_frame != game_state.game_reader.timer:
            self.current_frame = game_state.game_reader.timer
            #print(game_state.game_reader.timer)
            last_x_frames = GUI_MoveIdMeter.FRAMES
            if len(game_state.game_reader.snapshots) > last_x_frames:

                prev_p1_move_id = -1
                prev_p2_move_id = -1
                p1_string = ''
                p2_string = ''

                self.p1_text.delete(1.0, END)
                self.p2_text.delete(1.0, END)

                for i in reversed(range(1, last_x_frames)):
                    snapshot = game_state.game_reader.snapshots[-i]
                    p1_move_id = snapshot.p1.movement_block.movelist_id
                    p2_move_id = snapshot.p2.movement_block.movelist_id
                    if p1_move_id != prev_p1_move_id:
                        prev_p1_move_id = p1_move_id
                        found_key = False
                        for key, value in self.p1_keymap.items():
                            if value == p1_move_id:
                                self.p1_counter = key
                                found_key = True
                                break
                        if not found_key:
                            self.p1_counter += 1
                            self.p1_counter = self.p1_counter % len(GUI_MoveIdMeter.p1_symbols)
                            self.p1_keymap[self.p1_counter] = p1_move_id
                    if p2_move_id != prev_p2_move_id:
                        prev_p2_move_id = p2_move_id
                        found_key = False
                        for key, value in self.p2_keymap.items():
                            if value == p2_move_id:
                                self.p2_counter = key
                                found_key = True
                                break
                        if not found_key:
                            self.p2_counter += 1
                            self.p2_counter = self.p2_counter % len(GUI_MoveIdMeter.p2_symbols)
                            self.p2_keymap[self.p2_counter] = p2_move_id
                    p1_string = GUI_MoveIdMeter.p1_symbols[self.p1_counter]
                    p2_string = GUI_MoveIdMeter.p2_symbols[self.p2_counter]

                    self.p1_text.insert(END, p1_string, str(self.p1_counter))
                    self.p2_text.insert(END, p2_string, str(self.p2_counter))







                self.p1_key.delete(1.0, END)
                for x, y in self.p1_keymap.items():
                    self.p1_key.insert(END, '{}: {}\n'.format(GUI_MoveIdMeter.p1_symbols[x], y), str(x))

                self.p2_key.delete(1.0, END)
                for x, y in self.p2_keymap.items():
                    self.p2_key.insert(END, '{}: {}\n'.format(GUI_MoveIdMeter.p2_symbols[x], y), str(x))














if __name__ == '__main__':
    root = Tk()
    my_gui = GUI_MoveIdMeter(root)
    #root.mainloop()
    #launcher = SoulCaliburGameState.SC6GameReader()
    launcher = _GameStateManager.GameStateManager()
    counter = 0
    while (True):
        counter += 1
        launcher.Update(False, False)

        root.update_idletasks()
        root.update()

        #if counter % 10 == 0:
        my_gui.update_meter(launcher)

        time.sleep(.005)