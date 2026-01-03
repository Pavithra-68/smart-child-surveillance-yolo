import cv2
import mediapipe as mp
from ultralytics import YOLO

class ChildSafetyDetector:
    def __init__(self):
        # 1. Initialize YOLOv8 (n = nano version for speed)
        self.model = YOLO('yolov8n.pt') 
        
        # 2. Initialize MediaPipe Pose for height estimation
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5)

    def is_child(self, frame, bbox):
        """
        Determines if a detected person is a child based on 
        the relative height of their skeletal landmarks.
        """
        x1, y1, x2, y2 = map(int, bbox)
        roi = frame[y1:y2, x1:x2] # Crop to the person
        
        if roi.size == 0: return False

        # Process the crop with MediaPipe
        results = self.pose.process(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        
        if not results.pose_landmarks:
            return False

        # Logic: Measure distance from Nose to Ankle
        landmarks = results.pose_landmarks.landmark
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE].y
        ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE].y
        
        person_height_in_box = abs(ankle - nose)
        
        # In a standard YOLO box, a child's skeleton usually covers 
        # less vertical space than an adult's.
        return person_height_in_box < 0.7 

    def analyze_frame(self, frame, danger_zone):
        """
        Analyzes the frame for people and checks danger zone intersection.
        danger_zone format: [x1, y1, x2, y2]
        """
        results = self.model(frame, verbose=False)
        alert_triggered = False
        
        for r in results:
            for box in r.boxes:
                # Class 0 is 'person' in COCO dataset
                if int(box.cls) == 0:
                    coords = box.xyxy[0].tolist()
                    
                    # Check if the person is a child
                    child_status = self.is_child(frame, coords)
                    
                    # Check if center of person is inside the danger zone
                    cx = (coords[0] + coords[2]) / 2
                    cy = (coords[1] + coords[3]) / 2
                    
                    in_zone = (danger_zone[0] < cx < danger_zone[2] and 
                               danger_zone[1] < cy < danger_zone[3])

                    if child_status and in_zone:
                        alert_triggered = True
                        color = (0, 0, 255) # Red
                        label = "ALERT: CHILD IN DANGER"
                    else:
                        color = (0, 255, 0) # Green
                        label = "Child" if child_status else "Adult"

                    # Draw visual feedback
                    cv2.rectangle(frame, (int(coords[0]), int(coords[1])), 
                                 (int(coords[2]), int(coords[3])), color, 2)
                    cv2.putText(frame, label, (int(coords[0]), int(coords[1])-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame, alert_triggered