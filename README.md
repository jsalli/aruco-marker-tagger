# Aruco marker tagger for video stream
This repo tags Aruco markers with text and box under the text.

See the params.yaml and edit colors, text and other values for each Aruco marker

<img src="tagged-aruco-markers.png" alt="drawing" width="500"/>

# Linux
## Requirements
The Aruco Tagger start script expects to run in a virtual python3 environment. To make sure it's available, run:

`sudo apt update`

`sudo apt install python3-venv`

## Install
`chmod +x install.sh`

`./install.sh`

## Start
`chmod +x start.sh`

`./start.sh`

Stop program by pressing CTRL and C simuntaniously in the opened terminal window.


# Windows
## Install
`install.bat`

## Start
`start.bat`

Stop program by pressing CTRL and C simuntaniously in the opened terminal window.


# Testing with a local stream
## Windows

To test with a local webcam or e.g. [OBS VirtualCamera](https://github.com/CatxFish/obs-virtual-cam), you can stream the camera input via [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) to a localhost address, and then read the stream with cv2.VideoCapture.
(_These instructions are very much "works on my machine" and there are probably better ways to do this. -jkostet_)

Run this command with cmd.exe from the aruco-marker-tagger directory.

`"<PATH TO>\ffmpeg.exe" -f dshow -i video="<DEVICE NAME e.g. OBS-Camera" -f rtp rtp://localhost:8887 -sdp_file saved_sdp_file -f rtp rtp://localhost:8889`

_Note: some udp magic will happen in a port +1 larger than the first localhost:port in the command. The second port at the end of the command needs to be +2 larger (or something else), otherwise you'll get this error when running aruco_tagger.py:_

`[udp @ 0000015abcabc] bind failed: Error number -10048 occurred`

A stream to localhost:8887 will open, and an sdp file "saved_sdp_file" will be created in the directory. Set video_path in params.yaml as "saved_sdp_file".

Try running start.bat with another command line. You may run into another error:

`Protocol 'rtp' not on whitelist 'file,crypto'!`

I managed to get past this by setting an environment value with command (from cmd/powershell as admin):

`SETX "OPENCV_FFMPEG_CAPTURE_OPTIONS" "protocol_whitelist;file,rtp,udp"`

You can also try adding these to aruco_tagger.py (and running start.bat as admin):

```
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp"
# OR
os.system("SETX {0} {1} /M".format("OPENCV_FFMPEG_CAPTURE_OPTIONS", "protocol_whitelist;file,rtp,udp"))
```
