# ParkAlert Vision System

The ParkAlert Vision System is a sophisticated application designed to detect and classify vehicles in parking lots using real-time video streams. It leverages advanced computer vision techniques and the YOLO (You Only Look Once) model for efficient object detection.

## Features

- Real-time vehicle detection and classification.
- Parking spot management with drawing and undo capabilities.
- Integration with RTSP and HLS video streams.
- Visual overview of detected vehicles.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.6 or higher
- Virtual environment (recommended)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jackrvu/parkalert.git
   cd parkalert/vision
   ```

2. **Set Up a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **YOLO Model Files:**

   Ensure you have the YOLO model files (`yolov8x.pt`) in the working directory. You can download them from the [Ultralytics YOLO repository](https://github.com/ultralytics/yolov5).

2. **Video Stream URL:**

   Update the `hls_url` variable in `main.py` with your RTSP or HLS stream URL:

   ```python
   hls_url = "http://localhost:8888/test/stream.m3u8"
   ```

## Usage

1. **Run the Application:**

   Start the application by executing:

   ```bash
   python main.py
   ```

2. **Drawing Parking Spots:**

   - Click on the video window to draw parking spots by selecting four points for each spot.
   - Press 's' to save the spots, 'u' to undo the last spot, and 'q' to quit the drawing mode.

3. **Vehicle Detection:**

   - The application will automatically detect and classify vehicles in the video stream.
   - Detected vehicles and their positions will be displayed in the overview window.

4. **Exiting the Application:**

   - Press 'q' in the main window to exit the application.

## Troubleshooting

- Ensure the video stream URL is correct and accessible.
- Verify that all dependencies are installed correctly.
- Check for any network issues that might affect video stream access.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License
This software is proprietary and confidential. Unauthorized copying, distribution, modification, public display, or public performance of this software, or any portion thereof, is strictly prohibited. All rights reserved.

This software is owned by and constitutes valuable intellectual property of the company. No license, express or implied, to any intellectual property rights is granted by this document.

Copyright © 2024. All Rights Reserved.


## Functioning Docker commands
docker run -d --name=wyze-bridge -p 8554:8554 -p 8888:8888 -p 5000:5000 -e 'WYZE_EMAIL=mavjvu2@gmail.com' -e 'WYZE_PASSWORD=YourCorrectPasswordHere' -e 'API_ID=cde19a40-c81c-47da-9b4c-370bc82e9fbc' -e 'API_KEY=XYzr7Hs1YylalXJ47k7xwGk8hN9JvsT7w46CWeG5shHoP6KjigZypYSiCcXa' -e 'WB_AUTH=false' -e 'RTSP_FW_ENABLED=true' mrlt8/wyze-bridge:latest

docker stop wyze-bridge
docker rm wyze-bridge