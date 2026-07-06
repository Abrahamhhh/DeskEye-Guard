# System Design

## 1. System Name

DeskEye Guard: A Desktop Behavior Sensing and Posture Correction System Based on ESP32-S3

## 2. Design Motivation

Long-time computer use often causes unhealthy study habits, including poor posture, sitting too long, and getting too close to the screen. DeskEye Guard tries to use a low-cost ESP32-S3 camera device to provide lightweight behavior awareness and timely reminders.

## 3. Overall Architecture

```text
Camera Module
     ↓
ESP32-S3 Firmware
     ↓
Image / Behavior Processing
     ↓
State Decision Logic
     ↓
Local Reminder + Network Upload
     ↓
Backend API
     ↓
Web Dashboard
```

## 4. ESP32-S3 Side

The ESP32-S3 side is responsible for image capture, basic state judgment, and communication.

Main responsibilities:

- Initialize camera
- Capture frames
- Run lightweight image processing or rule-based judgment
- Maintain sitting-time counter
- Trigger local reminders
- Upload state data through Wi-Fi

Possible state values:

- `normal`: user is present and posture is acceptable
- `too_close`: user is too close to the screen
- `head_down`: user may be looking down for too long
- `away`: user is away from the desk
- `long_sitting`: user has been sitting for too long

## 5. Backend Side

The backend receives status data from the ESP32-S3 and stores it for later visualization.

Possible API design:

- `POST /api/state`: upload current behavior state
- `GET /api/state/latest`: get current state
- `GET /api/records`: get historical records
- `GET /api/statistics`: get daily statistics

## 6. Frontend Side

The frontend dashboard presents behavior status and statistics.

Main pages:

- Current status card
- Sitting-time timer
- Warning history table
- Daily summary chart
- System settings panel

## 7. Privacy Design

The system should avoid storing raw camera images by default. It should mainly upload behavior states, timestamps, and warning types. If images are needed for debugging, they should be saved manually and clearly marked as debug data.

## 8. Technical Challenges

- ESP32-S3 has limited computing power compared with a computer.
- Camera placement affects detection quality.
- Lighting conditions may cause unstable image results.
- Real posture estimation may require a more powerful side service or simplified rules.

## 9. Feasible Implementation Strategy

The first version should use simple and reliable rules instead of a heavy AI model. For example:

- Use face or head region size to estimate distance.
- Use object/person presence to determine whether the user is at the desk.
- Use time counters to detect long sitting.
- Use front-end statistics to strengthen the system-level design.

Later versions can add computer-side CV processing or lightweight model inference.
