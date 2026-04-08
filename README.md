# Real Time Object Tracker
## Overview

This project is a real-time object tracker built using Python and OpenCV. The user selects an object from the webcam feed, and the system tracks it as it moves.

## Approach

I used OpenCV’s CSRT tracker since the task is focused on tracking a user-selected object, not detecting objects automatically.

Flow:

1. Open the webcam and show a live preview
2. User selects object using a bounding box
3. Initialize the tracker with that region
4. Update and display tracking in real time

## Features
* Live webcam tracking
* Manual object selection (ROI)
* Real-time bounding box updates
* FPS display

## Setup 
```python
git clone <your-repo-url>
cd object-tracker

python3 -m venv venv
source venv/bin/activate

pip install opencv-contrib-python
```

## Run
```python
python tracker.py
```
Controls:

* s → select object
* q → quit


# Implementation Details

This solution is implemented using Python and OpenCV. I used the CSRT tracker for single-object tracking since the task requires tracking a user-selected object rather than detecting objects automatically.

The system first opens a live webcam feed and displays a preview. The user selects the object by drawing a bounding box on a chosen frame. The tracker is then initialized using this region and updated on each subsequent frame to estimate the object’s new position.

The tracking result is visualized by drawing a bounding box around the object, along with an FPS counter to indicate performance. On macOS, the AVFoundation backend is used to ensure reliable webcam access.

## Demo

A demo video is included showing the tracking performance in real time.

## Improvements (if extended)
* Re-detection if tracking fails
* Multi-object tracking
* Integration with detection models 
