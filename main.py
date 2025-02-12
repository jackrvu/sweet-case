import cv2
import numpy as np

# Public RTSP Stream (Replace with your own if needed)
rtsp_url = "rtsp:/10.0.0.161:8554/mystream"

# Open the RTSP Stream
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print(f"❌ Error: Unable to open RTSP stream at {rtsp_url}")
    exit()

# Display Video
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("⚠️ Warning: Failed to grab frame. Exiting...")
        break

    # Convert frame to grayscale and apply Gaussian blur for better circle detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles using Hough Circle Transform (assuming golf balls appear as circles)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                               param1=50, param2=30, minRadius=10, maxRadius=50)

    # If circles are found, draw a bounding box and label them as "Golf Ball"
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Draw a rectangle around the detected circle
            cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)
            # Add a nametag identifier next to the bounding box
            cv2.putText(frame, "Golf Ball", (x - r, y - r - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the video with detection overlays
    cv2.imshow("RTSP Stream", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
