# Vision-Based Robotic Hand Gesture Control

A vision-based robotic hand control system that uses a camera, MediaPipe hand tracking, Python, and STS3215 bus servos to reproduce human hand movements on a robotic hand.

## Project Overview

This project focuses on controlling a tendon-driven robotic hand using human hand movements captured through a camera.

The system detects the human hand using MediaPipe, extracts 21 hand landmarks, calculates finger joint angles, and converts these movements into servo positions. The calculated commands are sent to STS3215 bus servos through the STServo SDK.

## System Workflow

Camera
↓
Hand Detection using MediaPipe
↓
21 Hand Landmarks
↓
Finger Angle Calculation
↓
Servo Position Mapping
↓
Calibration
↓
STServo SDK
↓
STS3215 Servos
↓
Robotic Hand Movement

## Features

- Real-time hand detection
- 21-point hand landmark tracking
- Finger joint angle calculation
- Human-to-robot movement mapping
- Servo calibration
- STS3215 bus servo control
- Individual servo testing
- Real-time camera-based servo control
- Servo position and feedback reading

## Technologies Used

### Software

- Python
- OpenCV
- MediaPipe
- NumPy
- STServo Python SDK

### Hardware

- STS3215 bus servos
- 16-servo robotic hand
- Bus Servo Adapter
- External power supply
- USB serial communication

## Hand Tracking

MediaPipe is used to detect 21 landmarks on the human hand.

The landmarks are used to determine:

- Finger joint angles
- Finger bending
- Hand orientation
- Hand movement

These measurements are then converted into servo commands.

## Servo Calibration

Each servo has a unique ID and a calibrated position range.

Example:

| Servo ID | Function | Calibration |
|----------|----------|-------------|
| 1 | Pinky sideward | 1220 |
| 2 | Pinky middle upper | 3661 |
| 3 | Pinky bottom | 4027 |
| 4 | Ring middle upper | 3403 |
| 6 | Ring bottom | 3370 |
| 7 | Index bottom | 922 |
| 9 | Index middle upper | 3471 |
| 10 | Middle middle upper | 597 |
| 11 | Middle bottom | 1302 |
| 13 | Thumb bottom | 3756 |
| 14 | Thumb middle upper | 922 |

The calibration values are used to convert human finger movement into appropriate robotic servo positions.

## Servo Communication

The robotic hand uses STS3215 bus servos.

Each servo is assigned a unique ID, allowing multiple servos to communicate through the same serial bus.

Current communication configuration:

- Port: COM11
- Baud rate: 1,000,000 bps
- Servo protocol: STServo
- Position range: 0–4095

Servo commands include:

- Torque enable
- Target position
- Speed
- Acceleration
- Present position
- Present speed
- Present load

## Software Architecture

The software is divided into several modules:

### `hand_tracking.py`

Handles:

- Camera input
- MediaPipe hand detection
- Landmark extraction
- Finger angle calculation

### `calibration.py`

Contains the experimentally determined servo calibration values.

### `gesture_mapping.py`

Converts detected human hand movements and angles into servo target positions.

### `main.py`

Coordinates the camera processing, hand tracking, gesture mapping, and servo control.

### `servo_tests/`

Contains programs used to individually test and diagnose the STS3215 servos.

## Testing

The development process was divided into multiple stages:

1. Individual servo communication testing
2. Servo position testing
3. Torque testing
4. Servo calibration
5. Camera-based hand tracking
6. Human finger angle calculation
7. Camera-to-servo integration

All 16 servos were individually tested before integrating them with the vision-control system.

## Project Status

The project is being developed in stages.

- [x] MediaPipe hand detection
- [x] 21-point hand landmark detection
- [x] Finger angle calculation
- [x] Servo communication
- [x] Individual servo testing
- [x] Servo calibration
- [x] Initial camera-to-servo integration
- [ ] Complete integration of all 16 servos
- [ ] Final full-hand demonstration

## Safety

This project involves high-torque robotic servos.

During testing:

- Keep hands and objects away from moving mechanisms.
- Use the emergency stop when necessary.
- Test servo movements at low speed first.
- Verify the correct servo ID before sending movement commands.
- Use the appropriate power supply for each servo.

## Installation

Clone the repository:

```bash
git clone https://github.com/Farhan-Ahmed-Mohammed/robotic-hand-gesture-control.git
