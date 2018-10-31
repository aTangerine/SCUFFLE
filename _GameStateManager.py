import SoulCaliburGameState
import time
import GameplayEnums
from typing import List

class GameStateManager:
    def __init__(self):
        self.game_reader = SoulCaliburGameState.SC6GameReader()
        self.last_move = 0
        self.p1_backfiller = FrameBackCounter(True)
        self.p2_backfiller = FrameBackCounter(False)

    def Update(self):
        successful_update = self.game_reader.UpdateCurrentSnapshot()
        if successful_update:
            snapshots = self.game_reader.snapshots
            self.p1_backfiller.update(snapshots)
            self.p2_backfiller.update(snapshots)
            if len(snapshots) > 4:
                did_p1_attack_change = snapshots[-3].p1.global_block.last_attack_address != snapshots[-4].p1.global_block.last_attack_address # we build in a slight delay so we don't trample the middile of the update or slower computers
                if (did_p1_attack_change):
                    b, h, c, t, s = GameStateManager.FormatFrameString('p1', self.game_reader.snapshots[-1].p1)
                    self.p1_backfiller.reset(t, 4, snapshots)
                    print(s)

                did_p2_attack_change = snapshots[-1].p2.global_block.last_attack_address != snapshots[-2].p2.global_block.last_attack_address
                if (did_p2_attack_change):
                    b, h, c, t, s = GameStateManager.FormatFrameString('p2', self.game_reader.snapshots[-1].p2)
                    self.p2_backfiller.reset(t, 4, snapshots)
                    print(s)

    def FormatFrameString(p_str, p : SoulCaliburGameState.PlayerSnapshot):
        b, h, c, t = FrameAnalyzer.CalculateFrameAdvantage(p)
        str = "FDO:{}:{:^4}|{:^4}|{:^4}|{:^7}|{:^7}|{:^7}|{:^4}|{:^4}|{:^4}|".format(
                                                        p_str,
                                                        p.timer_block.move_id,
                                                        p.startup_block.startup_frames + 1,
                                                        p.startup_block.attack_type,
                                                        b,
                                                        h,
                                                        c,
                                                        p.startup_block.damage,
                                                        p.startup_block.guard_damage,
                                                        t,
                                                      )

        return b, h, c, t, str


class FrameAnalyzer:
    def CalculateFrameAdvantage(p : SoulCaliburGameState.PlayerSnapshot):
        uncanceled_frames = p.global_block.total_animation_frames
        cancelable = p.global_block.end_of_move_cancelable_frames
        startup = p.startup_block.startup_frames
        block_stun = p.startup_block.block_stun
        hit_stun = p.startup_block.hit_stun
        counter_stun = p.startup_block.counterhit_stun
        total_frames = uncanceled_frames - cancelable

        on_block = total_frames - (startup + block_stun)
        on_hit = total_frames - (startup + hit_stun)
        on_counter = total_frames - (startup + counter_stun)

        b, h, c = FrameAnalyzer.StringifyAdvantage(on_block), FrameAnalyzer.StringifyAdvantage(on_hit), FrameAnalyzer.StringifyAdvantage(on_counter)
        if p.startup_block.hit_launch != GameplayEnums.LaunchType.none.name:
            h = '{} {}'.format(p.startup_block.hit_launch, h)
        if p.startup_block.counter_launch!= GameplayEnums.LaunchType.none.name:
            c = '{} {}'.format(p.startup_block.counter_launch, c)

        return b, h, c, total_frames

    def StringifyAdvantage(f : int):
        flipped = f * -1
        if flipped >= 0:
            return '+{}'.format(flipped)
        else:
            return '{}'.format(flipped)

class FrameBackCounter:
    def __init__(self, is_p1):
        self.is_p1 = is_p1
        self.total_frames = 0
        self.current_frame = 9999

    def reset(self, total, current_frame, snapshots : List[SoulCaliburGameState.GameSnapshot]):
        if self.current_frame < self.total_frames: #if we haven't printed any frames, we print them now
            self.retrospective(snapshots)
        self.total_frames = total
        self.current_frame = current_frame


    def update(self, snapshots : List[SoulCaliburGameState.GameSnapshot]):
        self.current_frame += 1
        if self.current_frame == self.total_frames:
            self.retrospective(snapshots)

    def retrospective(self, snapshots : List[SoulCaliburGameState.GameSnapshot]):
        if self.current_frame < len(snapshots):
            crouching = lambda s: s.global_block.is_currently_crouching
            TC = self.backfill_for_func('TC', crouching, snapshots)
            jumping = lambda s: s.global_block.is_currently_jumping
            TJ = self.backfill_for_func('TJ', jumping, snapshots)
            if self.is_p1:
                p = 'p1:'
            else:
                p = 'p2:'
            note_string = 'NOTE:{} {} {}'.format(p, TC, TJ)
            if len(note_string) > 10:
                print(note_string)

    def backfill_for_func(self, string, func, snapshots):
        old_string = string
        toggle = False

        for i in reversed(range(1, self.current_frame)):
            if self.is_p1:
                s = snapshots[-i].p1
            else:
                s = snapshots[-i].p2
            c = func(s)
            if not toggle and c:
                toggle = True
                string += '[{}-'.format(s.movement_block.move_counter)
            if toggle and not c:
                toggle = False
                string += '{}]'.format(s.movement_block.move_counter)
        if string != old_string:
            return string
        else:
            return ""


if __name__ == "__main__":
    launcher = GameStateManager()
    while(True):
        launcher.Update()
        time.sleep(.05)
