from enum import Enum


class MoveState(Enum):
    neutral = 0
    crouching = 1
    downed_supine = 2  # face up
    downed_prone = 3  # face down
    hit_or_guard = 4
    starting_attack = 5
    guard_stand = 6
    guard_crouch = 7

    crouch_rising = 10
    guard_stand_start = 11
    guard_stand_release = 12
    guard_stand_to_crouch = 13
    guard_fast_duck_then_sidestep = 14 #looks like a duck and sidestep happens only on extremly fast step and guard
    guard_crouch_and_start_guarding = 15
    guard_crouch_start = 16
    guard_crouch_release = 17
    guard_release_and_stand = 18 #releasing guard at the same time as standing?
    guard_crouch_to_stand = 19
    guard_lying_to_stand = 20  # ???
    jump_up = 21
    jump_forward = 22
    jump_back = 23
    forwardstep_start = 24
    forwardstep_middle = 25
    forwardstep_walk = 26
    forwardstep_medium_stop = 27
    forwardstep_big_stop = 28
    forwardstep_bigger_stop = 29
    forwardstep_running_stop = 30
    running_unknown_31 = 31 #only accessible if running in another 8way direction first?
    running_unknown_32 = 32

    backstep_start = 33
    backstep_middle = 34
    backstep_backwalk = 35
    backstep_medium_stop = 36
    backstep_big_stop = 37


    backright_start = 39
    backright_start_middle = 40
    backright_start_sidewalk = 41
    backright_start_medium_stop = 42
    backright_start_big_stop = 43

    sidestep_right_start = 45
    sidestep_right_middle = 46
    sidestep_right_sidewalk = 47
    sidestep_right_medium_stop = 48
    sidestep_right_big_stop = 49

    forward_right_start = 51
    forward_right_middle = 52
    forward_right_sidewalk = 53
    forward_right_medium_stop = 54
    forward_right_big_stop = 55

    #59, 61, 44, and 38 are all backwalk weird states

    sidestep_left_start = 63  # all sidesteps start with this
    sidestep_left_middle = 64  # only the smallest sidesteps don't have this
    sidestep_left_sidewalk = 65  # you can get 8 way run moves without this
    sidestep_left_medium_stop = 66  # requires a 64 but not a 65
    sidestep_left_big_stop = 67  # only for 65 steps?

    forward_left_start = 69
    forward_left_middle = 70
    forward_left_sidewalk = 71
    forward_left_medium_stop = 72
    forward_left_big_stop = 73


    forwardstep_short_stop = 75
    forwardleft_short_stop = 76
    forwardright_short_stop = 77
    sidestep_left_short_stop = 78
    sidestep_right_short_stop = 79
    backstep_short_stop = 80
    backleft_short_stop = 81
    backright_short_stop = 82
    move_animation_playing = 83
    move_animation_playing_crouching = 84  # ??? not tech crouches, but actually crouching state? flags on forced crouched?

    move_animation_forward_throw = 86
    move_animation_back_throw = 87
    move_animation_airborne = 88  # true for juggles but also aerial attacks?
    move_finished = 89
    move_finished_crouching = 90 #????
    recovering_forward_throw = 91
    recovering_back_throw = 92
    recovering_from_heavy_block = 93  # occurs on guard breaks but also tira's gloomy 66k

    standing_to_supine = 97
    standing_to_prone = 98
    backturned_to_facing = 106 #hold towards opponent from backturn
    backturned_step_right = 107 #directions on these two moves are switched since we're backturned
    backturned_step_left = 108

    guard_turn_left = 109 #happens when you guard after backturn
    guard_turn_right = 110 #may not be guard only?
    downed_supine_to_standing = 113
    downed_prone_to_standing = 114
    downed_prone_to_standing_backturned = 115




class HitLevel(Enum):
    high_49 = 0x49
    high_6d = 0x6D #tira 4K


    mid_4b = 0x4b #common
    mid_24 = 0x24  # rising/launching mid? i think this is a substition value, doesn't give mid property when assigned in the editor to other moves
    mid_6f = 0x6f  # crouching mid?

    low_37 = 0x37 #common
    low_13 = 0x13 #crouching low?

    sm_5b = 0x5b
    sm_7f = 0x7F  # soul charge activation, also ivy backturned B+K

    sl_1b = 0x1b
    sl_63 = 0x63

    throw = 0x81 #most throws
    throw_ast = 0xC1 #astaroth throws
    throw_mid = 0x82 #mids

    UB_mid_43 = 0x43 #maybe only at end?
    UB_mid_67 = 0x67  # maybe only at end?
    UB_mid_47 = 0x47

    UB_high_41 = 0x41
    UB_high_63 = 0x63 #from editing move list



class LaunchType(Enum):
    none = 0x0
    STN = 0x01
    LNC = 0x02
    KND = 0x03
















