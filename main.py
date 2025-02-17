import cv2
from ultralytics import YOLO
import numpy as np
from pathlib import Path
import time
import json

# Global variables for parking spot drawing
drawing = False
current_spot = []
parking_spots = []
spot_number = 1
undo_history = []  # Track spot history for undo

def mouse_callback(event, x, y, flags, param):
    global drawing, current_spot, parking_spots, spot_number, undo_history
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_spot.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP and len(current_spot) == 4:
        drawing = False
        # Create a closed polygon
        new_spot = {
            'points': current_spot.copy(),
            'number': spot_number
        }
        parking_spots.append(new_spot)
        undo_history.append(new_spot)  # Add to undo history
        spot_number += 1
        current_spot = []

def draw_parking_spots(frame, spots, occupied_spots=set()):
    """
    Draws polygons for each parking spot. 
    Spots occupied are drawn in red; free spots in green.
    """
    for spot in spots:
        points = np.array(spot['points'])
        number = spot['number']
        
        # Draw spot in red if occupied, green if empty
        color = (0, 0, 255) if number in occupied_spots else (0, 255, 0)
        
        # Draw the polygon
        cv2.polylines(frame, [points.reshape((-1, 1, 2))], True, color, 2)
        
        # Calculate centroid for number placement
        centroid = np.mean(points, axis=0).astype(int)
        cv2.putText(frame, str(number), tuple(centroid),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

def point_in_polygon(point, polygon):
    """
    Ray casting algorithm for detecting if a point lies inside a polygon.
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    j = n - 1
    for i in range(n):
        if (((polygon[i][1] > y) != (polygon[j][1] > y)) and
            (x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) /
             (polygon[j][1] - polygon[i][1]) + polygon[i][0])):
            inside = not inside
        j = i
    
    return inside

# Replace with your RTSP or HLS URL
hls_url = "http://localhost:8888/test/stream.m3u8"
cap = cv2.VideoCapture(hls_url)

if not cap.isOpened():
    print("Error: Could not open stream.")
    exit()

# Check if parking spots file exists
spots_file = Path("parking_spots.json")
if spots_file.exists():
    with open(spots_file, 'r') as f:
        parking_spots = json.load(f)
    spot_number = max(spot['number'] for spot in parking_spots) + 1
else:
    # Create window for drawing parking spots
    cv2.namedWindow("Draw Parking Spots")
    cv2.setMouseCallback("Draw Parking Spots", mouse_callback)
    
    print("Draw parking spots by clicking 4 points for each spot.")
    print("Press 's' to save, 'u' to undo last spot, 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
            
        frame_copy = frame.copy()
        
        # Draw existing spots
        for spot in parking_spots:
            points = np.array(spot['points'])
            cv2.polylines(frame_copy, [points.reshape((-1, 1, 2))], True, (0, 255, 0), 2)
            centroid = np.mean(points, axis=0).astype(int)
            cv2.putText(frame_copy, str(spot['number']), tuple(centroid),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw current spot being created
        if len(current_spot) > 0:
            points = np.array(current_spot)
            cv2.polylines(frame_copy, [points.reshape((-1, 1, 2))], False, (255, 0, 0), 2)
        
        cv2.imshow("Draw Parking Spots", frame_copy)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            # Save spots to file
            with open(spots_file, 'w') as f:
                json.dump(parking_spots, f)
            break
        elif key == ord('u') and len(parking_spots) > 0:  # Undo last spot
            removed_spot = parking_spots.pop()
            spot_number = removed_spot['number']  # Revert spot number
            current_spot = []  # Clear current spot if any
        elif key == ord('q'):
            exit()
    
    cv2.destroyWindow("Draw Parking Spots")

# Load YOLO model
model = YOLO('yolov8x.pt')  # Using YOLOv8x for better accuracy
conf_threshold = 0.3  # Confidence threshold

# Create an overview window for the top-down map or summary
overview_height = 400
overview_width = 600
overview = np.zeros((overview_height, overview_width, 3), dtype=np.uint8)

last_detection_time = time.time()
detected_vehicles = []  # Persist detections across frames

# Initialize occupied_spots so it's always defined
occupied_spots = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    current_time = time.time()
    
    # Only run detection once per second
    if current_time - last_detection_time >= 1.0:
        # Clear the overview window each time we do a new detection pass
        overview.fill(0)

        results = model(frame, conf=conf_threshold)
        new_detected_vehicles = []
        
        # Temporarily track spots occupied on this detection cycle
        new_occupied_spots = set()

        # Process detection results
        for result in results:
            for box in result.boxes:
                coords = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = map(int, coords)
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]

                # Focus on car-like vehicles
                if label.lower() in ["car", "truck", "bus"]:
                    # Check which parking spot this vehicle might be in
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    
                    for spot in parking_spots:
                        if point_in_polygon((center_x, center_y), spot['points']):
                            new_occupied_spots.add(spot['number'])
                    
                    # Store vehicle info for overview
                    new_detected_vehicles.append({
                        'label': f"Car ({conf:.2f})",
                        'position': (center_x, center_y),
                        'confidence': conf,
                        'box': (x1, y1, x2, y2)
                    })

        # Update persistent detection list only if we found new detections
        if new_detected_vehicles:
            detected_vehicles = new_detected_vehicles

        # Update the global occupied_spots
        occupied_spots = new_occupied_spots

        last_detection_time = current_time

    # Draw parking spots (pass in occupied_spots)
    draw_parking_spots(frame, parking_spots, occupied_spots)

    # Draw bounding boxes for all stored detections
    for vehicle in detected_vehicles:
        x1, y1, x2, y2 = vehicle['box']
        conf = vehicle['confidence']
        label_text = vehicle['label']
        
        # Color for bounding box based on confidence
        box_color = (0, int(255 * conf), 0)  # Brighter green for higher confidence
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
        # Add background rectangle for text
        cv2.rectangle(frame, (x1, y1 - 30), (x1 + len(label_text) * 11, y1), box_color, -1)
        cv2.putText(frame, label_text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Update overview window with vehicle positions
    overview.fill(0)  # Optional: clear each frame; or remove if you only want to clear once per detection
    for i, vehicle in enumerate(detected_vehicles):
        scaled_x = int((vehicle['position'][0] / frame.shape[1]) * overview_width)
        scaled_y = int((vehicle['position'][1] / frame.shape[0]) * overview_height)
        
        cv2.circle(overview, (scaled_x, scaled_y), 5, (0, 255, 0), -1)
        cv2.putText(overview, f"{i+1}: {vehicle['label']}", 
                    (10, 20 + i*20), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (255, 255, 255), 1)

    # Add frame info
    cv2.putText(frame, "Press 'q' to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display windows
    cv2.imshow("Vehicle Detection and Classification", frame)
    cv2.imshow("Vehicle Overview", overview)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
