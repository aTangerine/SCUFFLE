import SoulCaliburGameState
import time
import GameplayEnums

class GameStateManager:
    def __init__(self):
        self.game_reader = SoulCaliburGameState.SC6GameReader()
        self.last_move = 0

    def Update(self):
        successful_update = self.game_reader.UpdateCurrentSnapshot()
        if successful_update:
            snapshots = self.game_reader.snapshots
            if len(snapshots) > 2:
                did_p1_attack_change = snapshots[-1].p1.global_block.last_attack_address != snapshots[-2].p1.global_block.last_attack_address
                if (did_p1_attack_change):
                    print(GameStateManager.FormatFrameString('p1', self.game_reader.snapshots[-1].p1))

                did_p2_attack_change = snapshots[-1].p2.global_block.last_attack_address != snapshots[-2].p2.global_block.last_attack_address
                if (did_p2_attack_change):
                    print(GameStateManager.FormatFrameString('p2', self.game_reader.snapshots[-1].p2))

    def FormatFrameString(p_str, p : SoulCaliburGameState.PlayerSnapshot):
        b_h_c = FrameAnalyzer.CalculateFrameAdvantage(p)
        return "FDO:{}:{:^4}|{:^4}|{:^4}|{:^7}|{:^7}|{:^7}|{:^4}|{:^4}|".format(
                                                        p_str,
                                                        p.timer_block.move_id,
                                                        p.startup_block.startup_frames + 1,
                                                        p.startup_block.attack_type,
                                                        b_h_c[0],
                                                        b_h_c[1],
                                                        b_h_c[2],
                                                        p.startup_block.damage,
                                                        p.startup_block.guard_damage
                                                      )


class FrameAnalyzer:
    def CalculateFrameAdvantage(p : SoulCaliburGameState.PlayerSnapshot):
        total = p.global_block.total_animation_frames
        cancelable = p.global_block.end_of_move_cancelable_frames
        startup = p.startup_block.startup_frames
        block_stun = p.startup_block.block_stun
        hit_stun = p.startup_block.hit_stun
        counter_stun = p.startup_block.counterhit_stun
        recovery = total - cancelable

        on_block = recovery - (startup + block_stun)
        on_hit = recovery - (startup + hit_stun)
        on_counter = recovery - (startup + counter_stun)

        b, h, c = FrameAnalyzer.StringifyAdvantage(on_block), FrameAnalyzer.StringifyAdvantage(on_hit), FrameAnalyzer.StringifyAdvantage(on_counter)
        if p.startup_block.hit_launch != GameplayEnums.LaunchType.none.name:
            h = '{} {}'.format(p.startup_block.hit_launch, h)
        if p.startup_block.counter_launch!= GameplayEnums.LaunchType.none.name:
            c = '{} {}'.format(p.startup_block.counter_launch, c)




        return b, h, c

    def StringifyAdvantage(f : int):
        flipped = f * -1
        if flipped >= 0:
            return '+{}'.format(flipped)
        else:
            return '{}'.format(flipped)



if __name__ == "__main__":
    launcher = GameStateManager()
    while(True):
        launcher.Update()
        time.sleep(.05)
