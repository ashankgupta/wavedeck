# Wave Deck

## Description

A Python application that enables control of PowerPoint presentations through hand gestures detected via webcam. It utilizes computer vision to interpret gestures and simulate keyboard inputs for seamless presentation management.

## Features

- Real-time hand gesture recognition using MediaPipe
- Single-hand navigation for slide control
- Two-hand gesture to toggle recognition on/off
- Palm gestures for starting and exiting slideshows
- Cross-platform compatibility (Linux, Windows)
- Visual feedback with on-screen status overlay
- Support for Wayland and X11 on Linux

## Requirements

- Python 3.10 or higher
- Webcam
- Dependencies: mediapipe, opencv-python, pyautogui, pyinstaller

## Installation

1. Clone the repository:
   ```
   https://github.com/ashankgupta/wavedeck.git
   cd ppt-handgesture
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. (Linux with Wayland) Install ydotool for input simulation:
   ```
   # On Ubuntu/Debian
   sudo apt install ydotool
   ```

## Usage

1. Connect and ensure your webcam is functional.

2. Launch the application:
   ```
   python main.py
   ```

3. A window will display the camera feed with detected hand landmarks.

4. Perform gestures in front of the camera:
   - **Next slide**: Raise index finger on right hand
   - **Previous slide**: Raise index finger on left hand
   - **Start slideshow**: Open right palm (hold for 0.6 seconds)
   - **Exit slideshow**: Open left palm (hold for 0.6 seconds)
   - **Toggle gestures**: Open both palms (hold for 1.0 second) to enable/disable recognition

5. The on-screen overlay shows the current gesture status (ENABLED/DISABLED).

6. Press the Escape key in the application window to exit.

## Building Executables

To create standalone executables:

### Windows
Use the provided GitHub Actions workflow or run:
```
pyinstaller --onefile --noconsole --collect-data mediapipe --icon icon.ico --version-file version_info.txt --name HandGesturePresenter main.py
```

### Linux
Run:
```
pyinstaller HandGesturePresenter.spec
```

Ensure all dependencies are installed and test the build on the target platform.

## Troubleshooting

- If gestures are not detected, check lighting and camera positioning.
- On Linux Wayland, ensure ydotool is installed and running.
- Adjust tunable parameters in `config.py` for sensitivity (e.g., detection confidence, hold times).

## License

This project is licensed under the MIT License.
