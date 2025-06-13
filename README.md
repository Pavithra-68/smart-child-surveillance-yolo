# smart-child-surveillance-yolo
A smart surveillance system for child safety using YOLO for object detection and real-time alerts.
🚨 Child Danger Zone Detection System
This project is a real-time child detection and alerting system using computer vision. It identifies when a child enters a predefined danger zone using the YOLOv8 object detection model and MediaPipe pose estimation. Alerts are sent via email and SMS, and an image of the alert is saved for history and monitoring.

💡 Features
🎥 Real-time camera feed processing with YOLOv8 and MediaPipe

🧒 Differentiates between Adult and Child based on height estimation

🔴 Detects when a Child enters a Danger Zone

📸 Automatically captures an image when danger is detected

📩 Sends Email with image attachment

📱 Sends SMS alert using Twilio

📁 Maintains Alert History with timestamps

🗑️ Allows deletion of specific or all alerts

🧭 View system via a browser-based interface

🛠️ Tech Stack
Technology	Purpose
Python	Main programming language
Flask	Web server framework
OpenCV	Video and image processing
YOLOv8	Person detection
MediaPipe	Pose estimation and landmarks
Twilio	SMS notification
SMTP	Email sending with image
SQLite	(Optional) Alert history database
HTML/CSS	Frontend templates

