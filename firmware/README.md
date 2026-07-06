# Firmware Module

This folder contains ESP32-S3 firmware code for DeskEye Guard.

## Responsibilities

- Initialize ESP32-S3 board
- Initialize camera module
- Capture frames or snapshots
- Run basic behavior-state judgment
- Maintain sitting-time counter
- Trigger local reminder output
- Upload status data through Wi-Fi

## Planned Files

```text
firmware/
├── README.md
├── src/
│   └── main.cpp or main.ino
├── include/
├── lib/
└── platformio.ini or Arduino project files
```

## First Milestone

The first firmware milestone is to make the ESP32-S3 camera capture images successfully and print basic status through the serial monitor.
