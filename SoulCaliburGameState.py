import AddressMap

from ByteTools import *
#import ModuleEnumerator
import PIDSearcher
import GameplayEnums
import MovelistParser

class SC6GameReader:
        def __init__(self):
            self.pid = -1
            self.module_address = 0x140000000 #hard coding this until it breaks, then use ModuleEnumerator again
            self.snapshots = []
            self.p1_movelist = None
            self.p2_movelist = None

        def IsForegroundPID(self):
            pid = c.wintypes.DWORD()
            active = c.windll.user32.GetForegroundWindow()
            active_window = c.windll.user32.GetWindowThreadProcessId(active, c.byref(pid))
            return pid.value == self.pid

        def GetWindowRect(self):
            # see https://stackoverflow.com/questions/21175922/enumerating-windows-trough-ctypes-in-python for clues for doing this without needing focus using WindowsEnum
            if self.IsForegroundPID():
                rect = c.wintypes.RECT()
                c.windll.user32.GetWindowRect(c.windll.user32.GetForegroundWindow(), c.byref(rect))
                return rect
            else:
                return None

        def HasWorkingPID(self):
            return self.pid > -1

        def VoidPID(self):
            self.pid = -1

        def VoidMovelists(self):
            self.p1_movelist = None
            self.p2_movelist = None

        def UpdateCurrentSnapshot(self):
            if not self.HasWorkingPID():
                self.pid = PIDSearcher.GetPIDByName(b'SoulcaliburVI.exe')
                if self.HasWorkingPID():
                    print("Soul Calibur VI process id acquired: {}".format(self.pid))
                else:
                    print("Failed to find processid. Trying to acquire...")

            if self.HasWorkingPID():
                process_handle = OpenProcess(0x10, False, self.pid)

                test_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.test_breadcrumb, 0x08)
                test_value = GetValueFromDataBlock(test_block, 0x00)

                if test_value == 0: #not in a fight yet or application closed
                    self.VoidPID()
                    self.VoidMovelists()
                    return False
                else:
                    if self.p1_movelist == None:
                        #movelist_sample = GetValueFromAddress(process_handle, AddressMap.p1_movelist_address, isString=True)
                        movelist_sample = GetDataBlockAtEndOfPointerOffsetList(process_handle, 0, [AddressMap.p1_movelist_address], 0x4)
                        movelist_sample = GetValueFromDataBlock(movelist_sample, 0)

                        if  movelist_sample == MovelistParser.Movelist.STARTER_INT:
                            p1_movelist_data = GetDataBlockAtEndOfPointerOffsetList(process_handle, 0, [AddressMap.p1_movelist_address], AddressMap.MOVELIST_BYTES)
                            p2_movelist_data = GetDataBlockAtEndOfPointerOffsetList(process_handle, 0, [AddressMap.p2_movelist_address], AddressMap.MOVELIST_BYTES)
                            self.p1_movelist = MovelistParser.Movelist(p1_movelist_data)
                            self.p2_movelist = MovelistParser.Movelist(p2_movelist_data)

                    p1_startup_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p1_startup_block_breadcrumb, 0x100)
                    p2_startup_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p2_startup_block_breadcrumb, 0x100)

                    p1_movement_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p1_movement_block_breadcrumb, 0x100)
                    p2_movement_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p2_movement_block_breadcrumb, 0x100)

                    p1_timer_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p1_timer_block_breadcrumb, 0x200)
                    p2_timer_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p2_timer_block_breadcrumb, 0x200)


                    p1_last_attack_address = GetValueFromAddress(process_handle, AddressMap.p1_last_attack_address)
                    p1_total_animation_frames = GetValueFromAddress(process_handle, AddressMap.p1_total_animation_frames, isFloat=True)
                    p1_end_of_move_cancelable_frames = GetValueFromAddress(process_handle, AddressMap.p1_end_of_move_cancelable_frames, is_short =True)
                    p1_is_currently_jumping = GetValueFromAddress(process_handle, AddressMap.p1_is_currently_jumping_address, is_short =True)
                    p1_is_currently_crouching = GetValueFromAddress(process_handle, AddressMap.p1_is_currently_crouching_address, is_short=True)
                    p1_is_currently_guard_impacting = GetValueFromAddress(process_handle, AddressMap.p1_is_currently_guard_impacting, is_short=True)
                    p1_is_currently_armoring = GetValueFromAddress(process_handle, AddressMap.p1_is_currently_armoring, is_short=True)

                    p1_global = SC6GlobalBlock(p1_last_attack_address, p1_total_animation_frames, p1_end_of_move_cancelable_frames, p1_is_currently_jumping, p1_is_currently_crouching, p1_is_currently_guard_impacting, p1_is_currently_armoring)


                    p2_last_attack_address = GetValueFromAddress(process_handle, AddressMap.p2_last_attack_address)
                    p2_total_animation_frames = GetValueFromAddress(process_handle, AddressMap.p2_total_animation_frames, isFloat=True)
                    p2_end_of_move_cancelable_frames = GetValueFromAddress(process_handle, AddressMap.p2_end_of_move_cancelable_frames, is_short=True)
                    p2_is_currently_jumping = GetValueFromAddress(process_handle, AddressMap.p2_is_currently_jumping_address, is_short=True)
                    p2_is_currently_crouching = GetValueFromAddress(process_handle, AddressMap.p2_is_currently_crouching_address, is_short=True)
                    p2_is_currently_guard_impacting = GetValueFromAddress(process_handle, AddressMap.p2_is_currently_guard_impacting, is_short=True)
                    p2_is_currently_armoring = GetValueFromAddress(process_handle, AddressMap.p2_is_currently_armoring, is_short=True)
                    p2_global = SC6GlobalBlock(p2_last_attack_address, p2_total_animation_frames, p2_end_of_move_cancelable_frames, p2_is_currently_jumping, p2_is_currently_crouching, p2_is_currently_guard_impacting, p2_is_currently_armoring)

                    value_p1 = PlayerSnapshot(p1_startup_block, p1_movement_block, p1_timer_block, p1_global)
                    value_p2 = PlayerSnapshot(p2_startup_block, p2_movement_block, p2_timer_block, p2_global)



                    if (len(self.snapshots) == 0) or (value_p1.movement_block.short_timer != self.snapshots[-1].p1.movement_block.short_timer):
                        self.snapshots.append(GameSnapshot(value_p1, value_p2))
                        return True
                    else:
                        return False


class SC6MovementBlock:
    def __init__(self, data_block):
        self.movement_type = GetValueFromDataBlock(data_block, 0x04)
        try:
            self.movement_type = GameplayEnums.MoveState(self.movement_type)
        except Exception as e:
            pass
            # print(e)
        self.short_timer = GetValueFromDataBlock(data_block, 0x08)
        self.float_timer = GetValueFromDataBlock(data_block, 0x0C, is_float=True)
        #0x10 is another timer that only resets on movement/guard?
        #0x14 seems to be a very few frame flag that trips on move ending and running?
        #0x18 is mostly 0x01 but changes briefly to 0x02 during extended 8way run movement
        #0x0C is 0 or 1, trips on attacks and movement
        #0x20 0 most of the time goes to 1 during throws, supers, and reversal edge (animation locks?)
        #0x24 is another timer (float)
        #0x28 is (probably) a float. mostly 1.00 but goes between .5 and 1.5 for a few frames sometimes, 8 way run can trip this for longer
        #0x2C mirror of above?
        #0x30 attacks set this to 1, movement or guarding sets it to 0, guarding an attack sets it to 1
        #0x34 changes from default value only very briefly (active frames???)
        #0x38 trips on the end of moves and movement, somewhat brief, flags? address? doesn't seem to be a number
        #0x4C mostly 0 but vvvvvery ocassionaly trips (???)
        #0x50 mostly constant, but sometimes flips 3rd byte (time based? every x input based?)
        #next 24 bytes mostly constant?
        #0x68 on hit or block seems to be a damage... correlated? number (float)
        #0x6C timer, int, seems to be a bit less prone to resetting than the others, gets up to bigger values
        #12 bytes of constant?
        self.movelist_id = GetValueFromDataBlock(data_block, 0x6C, is_short=True)#0x6C animation id (65535 in nuetral)
        self.move_counter = GetValueFromDataBlock(data_block, 0x70, is_short=True)  # counts the number of frames in a move
        #0x78 countup move timer, stops and stays at end if you don't do anything else
        #0x7C A float version of the above
        #0x80 the number the move timers are counting up to (number of animation frames?) (float)
        #0x84 float or flag? gets set to 1.0 when hit or guarding, some movement or attacks can set this to 0-155, mostly 0
        #0x88 two(?) flags, 0 or 1, flips on attacks, idle, but not consistently
        #0x8C another flag that's 0 or 1 with mystery flip conditions
        #0x90 another count up timer (float)
        #0x94 and 0x98 same constant? floating point 1
        #0x98 another mystery flip 0 or 1
        #0x9C constant?
        #0xA0 mystery

    def __repr__(self):
        repr = "movement: {} | short_timer: {} | float_timer: {} | animation_id: {} | move_counter: {}".format(
            self.movement_type, self.short_timer, self.float_timer, self.movelist_id, self.move_counter
        )
        return repr

class SC6StartupBlock:
    def __init__(self, data_block):

        #self.player_health = GetValueFromDataBlock(data_block, 0x16, is_float=True) #starts at 240.00 and decreases
        #0x38 is some kind move property address, but not an actual address, could also be flags?
        self.attack_type = GetValueFromDataBlock(data_block, 0x40, is_byte=True)
        try:
            self.attack_type = GameplayEnums.HitLevel(self.attack_type).name
        except Exception as e:
            pass
            # print(e)

        self.startup_frames = GetValueFromDataBlock(data_block, 0x44, is_short=True) #1 less than the common terminology
        #self.end_of_active_frames = GetValueFromDataBlock(data_block, 0x46, is_short=True) #usually only 1 or 2 higher than startup frames #??? this is, something else
        self.damage = GetValueFromDataBlock(data_block, 0x48, is_short=True)
        #0x4A is a constant, though different for p1 and p2 same character (01 22 vs 01 BB)
        #0x4C 4 byte constant? 01 D1 vs 01 D9
        #0x50 is 0, 1, or 0x20 seemingly at random for a move?
        #0x52 again only a few specific values
        #0x54-58 more specific values
        #0x5A constant, almost but not quite FFFF (FD FF) -3 perhaps?
        #0x5C 00 mostly, except for A+B guard break? 1 byte only (or second byte is always 2e?)
        #0x5E multiple of 10 or 5?
        #0x60 0 or multiple of 5, can be negative
        #0x62 0 mostly, -80 on super/some guard breaks (not all), and -70 on tira's kick into air
        #0x64 multiple of 5 (mostly of 10)
        #0x66 multiple of 5
        #0x68 multiple of 5 (negative?)
        #0x6A multiple of 5
        #0x6C multiple of 5, although might've gotten 76


        self.hit_stun = GetValueFromDataBlock(data_block, 0x7C, is_short=True)
        self.counterhit_stun = GetValueFromDataBlock(data_block, 0x7E, is_short=True)
        self.block_stun = GetValueFromDataBlock(data_block, 0x80, is_short=True)
        self.hit_launch = GetValueFromDataBlock(data_block, 0x82, is_short=True)
        self.counter_launch = GetValueFromDataBlock(data_block, 0x84, is_short=True)
        try:
            #self.hit_launch = GameplayEnums.HitEffect(self.hit_launch)
            self.hit_launch = GameplayEnums.HitEffectToLaunchType(self.hit_launch).name

        except Exception as e:
            #print(e)
            self.hit_launch = hex(self.hit_launch)

        try:
            #self.counter_launch = GameplayEnums.HitEffect(self.counter_launch)
            self.counter_launch = GameplayEnums.HitEffectToLaunchType(self.counter_launch).name
        except Exception as e:
            self.counter_launch = hex(self.counter_launch)




        self.has_counterhit_properties = (self.hit_launch != self.counter_launch) or (self.hit_stun != self.counterhit_stun)



        self.guard_damage = GetValueFromDataBlock(data_block, 0xA8, is_short=True)

    def __repr__(self):
        repr = "attack_type: {} | startup: {} | dam: {} | hit_stun: {} | counter_stun: {} | block_stun: {} | launch_hit: {} | launch_counter: {} | guard_damage: {}".format(
            self.attack_type, self.startup_frames, self.damage, self.hit_stun, self.counterhit_stun, self.block_stun, self.hit_launch, self.counter_launch, self.guard_damage
        )

        return repr


class SC6GlobalBlock:
    def __init__(self, last_attack_address, total_animation_frames, end_of_move_cancelable_frames, is_currently_jumping, is_currently_crouching, is_currently_guard_impacting, is_currently_armoring):
        self.last_attack_address = last_attack_address
        self.total_animation_frames = int(total_animation_frames)
        self.end_of_move_cancelable_frames = end_of_move_cancelable_frames
        self.is_currently_jumping = is_currently_jumping
        self.is_currently_crouching = is_currently_crouching
        self.is_currently_guard_impacting = is_currently_guard_impacting
        self.is_currently_armoring = is_currently_armoring

    def __repr__(self):
        repr = "attack_address: {} | total_uncanceled_frames: {} | frames_move_can_be_canceled_early: {} | TJ: {} | TC: {} | GI: {} | REV: {}".format(
            hex(self.last_attack_address), self.total_animation_frames, self.end_of_move_cancelable_frames, self.is_currently_jumping, self.is_currently_crouching, self.is_currently_guard_impacting, self.is_currently_armoring)
        return repr


class SC6TimerBlock:
    def __init__(self, data_block):
        self.move_id = GetValueFromDataBlock(data_block, 0x74, is_short=True)

    def __repr__(self):
        return "move_id: {}".format(self.move_id)

class PlayerSnapshot:
    def __init__(self, startup_data_block, movement_data_block, timer_data_block, global_block : SC6GlobalBlock):
        self.movement_block = SC6MovementBlock(movement_data_block)
        self.startup_block = SC6StartupBlock(startup_data_block)
        self.timer_block = SC6TimerBlock(timer_data_block)
        self.global_block = global_block

    def __repr__(self):
        return "{} | {} | {} | {}".format(self.timer_block, self.startup_block, self.global_block, self.movement_block)


class GameSnapshot:
    def __init__(self, p1_snapshot : PlayerSnapshot, p2_snapshot : PlayerSnapshot):
        self.p1 = p1_snapshot
        self.p2 = p2_snapshot

    def __repr__(self):
        return "{} ||| {}".format(self.p1, self.p2)


if __name__ == "__main__":
    import time
    import GameplayEnums
    myReader = SC6GameReader()
    old_state = None
    while True:
        successful_update = myReader.UpdateCurrentSnapshot()

        if successful_update:
            new_state = myReader.snapshots[-1]
            if old_state == None:
                old_state = new_state

            if new_state.p1.movement_block.short_timer != old_state.p1.movement_block.short_timer:
                old_state = new_state
                print(new_state)
                if myReader.p1_movelist != None:
                    myReader.p1_movelist.print_cancel_bytes_by_move_id(new_state.p1.movement_block.movelist_id)


            #if v1.movement_block.movement_type != ov1.movement_block.movement_type or v2.movement_block.movement_type != ov2.movement_block.movement_type:
                #ov1, ov2 = v1, v2
                #print('{}, {} ({}, {})'.format(v1.movement_block.movement_type, v2.movement_block.movement_type, v1.startup_block.startup_frames, v2.startup_block.startup_frames))
            #print('t')
        time.sleep(.005)

