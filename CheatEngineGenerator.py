from AddressMap import *
import SoulCaliburGameState

if __name__ == "__main__":
    CHEAT_ENGINE_BLOCK = '<CheatEntry> <ID>{id}</ID> <Description>"{name}"</Description> <VariableType>{variable_type}</VariableType> <Address>"SoulcaliburVI.exe"+{base_address}</Address> <Offsets> {offsets} </Offsets> </CheatEntry>'
    GENERIC_OFFSET_BLOCK = "<Offset>{offset}</Offset>"

    CHEAT_ENGINE_HEADER = '<?xml version="1.0" encoding="utf-8"?><CheatTable CheatEngineTableVersion="26"><CheatEntries>'
    CHEAT_ENGINE_FOOTER = '</CheatEntries><UserdefinedSymbols/><Comments>Info about this table:</Comments></CheatTable>'


    def PrintCheatEngineBlock(id, name, base_address, offset_list, data_is_float=False, bytes = 4):
        if data_is_float:
            variable_type = 'Float'
        else:
            variable_type = '{} Bytes'.format(bytes)

        offset_string = ""
        for offset in offset_list:
            offset_string = GENERIC_OFFSET_BLOCK.replace('{offset}', format(offset, 'x')) + offset_string
        print(CHEAT_ENGINE_BLOCK.replace('{id}', str(id)).replace('{name}', name).replace('{variable_type}', variable_type).replace('{base_address}', format(base_address, 'x')).replace('{offsets}', offset_string))



    address_map = [
        (global_timer_address, '_global_timer', 4, []),
        (p1_input_address, 'p1_input', 2, []),
        (p2_input_address, 'p2_input', 2, []),

        (p1_movelist_address, 'p1_movelist_address', 2, []),
        (p2_movelist_address, 'p2_movelist_address', 2, []),

        (p1_move_id_address, 'p1_move_id_address', 2, []),
        (p2_move_id_address, 'p2_move_id_address', 2, []),

        (p1_guard_damage_address, 'p1_guard_damage_address', 2, []),
        (p2_guard_damage_address, 'p2_guard_damage_address', 2, []),

        (p1_startup_block_breadcrumb[0], 'p1_startup_block', 4, p1_startup_block_breadcrumb[1:]),
        (p2_startup_block_breadcrumb[0], 'p2_startup_block', 4, p2_startup_block_breadcrumb[1:]),

        (p1_movement_block_breadcrumb[0], 'p1_movement_block', 4, p1_movement_block_breadcrumb[1:]),
        (p2_movement_block_breadcrumb[0], 'p2_movement_block', 4, p2_movement_block_breadcrumb[1:]),

        (p1_movement_block_breadcrumb[0], 'p1_movelist_id', 2, p1_movement_block_breadcrumb[1:] + [0x6c]),
        (p2_movement_block_breadcrumb[0], 'p2_movelist_id', 2, p2_movement_block_breadcrumb[1:] + [0x6c]),

        (p1_movement_block_breadcrumb[0], 'p1_movement_block_counter', 2, p1_movement_block_breadcrumb[1:] + [0x70]),
        (p2_movement_block_breadcrumb[0], 'p2_movement_block_counter', 2, p2_movement_block_breadcrumb[1:] + [0x70]),

        (p1_timer_block_breadcrumb[0], 'p1_timer_block', 4, p1_timer_block_breadcrumb[1:]),
        (p2_timer_block_breadcrumb[0], 'p2_timer_block', 4, p2_timer_block_breadcrumb[1:]),

        (p1_timer_block_breadcrumb[0], 'p1_timer_block_move_id', 4, p1_timer_block_breadcrumb[1:] + [0x74]),
        (p2_timer_block_breadcrumb[0], 'p2_timer_block_move_id', 4, p2_timer_block_breadcrumb[1:] + [0x74]),
    ]

    print(CHEAT_ENGINE_HEADER)
    id = 999
    for base, name, bytes, offsets in address_map:
        id += 1
        PrintCheatEngineBlock(id, name, base, offsets, bytes=bytes)
    print(CHEAT_ENGINE_FOOTER)