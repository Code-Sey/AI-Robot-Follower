# AI Robot Follower: Vision-Based Person Tracking

A person-following robot that uses a camera and YOLO11 to detect people, lock onto one
selected "owner," and send motion commands to an Arduino-driven robot over serial.

🏆 1st Place (of 8 teams) + Best Design, PGCC C.O.D.E Club Engineering Challenge, April 2026

## How it works
1. **Capture**: `camera.py` grabs frames from the webcam and computes the frame center.
2. **Detect + track**: `detector.py` runs YOLO11n with Ultralytics' BoT-SORT tracker
   (people only), so each person keeps a persistent ID across frames.
3. **Select owner**: press `w` to lock onto the tracked person closest to the frame
   center. Press `z` to release them.
4. **Follow**: each frame, `controller.py` compares the owner's bounding box to the frame:
   - **Steering:** horizontal offset from the frame center, with a ±150 px dead zone so
     the robot doesn't jitter when the owner is roughly centered
   - **Distance:** box area (w × h) stands in for distance, since there's no depth sensor.
     Below 70,000 px² = too far → drive forward while steering (F / FL / FR).
     Above = close enough → turn in place (L / R), or STOP if centered.
   - Commands are only sent over serial when they change, to avoid flooding the Arduino.
5. **Safety**: if the owner is missing for more than 10 frames, the robot stops. A STOP
   command is also sent on any program exit (keypress, camera failure, or crash).

## Hardware story
Originally ran onboard a Raspberry Pi. When the Pi failed right before the competition,
we moved processing to a laptop that sends commands to the Arduino over USB serial
(9600 baud). That's why the code uses a Windows COM port. The Pi version of the code
was lost, which is part of why this repo exists.

## My role
I wrote all the computer vision and control software in this repo.
Hardware and Arduino motor control were built by Basir Mercer.

## Stack
Python · OpenCV · Ultralytics YOLO11 · pyserial · Arduino

## Running it
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
**No robot?** In `main.py`, swap the import to `fake_controller`. It prints commands
instead of sending them over serial, so you can test with just a webcam.

**Controls:** `w` select owner · `z` deselect · `d` quit

## Known limitations / what I'd improve
- **ID switches:** if someone walks in front of the owner, the tracker may assign the
  owner a new ID when they reappear, and the robot loses them until manually re-selected.
  Re-identification by appearance or box position/size would fix this.
- **Thresholded control:** the robot either turns or doesn't at fixed thresholds.
  Proportional control (turn harder the farther off-center the owner is) would be smoother.
- **Resolution-dependent thresholds:** 70,000 px² and 150 px assume a 640×480 camera;
  they should be fractions of the frame size.
- **Box size as distance is rough:** it changes with pose and how the person is turned.
  A depth camera or ultrasonic sensor would be more reliable.
- **No measured performance yet:** next step is logging FPS and command latency.
