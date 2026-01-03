from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
import cv2
from detector import ChildSafetyDetector
import os
from notifier import AlertSystem
import time
from flask import request

app = Flask(__name__)
CORS(app) # Allows your React frontend to talk to this Python backend

notifier = AlertSystem()
last_alert_time = 0  # To prevent sending 100 messages per second


# Initialize the AI Engine
detector = ChildSafetyDetector()
camera = cv2.VideoCapture(0) # 0 is usually the built-in webcam

 
# Define Danger Zone: [x1, y1, x2, y2] in pixels
# For now, we hardcode it. Later, we can make it dynamic.
DANGER_ZONE = [100, 100, 500, 400] 

def generate_frames():
    global last_alert_time
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # 1. Run AI Analysis
            processed_frame, is_alert = detector.analyze_frame(frame, DANGER_ZONE)
            
            # 2. Draw the Danger Zone box for visual reference
            cv2.rectangle(processed_frame, (DANGER_ZONE[0], DANGER_ZONE[1]), 
                         (DANGER_ZONE[2], DANGER_ZONE[3]), (255, 0, 0), 2)
            cv2.putText(processed_frame, "DANGER ZONE", (DANGER_ZONE[0], DANGER_ZONE[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            # 3. Handle Alert (This is where we will trigger SMS/Email later)
            if is_alert:
                current_time = time.time()
                # Only send alert once every 60 seconds
                if current_time - last_alert_time > 60:
                    notifier.send_whatsapp_alert()
                    notifier.send_email_with_photo(processed_frame)
                    last_alert_time = current_time

            # 4. Encode frame as JPEG to stream to the web
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        

@app.route('/video_feed')
def video_feed():
    """Route that streams the processed video."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    """Simple API endpoint for React to check system health."""
    return jsonify({"status": "Active", "camera": "Connected"})
@app.route('/update_zone', methods=['POST'])

def update_zone():
    global DANGER_ZONE
    data = request.json
    # data format expected: [x1, y1, x2, y2]
    DANGER_ZONE = data['new_zone']
    return jsonify({"message": "Zone updated successfully", "new_zone": DANGER_ZONE})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)