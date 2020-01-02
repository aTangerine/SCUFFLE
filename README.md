# SCUFFLE (Simple FSO Edition)
Soul Calibur 6 Live Frame Data Reader -- based on the useful parts of the popular Tekken Bot Prime, it shows you frame data while you're playing the game so you don't have to alt-tab to a wiki or a google doc or a paste bin or yell at your twitch chat or <character> discord. Some of the frame data is even correct.

This is the Simple FSO (Full Screen Overlay) Edition of SCUFFLE, which incorporates an abridged, simpler display of frame data on a full screen overlay - no need to use borderless.

![image](https://user-images.githubusercontent.com/44570288/47742019-b740ca00-dc49-11e8-8f68-938c418bbaa3.png)

# Usage

Download the latest release from https://github.com/rougelite/SCUFFLE/releases. Run the .exe at the same as Soul Calibur 6 (PC version only) and it will read the memory to display internal frame data. The frame data overlay should display at the top of the screen, works only in windowed or windowed borderless mode (NO FULLSCREEN).

# Technical

SCUFFLE uses python 3.5 and strives to use only Standard Library modules so it should run with any 64-bit python 3.5. 32-bit Python (the default if you use the installer) probably won't work.

To build the project, make sure you have python 3.5 and pyinstaller and run the the project_build.bat file.

# I want to know more!

Check out https://www.youtube.com/watch?v=GjB-MRonAFc or read [How the Movelist is Parsed](__HowTheMovelistBytesWork.md)

# Information about Full Screen Overlay
Extremely hacky, prints string output from SCUFFLE to `Data/read.txt` and then reads and prints it on the overlay.
Output is presently parsed to show only the input notation and its frames on block. 
Need to get this working in a basic manner first and then work to more elegantly integrate it into SCUFFLE. 
Current problems:
* Alt-tabs back to desktop the first time it registers an input but never again after

Have not tested the build process, currently use the following instructions to use:
1. Ensure that Python 3.5 is installed
2. Install required modules via pip
3. Using PowerShell as admin, run `python GUI_FrameDataOverlayFullScreen.py` from the folder you cloned to
4. Start SC6

## To do
* Reposition overlay
* Heading column for overlay
* Implement OH data display
* General code cleanup and better integration with existing SCUFFLE codebase