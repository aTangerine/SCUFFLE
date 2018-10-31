

offset_module = 0x03EC14D0 #The first value on the cheat engine pointers
offset_players_pointer_A = 0x08
offset_players_pointer_B = 0x520
offset_player_1_object = 0x390
offset_player_2_object = 0x3A0
offset_movement_type_block = 0x160
offset_timer_block = 0x110

test_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B]

p1_movement_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_1_object, offset_movement_type_block]#xianghua's aab is 257/259/262
p2_movement_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_2_object, offset_movement_type_block]

p1_startup_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_1_object] #xianghua's AAB is 10/16/25
p2_startup_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_2_object]

p1_timer_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_1_object, offset_timer_block]#xianghua's AAB is 123/65/433
p2_timer_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_2_object, offset_timer_block]

p1_end_of_move_cancelable_frames = 0x14455B3D0 #for tira AA is 11/12, this is 0 when no move is active #for xianghua's AAB it's 5/6/4
p2_end_of_move_cancelable_frames = 0x14455B5B0

p1_total_animation_frames = 0x1445A7D80 #for Tira AA is 52/56, remember this is a FLOAT #for xianghua's aab 46/55/62
p2_total_animation_frames = 0x14463EA90

p1_last_attack_address = 0x1445A7460 #for Tira A is 0x3730, K is 0x5aa0 and A+B is 0x62f0, search for the increase/decrease from one to the next #xianghua's AAB is 0x42b8/0x4408/0x45c8
p2_last_attack_address = 0x14463E170

p1_is_currently_jumping_address = 0x1445F8B84 # 4 bytes 01 00 00 00 when jumping, 00 when not
p1_is_currently_crouching_address = 0x1445F8B88 # same as above but for crouching, can probably search for both together with 8 byte array

p2_is_currently_jumping_address = 0x14468F894
p2_is_currently_crouching_address = 0x14468F898

p1_is_currently_guard_impacting = 0x144563E40 # 8 byte boolean, 1 when guard impacting, 0 the rest of the time; use ivy's super or xianghua's b+k spinny one for enough frames to pause reliably
p2_is_currently_guard_impacting = 0x1445FAB50

p1_is_currently_armoring = 0x1445652DC #8 byte boole, 1 when armoring, else 0; use nightmare super or 6A or 6K
p2_is_currently_armoring = 0x1445FBFEC