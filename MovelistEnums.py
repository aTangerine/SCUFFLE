from enum import Enum

class Button(Enum):
    A = 0x01
    B = 0x02
    K = 0x04
    G = 0x08

    B_K = 0x06
    A_B = 0x03
    A_G = 0x09
    K_G = 0x0C

    A_B_K = 0x07


class PaddedButton(Enum):
    A = 0x0001
    B = 0x0002
    K = 0x0004

    B_K = 0x0600
    A_B = 0x0300
    A_G = 0x0900
    K_G = 0x0C00

    A_B_K = 0x0700

class InputType(Enum):
    Button = 0x06
    HoldButton = 0x20
    OnHit = 0x0B #counter hit uses the same code signature but are about 3x as long so the counterhit part must be in there somewhere
    #PressDown = 0x13af /0x13ae ??
    #PressBack =  0x0002 /0x1002 ??
    #0x0120 #geralt, super?? + hold button

class CC(Enum): #Cancel codes for the cancel block, mostly we expect (CC XX XX CC XX XX ...) where CC is the cancel codes and XX is the variable provided to them
    START = 0x01 #begins every block(?)
    END = 0x02  # this byte ends the block

    EXE_25 = 0x25 #all EXE blocks have the seecond argument as the number of instructions since the last non 8b/89 block (mostly true)
    EXE_19 = 0x19 #very common in neutral blocks
    EXE_A5 = 0xA5
    EXE_13 = 0x13 #very rare, yoshimitsu only???

    ARG_89 = 0x89 #the ARG blocks provide arguments to the EXE blocks
    ARG_8B = 0x8b
    ARG_8A = 0x8a #may not be an arg field???

    PEN_2A = 0x2A #the variables for these blocks stay the same or increase (although they may start in the middle of the block and 'wrap' around to the top)
    PEN_28 = 0x28
    PEN_29 = 0x29

    SINGLE_00 = 0x00
    SINGLE_03 = 0x03
    SINGLE_04 = 0x04
    SINGLE_05 = 0x05
    SINGLE_07 = 0x07
    SINGLE_08 = 0x08
    SINGLE_0b = 0x0b
    SINGLE_0d = 0x0d
    SINGLE_0e = 0x0e
    SINGLE_0f = 0x0f
    SINGLE_10 = 0x10
    SINGLE_12 = 0x12
    SINGLE_13 = 0x13
    SINGLE_14 = 0x14
    SINGLE_1a = 0x1a
    SINGLE_1b = 0x1b
    SINGLE_1c = 0x1c
    SINGLE_1e = 0x1e
    SINGLE_23 = 0x23
    SINGLE_32 = 0x32
    SINGLE_42 = 0x42
    SINGLE_4c = 0x4c
    SINGLE_4d = 0x4d
    SINGLE_5c = 0x5c
    SINGLE_5d = 0x5d
    SINGLE_61 = 0x61
    SINGLE_68 = 0x68
    SINGLE_6b = 0x6b
    SINGLE_74 = 0x74
    SINGLE_77 = 0x77
    SINGLE_78 = 0x78
    SINGLE_7a = 0x7a
    SINGLE_7e = 0x7e
    SINGLE_88 = 0x88
    SINGLE_8c = 0x8c
    SINGLE_8d = 0x8d
    SINGLE_8e = 0x8e
    SINGLE_8f = 0x8f
    SINGLE_91 = 0x91
    SINGLE_92 = 0x92
    SINGLE_94 = 0x94
    SINGLE_95 = 0x95
    SINGLE_96 = 0x96
    SINGLE_98 = 0x98
    SINGLE_99 = 0x99
    SINGLE_9e = 0x9e
    SINGLE_9f = 0x9f
    SINGLE_a0 = 0xa0
    SINGLE_a1 = 0xa1
    SINGLE_a2 = 0xa2
    SINGLE_a3 = 0xa3
    SINGLE_a4 = 0xa4
    SINGLE_ab = 0xab
    SINGLE_ac = 0xac
    SINGLE_ad = 0xad
    SINGLE_ae = 0xae
    SINGLE_af = 0xaf
    SINGLE_b1 = 0xb1
    SINGLE_b3 = 0xb3
    SINGLE_f0 = 0xf0
    SINGLE_fb = 0xfb



