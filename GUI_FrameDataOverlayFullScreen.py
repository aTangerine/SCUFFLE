# needs classes etc
'''
https://pypi.org/project/game-overlay-sdk/
54470 is steam app id
the following code uses run_process rather than start_monitor method
command line is:
python examples\overlay_log_handler.py --exe_path "D:\Steam\steamapps\common\Shadow of the Tomb Raider Trial\SOTTR.exe" --steam_app_id 974630
https://github.com/Andrey1994/game_overlay_sdk
'''
import time
import game_overlay_sdk
import game_overlay_sdk.injector
import threading
import logging


logging.basicConfig (filename = 'test.log', level = logging.WARNING)

logger = logging.getLogger (__name__)
logger.setLevel (logging.INFO)
overlay_log_handler = game_overlay_sdk.injector.OvelrayLogHandler ()
formatter = logging.Formatter ('%(levelname)s:%(message)s')
overlay_log_handler.setFormatter (formatter)
logger.addHandler (overlay_log_handler)


class MessageThread (threading.Thread):

    def __init__ (self):
        super (MessageThread, self).__init__ ()
        self.need_quit = False

    def run (self):
        i = 0
        while not self.need_quit:
            logger.info ('Hi from python OverlayLogHandler %d' % i)
            i = i + 1
            time.sleep (1)


def main ():

    game_overlay_sdk.injector.enable_monitor_logger ()
    # arguments are process path, process args, app id
    game_overlay_sdk.injector.run_process ('C:\Program Files (x86)\Steam\steamapps\common\SoulcaliburVI\SoulcaliburVI\Binaries\Win64\SoulcaliburVI.exe', '', '544750')

    # start sending messages to overlay
    thread = MessageThread ()
    thread.start ()
    input ("Press Enter to stop...")
    thread.need_quit = True
    thread.join ()

    game_overlay_sdk.injector.release_resources ()


if __name__ == "__main__":
    main ()