import cv2
import time
import requests
try:
    from ultralytics import YOLO
except ImportError:
    print("ultralytics not installed. Install via: pip install ultralytics")
    YOLO = None

API_URL = "http://localhost:5000/api/surveillance/alert"

def simulate_surveillance():
    print("Starting AI Surveillance Agent...")
    if YOLO is None:
        print("YOLO not available. Exiting.")
        return
        
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0) # Use webcam for demo
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
        
    last_alert_time = 0
    alert_cooldown = 10 # Seconds between alerts
    
    print("Surveillance active. Press 'q' to quit.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Run inference
        results = model(frame, stream=True, verbose=False)
        
        anomaly_detected = False
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Class 0 is 'person' in COCO dataset
                # We simulate an anomaly if a person is detected with high confidence
                if cls == 0 and conf > 0.7:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, "ANOMALY: Person Detected", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    anomaly_detected = True
                    
        cv2.imshow('CCTV Surveillance Feed', frame)
        
        current_time = time.time()
        if anomaly_detected and (current_time - last_alert_time > alert_cooldown):
            print("Anomaly Detected! Dispatching alert...")
            try:
                payload = {
                    "type": "Suspicious Activity (Person Detected)",
                    "lat": 28.6139, # Example lat
                    "lng": 77.2090, # Example lng
                    "camera_id": "CCTV-01-MainStreet",
                    "severity": "High"
                }
                res = requests.post(API_URL, json=payload)
                if res.status_code == 201:
                    print("Alert successfully sent to dashboard.")
                last_alert_time = current_time
            except Exception as e:
                print("Failed to send alert:", e)
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    simulate_surveillance()
