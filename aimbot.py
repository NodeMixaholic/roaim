#credit to nodemixahoic and NoName.
import mss
import numpy as np
import cv2
import torch
import time
from hubconf import custom
from detector import detect
from PIL import ImageGrab
import pyautogui
import time
from mss import mss
import win32api, win32con, win32gui

net = custom(path_or_model="!best.pt")
size_scale = 3

with mss() as sct:
    while True:
        t = time.time()
        # Get rect of Window
        hwnd = win32gui.FindWindow(None, 'Roblox')
        rect = win32gui.GetWindowRect(hwnd)
        region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
        wx,wy,ww,wh = region[0], region[1], region[2], region[3]
        # Capture a window screenshot
        window_screenshot = cv2.cvtColor(np.array(sct.grab({"top": wy, "left": wx, "width": ww, "height": wh})), cv2.COLOR_BGR2RGB)
        # Detect objects in the screenshot
        predictions = detect(window_screenshot)

        # Extract positions and classes of detected objects
        objects = []
        for pred in predictions:
            x, y, w, h = pred[2]
            objects.append((x + w / 2, y + h / 2, pred[0]))

        # Find the closest object
        mouse_x, mouse_y = win32api.GetCursorPos()
        closest_object = None
        min_distance = float("inf")
        for obj in objects:
            distance = np.sqrt((mouse_x - obj[0]) ** 2 + (mouse_y - obj[1]) ** 2)
            if distance < min_distance:
                closest_object = obj
                min_distance = distance

        # Calculate the change in the mouse position
        dx = int(closest_object[0] - ww / 2)
        dy = int(closest_object[1] - wh / 2)

        # Move the window and mouse cursor by the calculated amount
        pyautogui.moveRel(dx, dy)
        win32api.SetCursorPos((mouse_x + dx, mouse_y + dy))

        if cv2.waitKey(1) == 27:
                break
        time.sleep(0.01)

cv2.destroyAllWindows()
