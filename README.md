# DeskEye Guard

**DeskEye Guard：基于 ESP32-S3 的桌面行为感知与坐姿纠正系统**

DeskEye Guard is a lightweight desktop behavior sensing and posture correction system based on ESP32-S3. It uses an ESP32-S3 camera module to observe common desktop scenarios, estimate user behavior states, and provide reminders for unhealthy study or work habits.

## Project Overview

本项目面向宿舍书桌、自习室、个人工作台等桌面场景，尝试使用低成本嵌入式硬件完成基础的行为感知与健康提醒。系统以 ESP32-S3 为核心控制器，通过摄像头采集桌面前方图像，结合轻量级图像处理和规则判断，实现对久坐、低头、距离过近、离座等行为状态的检测，并通过本地提醒或前端页面进行反馈。

项目重点不是做一个复杂的商用 AI 摄像头，而是在有限硬件资源下完成一个完整的计算机系统设计：包括嵌入式端采集、状态判断、无线通信、后端数据记录、前端可视化以及项目文档管理。

## Core Features

- Desktop presence detection: 判断用户是否在桌前。
- Sitting-time monitoring: 记录连续学习/工作时间，触发休息提醒。
- Posture awareness: 基于头部/上半身位置进行简单坐姿判断。
- Screen-distance reminder: 识别用户是否过度靠近屏幕。
- Local feedback: 通过蜂鸣器、LED 或网页提示进行提醒。
- Web dashboard: 展示当前状态、历史记录和提醒次数。
- Extensible design: 后续可扩展数据库、移动端提醒或更复杂的姿态模型。

## Hardware

Planned hardware:

- ESP32-S3 development board
- Camera module, such as OV2640 or compatible ESP32-S3 camera module
- Optional buzzer or LED indicator
- USB power supply
- Computer or phone for dashboard access

## Suggested Repository Structure

```text
DeskEye-Guard/
├── firmware/              # ESP32-S3 firmware code
├── web/                   # Frontend dashboard
├── server/                # Backend API and database service
├── docs/                  # Design documents and project notes
├── assets/                # Images, diagrams, demo screenshots
├── README.md              # Project introduction
└── .gitignore
```

## System Architecture

```text
Camera Module
     ↓
ESP32-S3 Firmware
     ↓
Behavior State Detection
     ↓
Wi-Fi / HTTP / WebSocket
     ↓
Backend API + Database
     ↓
Web Dashboard
```

## Development Roadmap

### Stage 1: Basic Repository and Documentation

- Initialize project structure
- Write README and system design notes
- Define hardware requirements
- Split development tasks into GitHub Issues

### Stage 2: ESP32-S3 Camera Firmware

- Configure camera module
- Capture image frames
- Test basic streaming or snapshot upload
- Add simple rule-based behavior detection

### Stage 3: Reminder Logic

- Implement sitting-time counter
- Implement away-from-desk detection
- Implement posture warning rule
- Add buzzer, LED, or web reminder output

### Stage 4: Web and Backend

- Build backend API for state upload
- Store behavior records
- Build frontend dashboard
- Display current state and historical statistics

### Stage 5: Testing and Presentation

- Test in desk/study scenarios
- Record demo video or screenshots
- Write final report
- Prepare presentation slides

## Current Status

Project repository initialized. The next goal is to complete firmware camera initialization and define the first usable behavior detection prototype.

## License

This project is currently for course design and learning purposes.
