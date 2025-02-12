to use this program:

* install the requirements:
pip install -r requirements.txt

accesses some rtsp feed, must set one up prior to use
to set up the rtsp feed, first start the mediamtx server (./mediamtx), then stream from the camera
w/ the ffmpeg command (ffmpeg -f v4l2 -i /dev/video0 -vcodec libx264 -preset ultrafast -f rtsp rtsp://localhost:8554/mystream)

The program simply relies on a having a working RTSP feed, so any other method to accomplish that works as well (at home, test using a vlc server)

how to:
sudo apt update
sudo apt install vlc

raspivid -o - -t 0 -w 1280 -h 720 -fps 30 | cvlc stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/stream}' --demux h264

^ bunch of parameters, streams to rtsp link rtsp://<raspberry_pi_ip>:8554/stream
