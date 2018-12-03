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
            self.timer = 0

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
                        movelist_sample = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, [AddressMap.p1_movelist_address], 0x4)
                        movelist_sample = GetValueFromDataBlock(movelist_sample, 0)

                        if  movelist_sample == MovelistParser.Movelist.STARTER_INT:
                            p1_movelist_data = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, [AddressMap.p1_movelist_address], AddressMap.MOVELIST_BYTES)
                            p2_movelist_data = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, [AddressMap.p2_movelist_address], AddressMap.MOVELIST_BYTES)
                            self.p1_movelist = MovelistParser.Movelist(p1_movelist_data, 'p1')
                            self.p2_movelist = MovelistParser.Movelist(p2_movelist_data, 'p2')
                        else:
                            return False

                    new_timer = GetValueFromAddress(process_handle, self.module_address + AddressMap.global_timer_address)

                    if self.timer == new_timer:
                        return False
                    else:
                        self.timer = new_timer


                    #p1_startup_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p1_startup_block_breadcrumb, 0x100)
                    #p2_startup_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p2_startup_block_breadcrumb, 0x100)

                    #p1_movement_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p1_movement_block_breadcrumb, 0x100)
                    #p2_movement_block = GetDataBlockAtEndOfPointerOffsetList(process_handle, self.module_address, AddressMap.p2_movement_block_breadcrumb, 0x100)

                    p1_move_id = GetValueFromAddress(process_handle, self.module_address + AddressMap.p1_move_id_address, is_short =True)
                    p2_move_id = GetValueFromAddress(process_handle, self.module_address + AddressMap.p2_move_id_address, is_short=True)

                    p1_gdam = GetValueFromAddress(process_handle, self.module_address + AddressMap.p1_guard_damage_address, is_short=True)
                    p2_gdam = GetValueFromAddress(process_handle, self.module_address + AddressMap.p2_guard_damage_address, is_short=True)

                    p1_input = GetValueFromAddress(process_handle, self.module_address + AddressMap.p1_input_address, is_short =True)
                    p1_global = SC6GlobalBlock(p1_input)

                    p2_input = GetValueFromAddress(process_handle, self.module_address + AddressMap.p2_input_address, is_short=True)
                    p2_global = SC6GlobalBlock(p2_input)

                    value_p1 = PlayerSnapshot(self.p1_movelist, p1_gdam, p1_move_id, p1_global)
                    value_p2 = PlayerSnapshot(self.p2_movelist, p2_gdam, p2_move_id, p2_global)



                    #if (len(self.snapshots) == 0) or (value_p1.movement_block.short_timer != self.snapshots[-1].p1.movement_block.short_timer):
                    self.snapshots.append(GameSnapshot(value_p1, value_p2, self.timer))
                    MAX_FRAMES_TO_KEEP = 1000
                    if len(self.snapshots) > MAX_FRAMES_TO_KEEP:
                        self.snapshots = self.snapshots[MAX_FRAMES_TO_KEEP // 2: -1]
                    return True



class SC6MovementBlock:
    def __init__(self, move_id):
        self.movelist_id = move_id

class SC6StartupBlock:
    def __init__(self, gdam):
        self.guard_damage = gdam

class SC6GlobalBlock:
    def __init__(self, input_short):
        left_bytes = (input_short & 0xFF00) >> 8
        right_bytes = input_short & 0x00FF

        self.input_code_button = right_bytes
        self.input_code_direction = left_bytes

    def __repr__(self):
        repr = "{} | {} |".format(
            self.input_code_button, self.input_code_direction)
        return repr

class PlayerSnapshot:
    def __init__(self, movelist, gdam, move_id, global_block : SC6GlobalBlock):
        self.movelist = movelist
        self.movement_block = SC6MovementBlock(move_id)
        self.startup_block = SC6StartupBlock(gdam)
        self.global_block = global_block

class GameSnapshot:
    def __init__(self, p1_snapshot : PlayerSnapshot, p2_snapshot : PlayerSnapshot, timer):
        self.timer = timer
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
                    pass
                    #myReader.p1_movelist.print_cancel_bytes_by_move_id(new_state.p1.movement_block.movelist_id)
                    #print(myReader.p1_movelist.parse_move(new_state.p1.movement_block.movelist_id))
                    #print(myReader.p1_movelist.get_command_by_move_id(new_state.p1.movement_block.movelist_id))




            #if v1.movement_block.movement_type != ov1.movement_block.movement_type or v2.movement_block.movement_type != ov2.movement_block.movement_type:
                #ov1, ov2 = v1, v2
                #print('{}, {} ({}, {})'.format(v1.movement_block.movement_type, v2.movement_block.movement_type, v1.startup_block.startup_frames, v2.startup_block.startup_frames))
            #print('t')
        time.sleep(.005)

