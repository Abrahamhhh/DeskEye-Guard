# DeskEye Guard Project Plan

## 1. Project Goal

DeskEye Guard aims to build a practical desktop behavior sensing and posture correction system based on ESP32-S3. The project focuses on a complete system design process, including embedded sensing, lightweight behavior recognition, reminder logic, wireless communication, data recording, and dashboard visualization.

## 2. Target Scenario

The system is designed for personal desktop scenarios such as dormitory desks, study rooms, and home workstations. It helps users notice unhealthy study habits, including sitting for too long, getting too close to the screen, leaving the desk for long periods, or maintaining a poor head/upper-body posture.

## 3. Main Modules

### Firmware Module

- Camera initialization
- Frame capture
- Basic behavior state detection
- Wi-Fi connection
- Data upload to backend or dashboard
- Local reminder output

### Backend Module

- Receive behavior state data from ESP32-S3
- Store records in a database
- Provide API for frontend dashboard
- Support later data analysis

### Frontend Module

- Show current user state
- Show sitting-time statistics
- Show warning history
- Provide simple configuration interface

### Documentation Module

- Hardware connection notes
- System architecture
- Test records
- Final report material

## 4. Development Stages

### Stage 1: Repository Initialization

- Build repository structure
- Write README
- Create development issues
- Define project scope

### Stage 2: ESP32-S3 Camera Prototype

- Complete camera module test
- Capture image successfully
- Send test data through serial or Wi-Fi

### Stage 3: Behavior Detection Prototype

- Detect whether a person is present
- Estimate whether the user is too close to the screen
- Add simple posture rules
- Add sitting-time counter

### Stage 4: Web Dashboard Prototype

- Build backend API
- Store records
- Display state and statistics on frontend

### Stage 5: Final Integration

- Connect firmware, backend, and frontend
- Test real desktop scenarios
- Prepare report, demo, and presentation

## 5. Minimum Viable Product

The MVP should include:

- ESP32-S3 camera can capture frames
- System can distinguish at least three states: normal, away, warning
- A simple reminder can be triggered
- A web page can display current state
- README and design documents are complete

## 6. Possible Extensions

- Add MediaPipe-style posture estimation on a computer-side assistant service
- Add database statistics for daily study behavior
- Add privacy mode that avoids saving raw images
- Add mobile notification or browser notification
- Add model distillation or lightweight classification later
