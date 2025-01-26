import threading
import win32api, win32con
import time
import random
import os
from threading import Lock

# Add the lock for thread safety
lock = Lock()

# Default sleep time for autoclicker
sleep_timer = 0.01  # Default minimum sleep time

def rclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(random.uniform(0.04, 0.07))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.uniform(0.01, 0.03))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

clicking_enabled = True

def clickassist():
    global clicking_enabled
    while True:
        if win32api.GetAsyncKeyState(0x4E) & 0x8000:
            clicking_enabled = False

        if win32api.GetAsyncKeyState(0x4D) & 0x8000:
            clicking_enabled = True
        time.sleep(0.01)
        if clicking_enabled and win32api.GetAsyncKeyState(0x01) & 0x8000:
            for clicks in range(1):
                click()

def fastplace():
    global fastplace_enabled
    while True:
        if win32api.GetAsyncKeyState(0x4E) & 0x8000:
            fastplace_enabled = False

        if win32api.GetAsyncKeyState(0x4D) & 0x8000:
            fastplace_enabled = True

        time.sleep(0.01)

        if fastplace_enabled and win32api.GetAsyncKeyState(0x02) & 0x8000:
            for clicks in range(3):
                rclick()

def update_sleep_time(value):
    """Update the sleep_timer value from the GUI slider."""
    global sleep_timer
    with lock:
        # Ensuring sleep_timer stays within the valid range 0.01 - 0.1
        sleep_timer = max(0.01, min(value / 10, 0.1))  # Slider max value is 100, so dividing by 10

def backtrack():
    while True:
        os.system("ping -t -l 65500 localhost")

def autoclicker():
    """Autoclicker function triggered by key presses."""
    while True:
        time.sleep(0.01)
        if win32api.GetAsyncKeyState(0x52) & 0x8000:  # Key 'R' to start
            while True:
                with lock:
                    delay = sleep_timer  # Get the current sleep timer value
                time.sleep(delay)  # Use the dynamic sleep timer
                click()  # Perform the click action

                if win32api.GetAsyncKeyState(0x58) & 0x8000:  # Key 'X' to stop
                    break
