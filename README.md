# GuardianAI: Smart Child Safety Monitoring System

A Full-Stack AI surveillance solution designed to detect children entering "Danger Zones" (e.g., swimming pools, balconies) and trigger real-time alerts.

##  Tech Stack
- **Frontend:** React.js, Tailwind CSS, Vite
- **Backend:** Python (Flask), OpenCV
- **AI/ML:** YOLOv8 (Object Detection), MediaPipe (Pose Estimation)
- **Alerts:** Twilio API (SMS/WhatsApp), SMTP (Email with Image Attachments)

##  Key Features
- **Real-time Detection:** Processes live video streams to identify human figures.
- **Intelligent Classification:** Differentiates between adults and children using skeletal height-ratio analysis via MediaPipe.
- **Danger Zone Logic:** Users can define specific pixel coordinates; if a child's center-point enters the zone, an alert triggers.
- **Automated Alerts:** Sends instant Email notifications with a captured snapshot of the incident.
- **Professional Dashboard:** A modern React interface to monitor the live feed and system status.

##  Installation & Setup
1. **Clone the Repo:** `git clone https://github.com/yourusername/child-safety-ai.git`
2. **Backend Setup:**
   - `cd backend`
   - `pip install -r requirements.txt`
   - Create a `.env` file with your Twilio/Email credentials.
   - `python app.py`
3. **Frontend Setup:**
   - `cd frontend`
   - `npm install`
   - `npm run dev`

##  System Architecture
The system utilizes a decoupled architecture where the Flask server handles high-compute AI processing and streams M-JPEG frames to the React client for a low-latency monitoring experience.

## 📸 Project Preview

### Real-Time Monitoring Dashboard
![Dashboard Screenshot](./screenshots/dashboard.png)

### Automated Email Alert System
*When a child enters the danger zone, the system captures a frame and sends an instant email.*
![Email Alert](./screenshots/email_alert.png)
