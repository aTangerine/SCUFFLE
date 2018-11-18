
'''
MOVELIST STRUCTURE
[header]

[list of every possible move]
    [includes animation, length, and links to attack and cancel blocks]

[list of every possible attack info]
    [includes high/low, block stun, startup, etc.]

[0xAC bytes of ???]

[0x600 brief short section, possibly on cinematic things. first entry is Soul Charge]







[bunch of cancel info???]

'''


import struct
from collections import Counter
from MovelistEnums import *

def b4i (bytes, index : int):
    return struct.unpack('I', bytes[index: index + 4])[0]

def b2i (bytes, index : int , big_endian = False):
    if not big_endian:
        return struct.unpack('H', bytes[index: index + 2])[0]
    else:
        return struct.unpack('>H', bytes[index: index + 2])[0]



def b1i (bytes, index : int):
    return struct.unpack('B', bytes[index: index + 1])[0]

def b4f (bytes, index : int):
    return struct.unpack('f', bytes[index: index + 4])[0]

class Move:
    LENGTH = 0x48
    def __init__(self, bytes):

        self.animation = b4i(bytes, 0x00)
        self.unknown_04 = b4i(bytes, 0x04)
        self.motion_multiplier = b4f(bytes, 0x08)
        self.speed_multiplier = b4f(bytes, 0x0C)
        self.unknown_10 = b4i(bytes, 0x10)

        self.unknown_multiplier = b4i(bytes, 0x30)
        self.total_frames = b2i(bytes, 0x34)
        self.cancel_address = b4i(bytes, 0x38)
        self.attack_index = b2i(bytes, 0x3C)
        #last 12 bytes are fffffff?




class Attack:
    LENGTH = 0x70
    def __init__(self, bytes):
        self.bytes = bytes

        self.hitbox = b2i(self.bytes, 0) #hitbox limb?? 40 40 = right leg? 80 80 = left leg ??
        self.mystery_02 = b2i(self.bytes, 2) #Counter({128: 125, 0: 43, 17: 21, 2560: 18, 1: 14, 6144: 11, 2048: 10, 512: 10, 2: 9, 6784: 8, 51: 8, 4096: 6, 162: 4, 4608: 4, 34: 4, 513: 4, 640: 3, 641: 3, 3: 2, 129: 2, 3072: 1, 2099: 1})

        self.mystery_08 = b2i(self.bytes, 0x08) #Counter({0: 51, 10: 45, 40: 29, 20: 24, 100: 23, 80: 21, 30: 16, 60: 12, 85: 11, 50: 10, 110: 8, 120: 8, 70: 7, 90: 7, 140: 6, 160: 5, 125: 4, 75: 3, 150: 3, 95: 3, 45: 3, 65: 2, 130: 2, 5: 2, 142: 2, 155: 2, 15: 1, 175: 1})
        #there's 4, possibly 5 repeating-ish similar byte series here, poossibly corresponding to hitboxes? hurtboxes?
        #moving an ec ff (tira's 5k) over one byte on accident resulted in a 'pop' up on hit

        #0x0E controls launch height on hit
        #0x14 controls counter launch height on hit

        self.mystery_20 = b2i(self.bytes, 0x20) #5a, b4 ???

        self.mystery_24 = b2i(self.bytes, 0x24) #b0 ff, 48??

        self.mystery_26 = b2i(self.bytes, 0x26)#00  #e2ff

        self.mystery_2A = b2i(self.bytes, 0x2A) #14 # 00 #46

        self.hit_level = b2i(self.bytes, 0x32)
        self.strange_guard = b2i(self.bytes, 0x34) #this number is 0, 1, 2, 4, 8, or 16 (for tira). Changing it can change if it can cause guard crushes as well as influence the guard damage
        self.startup = b2i(self.bytes, 0x36)
        self.active = b2i(self.bytes, 0x38) #usually 1 or 2 higher than startup, possible when active frames end?
        self.damage = b2i(self.bytes, 0x3A)

        self.block_stun = b2i(self.bytes, 0x44)
        self.hit_stun = b2i(self.bytes, 0x46)
        self.counter_stun = b2i(self.bytes, 0x48)

        self.b2 = b2i(self.bytes, 0x4A) #for all but maybe 5 moves (for Tira), these values are the exact same as the stun value,
        self.h2 = b2i(self.bytes, 0x4C)
        self.c2 = b2i(self.bytes, 0x4E)

        self.hit_effect = b2i(self.bytes, 0x50) #this may be two sepearate 1 byte enums
        self.counter_effect = b2i(self.bytes, 0x52)

        self.mystery_54 = b1i(self.bytes, 0x54) #Counter({0: 172, 17: 74, 5: 23, 12: 8, 18: 8, 11: 7, 29: 6, 8: 3, 32: 2, 33: 2, 24: 2, 35: 1, 9: 1, 41: 1, 30: 1})
        self.mystery_55 = b1i(self.bytes, 0x55) #Always 4

        self.block_effect = b1i(self.bytes, 0x56)  #CE forces crouching     #Counter({214: 57, 184: 32, 218: 25, 202: 22, 200: 14, 179: 13, 206: 12, 167: 12, 169: 11, 170: 10, 173: 10, 226: 8, 185: 7, 233: 6, 174: 6, 181: 6, 248: 5, 188: 5, 208: 4, 209: 4, 223: 4, 232: 4, 203: 3, 222: 3, 228: 3, 183: 3, 251: 3, 194: 2, 195: 2, 201: 2, 216: 2, 220: 2, 221: 2, 224: 2, 207: 1, 225: 1, 239: 1, 186: 1, 189: 1})
        self.mystery_57 = b1i(self.bytes, 0x57) #Always 3

        self.mystery_58 = b1i(self.bytes, 0x58) #almost always the same as 0x56, 20 or so differences, just frame guard effect perhaps???

        self.mystery_5A = b2i(self.bytes, 0x5A) #changes guard damage, 0 is 0, 0x0002 makes guard damage 512 # Counter({65533: 225, 0: 31, 2: 14, 40: 12, 20: 5, 6: 4, 80: 4, 8: 4, 10: 3, 120: 3, 50: 2, 9: 1, 15: 1, 25: 1, 9999: 1})

        self.mystery_5C = b2i(self.bytes, 0x5C) #Counter({0: 257, 32: 32, 40: 12, 1: 8, 33: 1, 41: 1})

        self.strange_guard2 = b2i(self.bytes, 0x5E) #Another, possibly primary, guard crush determiner, but not the sole one?

        self.mystery_60 = b2i(self.bytes, 0x60) #always the same as 0x5e, possibly another just guard??? see 0x58

        self.mystery_62 = b2i(self.bytes, 0x62) #????

        self.mystery_64 = b2i(self.bytes, 0x64)  # ????

        self.mystery_66 = b2i(self.bytes, 0x66)  # ????

        self.ffff_1 = b4i(self.bytes, 0x68)  # ????
        self.ffff_2 = b4i(self.bytes, 0x6C)  # ????







class Cancel:
    def __init__(self, bytes, address, move_id):
        self.address = address
        self.bytes = bytes
        self.move_id = move_id


        #print(len(self.bytes))
        #print(self.bytes[-4:])


class Link:
    def __init__(self, conditions, move_id):
        self.conditions = conditions
        self.move_id = move_id
        self.hold = False

        #if self.move_id == 264:
        #print(self.move_id)
        #print(self.conditions)
        #print("----------")
        self.button_press = self.parse_button()

        self.auto_cancel = self.parse_auto_cancel()

    def get_command_string(self):
        if self.is_auto_cancel and not self.button_press:
            return '.'
        if self.hold:
            return '[{}]'.format(self.button_press.name)
        return self.button_press.name

    def parse_button(self):
        for type, c in self.conditions:
            index = 0

            while index < len(c) - 5:
                b = int(c[index]) #we're looking for the pattern 8b 00 06 8b [button argument]
                if b == 0x8b:
                    arg_1 = b2i(c, index + 1, big_endian=True)
                    if arg_1 == InputType.Press.value or arg_1 == InputType.No_SC_Press.value:
                        if (int(c[index + 3]) == 0x8b):
                            arg_2 = b2i(c, index + 4, big_endian=True)
                            if enum_has_value(PaddedButton, arg_2):
                                return PaddedButton(arg_2)
                    if arg_1 == InputType.Hold.value:
                        if (int(c[index + 3]) == 0x8b):
                            arg_2 = b2i(c, index + 4, big_endian=True)
                            if enum_has_value(PaddedButton, arg_2):
                                self.hold = True
                                return PaddedButton(arg_2)

                index += 3
        return None

    def parse_auto_cancel(self):
        if len(self.conditions) == 1:
            if len(self.conditions[0][1]) == 3: #this move auto cancels at a specific frame
                if int(self.conditions[0][1][0]) == 0x89:
                    return True
            if len(self.conditions[0][1]) == 6: #this move auto cancels during soul charge??
                if int(self.conditions[0][1][0]) == 0x89 and int(self.conditions[0][1][3]) == 0x8b:
                    return True
        elif len(self.conditions) == 0:
            return True
        return False

    def is_auto_cancel(self):
        return self.auto_cancel

    def is_button_press(self):
        if self.button_press == None:
            return False
        else:
            return True

class Movelist:
    HEADER_LENGTH = 0x30
    #STARTER_STRING = 'KH11'
    STARTER_INT = 0x3131484b

    THREE_BYTE_INSTRUCTIONS = [CC.START, CC.ARG_8A, CC.ARG_8B, CC.ARG_89, CC.EXE_19, CC.EXE_25, CC.EXE_A5, CC.EXE_13, CC.PEN_2A, CC.PEN_28, CC.PEN_29]

    def __init__(self, raw_bytes, name):
        self.name = name.replace('/', '')

        header_index_1 = 0xC
        header_index_2 = 0x10 # to attacks info
        header_index_3 = 0x14 # very short byte block
        header_index_4 = 0x18 # cinematics info
        header_unknown_1c = 0x1c
        header_unknown_20 = 0x20 #same as 0x1c in tira
        header_unknown_24 = 0x24 #??
        header_unknown_28 = 0x28
        header_unknown_2C = 0x2C

        move_block_start = 0x30
        attack_block_start = b4i(raw_bytes, header_index_2)
        short_block_start = b4i(raw_bytes, header_index_3)

        move_block_bytes = raw_bytes[move_block_start: attack_block_start]

        self.all_moves = []
        for i in range(0, len(move_block_bytes) - Move.LENGTH, Move.LENGTH):
            move = Move(move_block_bytes[i: i + Move.LENGTH])
            self.all_moves.append(move)

        attack_block_bytes = raw_bytes[attack_block_start: short_block_start]
        self.all_attacks = []
        for i in range(0, len(attack_block_bytes) - Attack.LENGTH, Attack.LENGTH):
            attack = Attack(attack_block_bytes[i: i + Attack.LENGTH])
            self.all_attacks.append(attack)

        self.all_cancels = {}
        self.move_ids_to_cancels = {}
        for i in range(0, len(self.all_moves) - 1):
            ca = self.all_moves[i].cancel_address
            cancel = Cancel(raw_bytes[ca: self.all_moves[i + 1].cancel_address], ca, i)
            self.all_cancels[ca] = cancel
            self.move_ids_to_cancels[i] = cancel

        self.move_ids_to_commands = self.parse_neutral()

        move_ids_to_check = list(self.move_ids_to_commands.keys())

        while len(move_ids_to_check) > 0:
            move_id = move_ids_to_check.pop(0)
            original_command = self.move_ids_to_commands[move_id]
            #ids_to_commands = self.parse_move(move_id)
            ids_to_commands = {}
            for link in self.condition_parse(move_id):
                if link.is_button_press() or link.is_auto_cancel():
                    ids_to_commands[link.move_id] = link.get_command_string().replace('_', '+')

            for cancelable_move_id in ids_to_commands:
                if not cancelable_move_id in self.move_ids_to_commands.keys():
                    new_command = ids_to_commands[cancelable_move_id]
                    if '['  in new_command:
                        self.move_ids_to_commands[cancelable_move_id] = '{}'.format(original_command[:2 - len(new_command)] + new_command)
                    else:
                        self.move_ids_to_commands[cancelable_move_id] = '{}{}'.format(original_command, new_command)
                    move_ids_to_check.append(cancelable_move_id)




    def get_command_by_move_id(self, move_id):
        if move_id in self.move_ids_to_commands:
            return self.move_ids_to_commands[move_id]
        else:
            return '???'

    def print_cancel_bytes_by_move_id(self, move_id):
        if move_id < len(self.all_moves):
            print(move_id)
            attack_index = self.all_moves[move_id].attack_index
            if attack_index < len(self.all_attacks):
                print(attack_index)
                attack = self.all_attacks[attack_index]
                Movelist.print_bytes(attack.bytes)


                cancel_address = self.all_moves[move_id].cancel_address
                bytes = self.all_cancels[cancel_address].bytes


                print(hex(attack.hit_effect))
                cancel_frames = []
                running_index = 0
                for index in range(0, len(bytes), 1):
                    if int(bytes[index + 1 : index + 2]) in [CC.EXE_25.value, CC.EXE_19.value]:
                        footer = bytes[index: index + 3]
                        if footer[:2] == b'\x25\x07': #or footer == b'\x25\x0d\x06':
                            if bytes[index + 2: index + 3] != b'\x01' or False:
                                move_cancel_bytes = bytes[running_index: index + 3]
                                Movelist.print_bytes(move_cancel_bytes)
                                self.parse_move_cancel(move_cancel_bytes)
                        running_index = index + 3


    def parse_move_cancel(self, bytes):
        buffer_89 = bytes.split(b'\x89')
        #buffer_89 = [x[:2] for x in buffer_89]

        buffer_8B = bytes.split(b'\x8B')
        #buffer_8B = [x[:2] for x in buffer_8B]

        buffer_89.pop(0) #this is the stuff before 89, which we don't care about and will make our indexes weird
        buffer_8B.pop(0)

        win_start = self.search_for_cancel_arg(buffer_89, 0, -1)
        if len(buffer_89[0]) == 2: #if the second 89 is directly after the first, then we have an exit window as well
            win_end = self.search_for_cancel_arg(buffer_89, 1, -1)
        else:
            win_end = -2

        cancel_type = self.search_for_cancel_arg(buffer_8B, 0, -1)
        cancel_type_arg = self.search_for_cancel_arg(buffer_8B, 1, -1)

        next_move = self.search_for_cancel_arg(buffer_8B, -1, -1)

        print('cancel: {}-{}  x{} input: {} / {}'.format(win_start, win_end, next_move, hex(cancel_type), hex(cancel_type_arg)))


    def search_for_cancel_arg(self, array, index, default):
        if index < len(array) and len(array) >= 2:
            return b2i(array[index], 0, big_endian=True)
        else:
            return default

    def print_bytes(byte_array):
        string = Movelist.bytes_as_string(byte_array)
        print(string)

    def bytes_as_string(byte_array):
        return ' '.join('{:02x}'.format(x) for x in byte_array)



    def from_file(filename):
        with open(filename, 'rb') as fr:
            raw_bytes = fr.read()
        return Movelist(raw_bytes, filename)

    def parse_move(self, move_id):
        move_ids_to_commands = {}

        if move_id in self.move_ids_to_cancels.keys():
            cancel = self.move_ids_to_cancels[move_id]
        else:
            return move_ids_to_commands

        i = 0
        buf_8b = [-1, -1, -1, -1, -1]
        buf_89 = [-1, -1, -1, -1, -1]

        button_code = -1
        button_code_code = -1

        expecting_cancel = False

        while i < len(cancel.bytes):
            raw = int(cancel.bytes[i])
            inst = CC(raw)
            if inst in Movelist.THREE_BYTE_INSTRUCTIONS:
                arg = b2i(cancel.bytes, i + 1, big_endian=True)
                if inst == CC.ARG_8B:
                    buf_8b.append(arg)
                if inst == CC.ARG_89:
                    buf_89.append(arg)
                if inst == CC.EXE_A5:
                    if arg == 0x0102 or arg == 0x0103 or arg == 0x1402:
                        button_code = buf_8b[-1]
                        button_code_code = buf_8b[-2]
                    if arg == 0x2502:
                        expecting_cancel = True
                if inst == CC.EXE_25:
                    if expecting_cancel or True:
                        expecting_cancel = False
                        clean_arg = arg >> 8
                        if clean_arg == 0x07:
                            move_id = buf_8b[-1]
                            if move_id < len(self.move_ids_to_cancels):
                                button = Movelist.button_parse(button_code_code, button_code)
                                move_ids_to_commands[move_id] = button
                                #print('{} -> x{}'.format(button, buf_8b[-1]))

            if inst in Movelist.THREE_BYTE_INSTRUCTIONS:
                i += 3
            else:
                i += 1

        return move_ids_to_commands


    def button_parse(type_code, input_code):
        if enum_has_value(InputType, type_code) and enum_has_value(PaddedButton, input_code):
            type = InputType(type_code)
            input = PaddedButton(input_code)
            if type == InputType.Press:
                return '{}'.format(input.name)
            elif type == InputType.Direction or type == InputType.Direction_ALT:
                codes_to_directions = {
                    PaddedButton.Forward : '6',
                    PaddedButton.Forward_ALT: '6',


                }
                if input in codes_to_directions.keys():
                    return'{}'.format(codes_to_directions[input])
                else:
                    return 'dir {:04x}'.format(input_code)

            elif type == InputType.Hold:
                return '[{}]'.format(input.name)
            else:
                return '{} {}'.format(type.name, input.name)
        else:
            try:
                return '{:04x}:{:04x}'.format(type_code, input_code)
            except Exception as e:
                import sys
                print ('{} {}'.format(type_code, input_code), file=sys.stderr)
                raise e


    def parse_neutral(self):
        cancels = sorted(self.all_cancels.values(), key=lambda x: x.bytes.count(b'\x19')) # incredibly hackish way to find neutral
        move_ids_to_commands = {}
        for cancel in (cancels[-50:]):

            #state machine variables
            args_expected = 0
            buf_89 = [-1, -1, -1, -1, -1]
            buf_8a = [-1, -1, -1, -1, -1]
            buf_8b = [-1, -1, -1, -1, -1]
            button_code = None
            next_8b_is_input = False
            next_19_is_normal_move = False
            next_19_is_8way_move = False
            next_19_is_backturned_move = False
            while_crouching_flag = False
            while_standing_signs = [-1]
            buffers = [buf_89, buf_8a, buf_8b]


            for i in range(len((cancel.bytes))):
                if args_expected != 0:
                    args_expected -= 1
                else:
                    inst = int(cancel.bytes[i])
                    try:
                        next_instruction = CC(inst)
                    except Exception as e:
                        print('ERROR move_id:{} hex:{}'.format(cancel.move_id, hex(inst)))
                        #unlisted_singles.append((inst, i))
                        next_instruction = inst
                        #raise e



                    #if it's an argument instruction, we store it for future use in an exe instruction
                    if next_instruction in Movelist.THREE_BYTE_INSTRUCTIONS:
                        args_expected = 2
                    else:
                        next_8b_is_input = False
                    if next_instruction in [CC.ARG_89, CC.ARG_8A, CC.ARG_8B]:
                        try:
                            buffers[abs(0x89 - inst)].append(b2i(cancel.bytes[i+1:], 0, big_endian = True))
                        except Exception as e:
                            print('error move_id: {} inst: {} counter: {}'.format(cancel.move_id, hex(inst), i))
                            raise e

                        if next_instruction == CC.ARG_8A:
                            if buf_8a[-1] == 0x0102 or buf_8a[-1] == 0x0101 or buf_8a[-1] == 0x0103: #input marker
                                next_8b_is_input = True
                            if buf_8a[-1] == 0x0103:
                                next_19_is_8way_move = True
                            if buf_8a[-1] == 0x003D:
                                next_19_is_normal_move = True
                            if buf_8a[-1] == 0x0048:
                                #next_19_is_backturned_move = True
                                next_19_is_normal_move = True
                        if next_instruction in [CC.ARG_8B]:
                            if next_8b_is_input:
                                button_code = buf_8b[-1]
                                next_8b_is_input = False
                    #if it's an exe instruction, we 'execute' it, reading from the proper buffers to provide arguments
                    if next_instruction in [CC.EXE_19]:
                        move_id, dir = buf_8b[-1], buf_89[-1]
                        try:
                            button = PaddedButton(button_code).name
                            button = button.replace('_', '+')
                        except Exception as e:
                            button = button_code

                        if dir == 0x0096 or dir == 0x0097:
                            dir = 'bt'

                        if buf_89[-1] == 0xffff: #dunno what these are, but they aren't moves???
                            next_19_is_8way_move = False
                            next_19_is_normal_move = False

                        elif next_19_is_normal_move or next_19_is_8way_move:
                            if not while_crouching_flag and next_19_is_normal_move: #hack way to guess when we've reached while crouching moves
                                if button_code in while_standing_signs:
                                    if button_code != while_standing_signs[-1]:
                                        while_crouching_flag = True
                                else:
                                    while_standing_signs.append(button_code)

                            command = '{}{}'.format(dir, button)

                            if next_19_is_8way_move:
                                command = '{}{}'.format(dir, command)
                            elif while_crouching_flag:
                                pass #TODO: better way to detect WC?
                                #command = 'WC {}'.format(command)


                            do_replace = True
                            if move_id in move_ids_to_commands.keys():
                                if '6' in move_ids_to_commands[move_id] or '4' in move_ids_to_commands[move_id]:
                                    do_replace = False

                            if do_replace:
                                move_ids_to_commands[move_id] = command

                            #cleanup
                            next_19_is_normal_move = False
                            next_19_is_8way_move = False
                            next_19_is_backturned_move = False

        return move_ids_to_commands

    def pen_parse(self, move_id):
        bytes = self.move_ids_to_cancels[move_id].bytes

        paper = []
        for _ in range(4 * len(bytes)):
            #paper.append(int(b'\x00'))
            paper.append(0)

        pos = 0
        index = 0
        while index < len(bytes):
            inst =  CC(int(bytes[index]))
            if inst in (CC.PEN_2A, CC.PEN_28, CC.PEN_29):
                arg = b2i(bytes, index + 1, big_endian=True)
                pos = arg
                index += 3
            elif inst in (CC.ARG_8B, CC.ARG_8A, CC.ARG_89):
                for _ in range(3):
                    paper[pos] = int(bytes[index])
                    pos += 1
                    index += 1
            elif inst in (CC.EXE_25, CC.EXE_A5, CC.EXE_19, CC.EXE_13):
                #print('{} {}: ({})'.format(inst, pos, Movelist.bytes_as_string((paper[max(pos - 29, 0):pos]))))
                if inst == CC.EXE_25:
                    print('{} {} {} [{}]: ({})'.format(inst, int(bytes[index + 1]), int(bytes[index + 2]), pos, Movelist.bytes_as_string((paper[max(pos - 30, 0):pos]))))
                index += 3
            else:
                paper[pos] = int(bytes[index])
                print('{}'.format(paper[pos]))
                pos += 1
                index += 1

        print(paper)

    def condition_parse(self, move_id):
        if not move_id < len(self.move_ids_to_cancels) or move_id < 0:
            return []
        else:
            bytes = self.move_ids_to_cancels[move_id].bytes
            buf_all = []

            links = []

            conditions = []
            index = 0
            buf_8b = []
            while index < len(bytes):
                inst = CC(int(bytes[index]))
                if inst == CC.START:
                    index += 3
                elif inst in (CC.PEN_2A, CC.PEN_28, CC.PEN_29):
                    #arg = b2i(bytes, index + 1, big_endian=True)
                    #pos = arg
                    index += 3
                elif inst in (CC.ARG_8B, CC.ARG_8A, CC.ARG_89):
                    if inst == CC.ARG_8B:
                        arg = b2i(bytes, index + 1, big_endian=True)
                        buf_8b.append(arg)

                    for _ in range(3):
                        buf_all.append(int(bytes[index]))
                        index += 1

                elif inst in (CC.EXE_25, CC.EXE_A5, CC.EXE_19, CC.EXE_13):
                    # print('{} {}: ({})'.format(inst, pos, Movelist.bytes_as_string((paper[max(pos - 29, 0):pos]))))
                    if inst == CC.EXE_A5: #add condition
                        condition_type = int(bytes[index + 1])
                        condition_arg_number = int(bytes[index + 2])
                        args = bytes[index - (3 * condition_arg_number): index]
                        conditions.append((condition_type, args))

                    if inst == CC.EXE_25: #add cancel
                        if len(conditions) > 0:
                            for type, args in conditions:
                                pass
                                #print('{} : {}'.format(type, Movelist.bytes_as_string(args)))

                        condition_type = int(bytes[index + 1])
                        condition_arg_number = int(bytes[index + 2])
                        args = bytes[index - (3 * condition_arg_number): index]
                        state = -1
                        for i, b in enumerate(args):
                            if b == 0x8b:
                                state = b2i(args, i + 1, big_endian=True)
                                if not state == 0x30CC: #soul charge marker, keep going
                                    break
                        links.append(Link(conditions, state))
                        #print('{} {} {}: ({})'.format(inst, int(bytes[index + 1]), int(bytes[index + 2]), state))

                        conditions = []
                    index += 3
                else:
                    #paper[pos] = int(bytes[index])
                    #print('{}'.format(inst))
                    #conditions = []
                    index += 1

            return links





if __name__ == "__main__":
    import os
    def load_all_movelists():

        directory = 'movelists/'

        movelists = []
        for filename in os.listdir(directory):
            if filename.endswith('.m0000'):
                localpath = '{}/{}'.format(directory, filename)
                movelist = Movelist.from_file(localpath)
                movelists.append(movelist)
        return movelists

    #input_file = 'tira_movelist.byte.m0000'

    def print_out_cancel_blocks(movelist, fw):
        for cancel in sorted(movelist.all_cancels.values(), key=lambda x: len(x.bytes)):
            running_index = 0
            check_for_end = False
            fw.write('#{}\n'.format(cancel.move_id))
            index = 0
            while index < len(cancel.bytes):
                # if cancel.bytes[index: index + 3] == b'\x25\x0d\05':
                # Movelist.print_bytes(cancel.bytes[index - 18: index + 2])
                bytes = cancel.bytes
                if check_for_end:
                    if bytes[index: index + 2] == b'\x02':
                        fw.write('02\n')
                        fw.write('-------------------------------\n')
                        break

                next_byte = int(bytes[index])

                if next_byte in [CC.EXE_13.value, CC.EXE_19.value, CC.EXE_25.value, CC.EXE_A5.value]:
                    fw.write(Movelist.bytes_as_string(bytes[running_index: index + 3]) + '\n')
                    running_index = index + 3
                    check_for_end = True
                    index += 2
                elif next_byte in [CC.START.value, CC.ARG_8B.value, CC.ARG_8A.value, CC.ARG_89.value, CC.PEN_29.value, CC.PEN_28.value, CC.PEN_2A.value]:
                    index += 2
                index += 1

    #input_file = 'movelists/xianghua_movelist.byte.m0000' #these come from cheat engine, memory viewer -> memory regions -> (movelist address) . should be 0x150000 bytes




    counted_bytes = []

    #movelists = load_all_movelists()
    #movelists = [Movelist.from_file('movelists/tira_movelist.m0000')]
    movelists = [Movelist.from_file('movelists/seong_mina_movelist.m0000')]
    #movelists = [Movelist.from_file('movelists/yoshimitsu_movelist.m0000')]
    #movelists = [Movelist.from_file('movelists/xianghua_movelist.m0000')]


    '''for movelist in movelists:
        with open('cancels/c_{}'.format(movelist.name), 'w') as fw:
            print('making cancels for {}'.format(movelist.name))
            print_out_cancel_blocks(movelist, fw)'''

    #cancels = sorted(movelists[0].all_cancels.values(), key = lambda x: x.bytes.count(b'\x19'))
    #hack_neutral = (cancels[-1]) #incredibly hackish way to find neutral
    #print(movelists[0].parse_neutral())

    #movelists[0].pen_parse(257)
    #links = movelists[0].condition_parse(257)
    #links = movelists[0].condition_parse(259)
    print('XXXXXXXXXXXXXXXXXXXX\n\n\n\n')
    links = movelists[0].condition_parse(275)

    for link in links:
        if link.is_button_press():
            print('{} -> {}'.format(link.button_press, link.move_id))
        if link.is_auto_cancel:
            print('auto -> {}'.format(link.move_id))

    '''unlisted_singles = []
    for movelist in movelists:
        for cancel in movelist.all_cancels.values():
            try:
                unlisted_singles += Movelist.parse_neutral(cancel)
            except Exception as e:
                print('ERROR: movelist {}'.format(movelist.name))
                raise e
    print('\n'.join('SINGLE_{:02x} = 0x{:02x}'.format(x, x) for x in sorted(set([y[0] for y in unlisted_singles]))))'''

    #for i in range(len(unlisted_singles) - 1):
        #if unlisted_singles[i][1] == unlisted_singles[i + 1][1] + 1:
            #print('potential inst:{:02x}'.format(unlisted_singles[i][0]))

    print(sorted(Counter(counted_bytes)))


