# Hardware Notes

## 1. Core Board

The core controller is ESP32-S3. It is selected because it provides Wi-Fi, enough GPIO resources, camera support, and better AI/vision-oriented capability than earlier ESP32 variants.

## 2. Camera Module

A camera module such as OV2640 or another ESP32-S3-compatible camera can be used.

Main tasks:

- Confirm camera pin mapping
- Test image capture
- Adjust resolution and frame rate
- Evaluate lighting and camera position

## 3. Camera Placement

Recommended placement:

- Put the camera above or near the monitor.
- Keep it facing the upper body or head area.
- Avoid strong backlight.
- Make sure the user's face/upper body is visible in normal sitting posture.

If screen brightness cannot be detected directly, the system can avoid relying on screen brightness and instead focus on user behavior states, such as sitting time, distance, and posture.

## 4. Reminder Output

Possible reminder methods:

- LED blinking
- Buzzer sound
- Web dashboard warning
- Browser notification

For early prototype, web dashboard warning is the simplest. LED or buzzer can be added later.

## 5. Hardware Test Checklist

- ESP32-S3 can be flashed successfully
- Serial output works
- Camera initializes successfully
- A frame can be captured
- Wi-Fi connection works
- State data can be sent to backend or browser
