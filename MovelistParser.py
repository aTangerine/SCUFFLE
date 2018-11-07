
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

def b4i (bytes, index : int):
    return struct.unpack('I', bytes[index: index + 4])[0]

def b2i (bytes, index : int):
    return struct.unpack('H', bytes[index: index + 2])[0]

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
    def __init__(self, bytes, address):
        self.address = address
        self.bytes = bytes
        #print(len(self.bytes))
        #print(self.bytes[-4:])


class Movelist:
    HEADER_LENGTH = 0x30
    #STARTER_STRING = 'KH11'
    STARTER_INT = 0x3131484b
    def __init__(self, raw_bytes):

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
        for i in range(0, len(self.all_moves) - 2):
            ca = self.all_moves[i].cancel_address
            cancel = Cancel(raw_bytes[ca: self.all_moves[i + 1].cancel_address], ca)
            self.all_cancels[ca] = cancel
            #TODO: missing the very last cancel



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
                    if bytes[index: index + 1] == b'\x25':
                        if bytes[index + 1 : index + 2] in (b'\x03', b'\x07', b'\x14', b'\x0d'):
                            if bytes[index: index + 2] == b'\x25\x07':
                                if bytes[index + 2: index + 3] != b'\x01':
                                    Movelist.print_bytes(bytes[running_index: index + 3])
                            running_index = index + 3


    def print_bytes(byte_array):
        string = ' '.join('{:02x}'.format(x) for x in byte_array)
        print(string)

    def print_stuff(self, all_moves, all_cancels):

        print(len(all_cancels))
        print(len(all_moves))

        potential_bytes = []
        for attack in self.all_attacks:
            potential_bytes.append(hex(attack.block_effect))
        for cancel in all_cancels:
            pass

            #print(cancel.bytes)

            #potential_bytes.append(hex(b2i(cancel.bytes, 2)))
            #potential_bytes.append(len(cancel.bytes))
            #if cancel.bytes[2:4] != b'\x00\x8b':
            #if (len(cancel.bytes) >= 8):
                #potential_bytes.append(hex(b2i(cancel.bytes, 6)))
            #if len(cancel.bytes) < 10:
                #print ('{} : {} : {}'.format(hex(cancel.address), len(cancel.bytes), cancel.bytes))
        print(Counter(potential_bytes))





if __name__ == "__main__":
    #input_file = 'tira_movelist.byte.m0000'
    input_file = 'xianghua_movelist.byte.m0000' #these come from cheat engine, memory viewer -> memory regions -> (movelist address) . should be 0x150000 bytes

    with open(input_file, 'rb') as fr:
        raw_bytes = fr.read()
    movelist = Movelist(raw_bytes)
    movelist.print_stuff(movelist.all_moves, movelist.all_cancels)