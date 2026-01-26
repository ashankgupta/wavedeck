import os
import subprocess
import sys

IS_LINUX = sys.platform.startswith("linux")
IS_WAYLAND = os.environ.get("XDG_SESSION_TYPE") == "wayland"

def _ydotool_key(code: int):
    subprocess.run(
        ["ydotool", "key", f"{code}:1", f"{code}:0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def _pyautogui_key(key: str):
    import pyautogui
    pyautogui.press(key)

def send_next():
    if IS_LINUX and IS_WAYLAND:
        _ydotool_key(106)   # Right Arrow
    else:
        _pyautogui_key("right")

def send_prev():
    if IS_LINUX and IS_WAYLAND:
        _ydotool_key(105)   # Left Arrow
    else:
        _pyautogui_key("left")

def send_start():
    if IS_LINUX and IS_WAYLAND:
        _ydotool_key(63)    # F5
    else:
        _pyautogui_key("f5")

def send_exit():
    if IS_LINUX and IS_WAYLAND:
        _ydotool_key(1)     # Esc
    else:
        _pyautogui_key("esc")
