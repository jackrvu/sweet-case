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
then run the program with python main.py

Found from testing: just use wyze-bridge w/ docker desktop to bring the video stream onto a local machine

(added vehicle make & model detection w/ bounding boxes, added an overview window to see vehicle summary)

to start the program:

docker run -d --name=wyze-bridge -p 8554:8554 -p 8888:8888 -p 5000:5000 -e 'WYZE_EMAIL=mavjvu2@gmail.com' -e 'WYZE_PASSWORD=YourCorrectPasswordHere' -e 'API_ID=cde19a40-c81c-47da-9b4c-370bc82e9fbc' -e 'API_KEY=XYzr7Hs1YylalXJ47k7xwGk8hN9JvsT7w46CWeG5shHoP6KjigZypYSiCcXa' -e 'WB_AUTH=false' -e 'RTSP_FW_ENABLED=true' mrlt8/wyze-bridge:latest

Is the command that actually works

Now, write full program to start detecting cars, etc
Start w/ the driveway, detecting which cars are present


yolov8x.pt is a good model, but too big, so not on repo. have to download