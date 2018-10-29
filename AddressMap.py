

offset_module = 0x03EC14D0 #The first value on the cheat engine pointers
offset_players_pointer_A = 0x08
offset_players_pointer_B = 0x520
offset_player_1_object = 0x390
offset_player_2_object = 0x3A0
offset_movement_type_block = 0x160
offset_timer_block = 0x110

test_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B]

p1_movement_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_1_object, offset_movement_type_block]
p2_movement_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_2_object, offset_movement_type_block]

p1_startup_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_1_object]
p2_startup_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_2_object]

p1_timer_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_1_object, offset_timer_block]
p2_timer_block_breadcrumb = [offset_module, offset_players_pointer_A, offset_players_pointer_B, offset_player_2_object, offset_timer_block]

p1_end_of_move_cancelable_frames = 0x14455B390 #for tira AA is 11/12, this is 0 when no move is active
p2_end_of_move_cancelable_frames = 0x14455B570

p1_total_animation_frames = 0x1445A7D40 #for Tira AA is 52/56, remember this is a FLOAT
p2_total_animation_frames = 0x14463EA50

p1_last_attack_address = 0x1445A7420 #for Tira A is 0x3730, K is 0x5aa0 and A+B is 0x62f0, search for the offsets from one to the next
p2_last_attack_address = 0x14463E130