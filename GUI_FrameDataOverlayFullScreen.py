# needs classes etc
# must run as admin
'''
https://pypi.org/project/game-overlay-sdk/
54470 is steam app id
the following code uses start_monitor rather than run_process method
command line is:
python examples\monitor.py --name SOTTR.exe
https://github.com/Andrey1994/game_overlay_sdk
'''
import time
import game_overlay_sdk
import game_overlay_sdk.injector
import threading
import logging


# create the file in the directory that (game_overlay_sdk) requires this:
path = 'C:\Program Files (x86)\Steam\steamapps\common\SoulcaliburVI'
with open('%s\steam_appid.txt' % path, 'w') as appid_file:
    appid_file.write('544750')

class MessageThread (threading.Thread):

    def __init__ (self):
        super (MessageThread, self).__init__ ()
        self.need_quit = False

    def run (self): # need to restrict length of file or something
        i = 0
        while not self.need_quit:
            with open('Data/read.txt', 'r') as read_file:
                last_line = read_file.read().splitlines()[-1]
                # last_line = read_file.readlines(1000)[-1]
            try:
                '''
                game_overlay_sdk.injector.send_message ('Hi from python %d' % i)
                i = i + 1
                time.sleep (1)
                '''
                game_overlay_sdk.injector.send_message (str(last_line))
                i += 1
            except game_overlay_sdk.injector.InjectionError as err:
                if err.exit_code == game_overlay_sdk.injector.CustomExitCodes.TARGET_PROCESS_IS_NOT_CREATED_ERROR.value:
                    logging.warning ('target process is not created')
                    time.sleep (5)
                elif err.exit_code == game_overlay_sdk.injector.CustomExitCodes.TARGET_PROCESS_WAS_TERMINATED_ERROR.value:
                    logging.warning ('target process was stopped')
                    # in monitor mode we can run process several times so dont need to stop this thread here
                    i = 0
                    time.sleep (5)
                else:
                    raise err
            time.sleep(0.01666)


def main ():
    logging.basicConfig (level = logging.DEBUG)

    game_overlay_sdk.injector.enable_monitor_logger ()
    game_overlay_sdk.injector.start_monitor ('SoulcaliburVI.exe')

    # start sending messages to overlay
    thread = MessageThread ()
    thread.start ()
    input ("Press Enter to stop...")
    thread.need_quit = True
    thread.join ()

    game_overlay_sdk.injector.release_resources ()


if __name__ == "__main__":
    main ()