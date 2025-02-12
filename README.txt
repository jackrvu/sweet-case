to use this program:

* install the requirements:
pip install -r requirements.txt

accesses some rtsp feed, must set one up prior to use
to set up the rtsp feed, first start the mediamtx server (./mediamtx), then stream from the camera
w/ the ffmpeg command (ffmpeg -f v4l2 -i /dev/video0 -vcodec libx264 -preset ultrafast -f rtsp rtsp://localhost:8554/mystream)