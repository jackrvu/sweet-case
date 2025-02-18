import cv2
from ultralytics import YOLO
import numpy as np
from pathlib import Path
import time
import json

# Global variables for drawing parking spots
drawing = False
current_spot = []
parking_spots = []
spot_number = 1
undo_history = []  # To track history for undo

def mouse_callback(event, x, y, flags, param):
    global drawing, current_spot, parking_spots, spot_number, undo_history
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_spot.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP and len(current_spot) == 4:
        drawing = False
        # Create a new spot and precompute its NumPy array & centroid
        new_spot = {
            'points': current_spot.copy(),
            'number': spot_number
        }
        parking_spots.append(new_spot)
        undo_history.append(new_spot)
        spot_number += 1
        current_spot.clear()

def update_precomputed_spots(spots):
    """
    For each parking spot, precompute the NumPy array and centroid.
    """
    for spot in spots:
        pts = np.array(spot['points'], dtype=np.int32)
        spot['np_points'] = pts.reshape((-1, 1, 2))
        spot['centroid'] = tuple(np.mean(pts, axis=0).astype(int))

def draw_parking_spots(frame, spots, occupied_spots=set()):
    """
    Draw each parking spot in green if free, or red if occupied.
    """
    for spot in spots:
        color = (0, 0, 255) if spot['number'] in occupied_spots else (0, 255, 0)
        pts = spot.get('np_points')
        if pts is None:
            pts = np.array(spot['points'], dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, color, 2)
        centroid = spot.get('centroid')
        if centroid is None:
            centroid = tuple(np.mean(np.array(spot['points']), axis=0).astype(int))
        cv2.putText(frame, str(spot['number']), centroid,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

def point_in_parking_spot(point, spot):
    """
    Uses OpenCV's pointPolygonTest (in C++) for fast hit-testing.
    """
    pts = spot.get('np_points')
    if pts is None:
        pts = np.array(spot['points'], dtype=np.int32).reshape((-1, 1, 2))
    # Returns >= 0 if the point is inside or on the edge
    return cv2.pointPolygonTest(pts, point, False) >= 0

def main():
    global parking_spots, spot_number, current_spot

    # Replace with your RTSP or HLS URL
    hls_url = "http://localhost:8888/test/stream.m3u8"
    cap = cv2.VideoCapture(hls_url)
    
    if not cap.isOpened():
        print("Error: Could not open stream.")
        return

    spots_file = Path("parking_spots.json")
    if spots_file.exists():
        with open(spots_file, 'r') as f:
            parking_spots = json.load(f)
        spot_number = max(spot['number'] for spot in parking_spots) + 1
        update_precomputed_spots(parking_spots)
    else:
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
                pts = np.array(spot['points'], dtype=np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame_copy, [pts], True, (0, 255, 0), 2)
                centroid = tuple(np.mean(np.array(spot['points']), axis=0).astype(int))
                cv2.putText(frame_copy, str(spot['number']), centroid,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw the current spot being drawn
            if current_spot:
                pts = np.array(current_spot, dtype=np.int32)
                cv2.polylines(frame_copy, [pts.reshape((-1, 1, 2))], False, (255, 0, 0), 2)
            
            cv2.imshow("Draw Parking Spots", frame_copy)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                with open(spots_file, 'w') as f:
                    json.dump(parking_spots, f)
                update_precomputed_spots(parking_spots)
                break
            elif key == ord('u') and parking_spots:
                parking_spots.pop()
                spot_number = parking_spots[-1]['number'] + 1 if parking_spots else 1
                current_spot.clear()
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return
        cv2.destroyWindow("Draw Parking Spots")
    
    # Load the YOLO model (using yolov8x for higher accuracy)
    model = YOLO('yolov8x.pt')
    conf_threshold = 0.3

    # Setup overview window dimensions
    overview_height, overview_width = 400, 600
    overview = np.zeros((overview_height, overview_width, 3), dtype=np.uint8)
    
    last_detection_time = time.time()
    detected_vehicles = []
    occupied_spots = set()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        current_time = time.time()
        # Run detection every second
        if current_time - last_detection_time >= 1.0:
            overview.fill(0)
            results = model(frame, conf=conf_threshold)
            new_detected_vehicles = []
            new_occupied_spots = set()
            
            for result in results:
                for box in result.boxes:
                    coords = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = map(int, coords)
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    
                    if label.lower() in ["car", "truck", "bus"]:
                        center = ((x1 + x2) // 2, (y1 + y2) // 2)
                        # Check against each parking spot using the fast polygon test
                        for spot in parking_spots:
                            if point_in_parking_spot(center, spot):
                                new_occupied_spots.add(spot['number'])
                        new_detected_vehicles.append({
                            'label': f"Car ({conf:.2f})",
                            'position': center,
                            'confidence': conf,
                            'box': (x1, y1, x2, y2)
                        })
            if new_detected_vehicles:
                detected_vehicles = new_detected_vehicles
            occupied_spots = new_occupied_spots
            last_detection_time = current_time
        
        # Draw parking spots with occupied status
        draw_parking_spots(frame, parking_spots, occupied_spots)
        
        # Draw detection bounding boxes and labels
        for vehicle in detected_vehicles:
            x1, y1, x2, y2 = vehicle['box']
            conf = vehicle['confidence']
            label_text = vehicle['label']
            box_color = (0, int(255 * conf), 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            # Compute text background dimensions
            text_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(frame, (x1, y1 - 30), (x1 + text_size[0] + 10, y1), box_color, -1)
            cv2.putText(frame, label_text, (x1 + 5, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Update the overview window with scaled vehicle positions
        overview.fill(0)
        for i, vehicle in enumerate(detected_vehicles):
            scaled_x = int((vehicle['position'][0] / frame.shape[1]) * overview_width)
            scaled_y = int((vehicle['position'][1] / frame.shape[0]) * overview_height)
            cv2.circle(overview, (scaled_x, scaled_y), 5, (0, 255, 0), -1)
            cv2.putText(overview, f"{i+1}: {vehicle['label']}", 
                        (10, 20 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                        (255, 255, 255), 1)
        
        cv2.putText(frame, "Press 'q' to quit", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow("Vehicle Detection and Classification", frame)
        cv2.imshow("Vehicle Overview", overview)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
