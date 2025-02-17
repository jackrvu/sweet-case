
import cv2
from ultralytics import YOLO
import numpy as np
from pathlib import Path

def classify_car_make_model(roi):
    # Basic car classification based on simple size/ratio heuristics
    height, width = roi.shape[:2]
    aspect_ratio = width / height
    area = width * height
    
    # Very basic classification rules based on typical car proportions
    if aspect_ratio > 2.0:
        return "Limousine"
    elif aspect_ratio > 1.6:
        return "Sedan"
    elif aspect_ratio > 1.3:
        if area > 40000:  # Large vehicle
            return "SUV"
        else:
            return "Compact Car"
    else:
        return "Van"

# Use RTSP stream URL from the README
hls_url = "http://localhost:8888/test/stream.m3u8"
cap = cv2.VideoCapture(hls_url)

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()

# Load YOLO model and ensure it's using the best weights for vehicle detection
model = YOLO('yolov8x.pt')  # Using YOLOv8x for better accuracy
conf_threshold = 0.3  # Higher confidence threshold for more reliable detections

# Create a blank overview window
overview_height = 400
overview_width = 600
overview = np.zeros((overview_height, overview_width, 3), dtype=np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Reset overview window for each frame
    overview.fill(0)

    # Run YOLO detection with higher confidence threshold
    results = model(frame, conf=conf_threshold)

    # Keep track of detected vehicles for overview
    detected_vehicles = []

    # Process detection results
    for result in results:
        for box in result.boxes:
            coords = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, coords)
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            # Focus specifically on car detections
            if label.lower() in ["car", "truck", "bus"]:
                # Ensure ROI is within frame boundaries
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
                
                if x2 > x1 and y2 > y1:  # Valid ROI check
                    roi = frame[y1:y2, x1:x2]
                    make_model = classify_car_make_model(roi)
                    label_text = f"{label}: {make_model} ({conf:.2f})"

                    # Store vehicle info for overview
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    detected_vehicles.append({
                        'label': label_text,
                        'position': (center_x, center_y),
                        'confidence': conf
                    })

                    # Color coding based on confidence
                    color = (0, int(255 * conf), 0)  # Brighter green for higher confidence
                    
                    # Draw bounding box and label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    # Add background rectangle for text
                    cv2.rectangle(frame, (x1, y1 - 30), (x1 + len(label_text) * 11, y1), color, -1)
                    cv2.putText(frame, label_text, (x1, y1 - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Update overview window
    for i, vehicle in enumerate(detected_vehicles):
        # Scale the position to fit overview window
        scaled_x = int((vehicle['position'][0] / frame.shape[1]) * overview_width)
        scaled_y = int((vehicle['position'][1] / frame.shape[0]) * overview_height)
        
        # Draw vehicle position
        cv2.circle(overview, (scaled_x, scaled_y), 5, (0, 255, 0), -1)
        
        # Add label
        cv2.putText(overview, f"{i+1}: {vehicle['label']}", 
                    (10, 20 + i*20), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (255, 255, 255), 1)

    # Add frame information
    cv2.putText(frame, "Press 'q' to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show both windows
    cv2.imshow("Vehicle Detection and Classification", frame)
    cv2.imshow("Vehicle Overview", overview)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
