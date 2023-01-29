#credit to nodemixahoic and NoName.
#also to monokim for code inspiration.
import mss
import numpy as np
import cv2
import torch
import time
from hubconf import custom
import pyautogui
import time
import win32api, win32con, win32gui
model = custom(path_or_model='!best.pt')
size_scale = 3

with mss.mss() as sct:
    while True:
        t = time.time()
        # Get rect of Window
        hwnd = win32gui.FindWindow(None, 'Roblox')
        rect = win32gui.GetWindowRect(hwnd)
        region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
        # Get image of screen
        ori_img = np.array(pyautogui.screenshot(region=region))
        ori_img = cv2.resize(ori_img, (ori_img.shape[1] // size_scale, ori_img.shape[0] // size_scale))
        image = np.expand_dims(ori_img, 0)
        img_w, img_h = image.shape[2], image.shape[1]
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)             
        results = model(img)
        results.render()
        results = results.xyxyn
        out = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow('s', out)
        try:
            labels, cords = results[0][:, -1].numpy(), results[0][:, :-1].numpy()
        except:
            labels, cords = results[0][:, -1].cpu().numpy(), results[0][:, :-1].cpu().numpy()
        
        n = 0
        # Pixel difference between crosshair(center) and the closest object
        x = ((img_h/img_w)*1000) - (cords[0] - img_w)
        y = ((img_h/img_w)*1000) - img_h/2 - (cords[1] * (img_h)) * 0.45

        # Move mouse and shoot
        scale = 1.7 * size_scale
        x = int(x * scale)
        y = int(y * scale)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        print('fps: {}'.format(1 / (time.time() - t)))

        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.01)

cv2.destroyAllWindows()
