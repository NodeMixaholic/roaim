#credit to nodemixahoic and NoName.
#also to monokim for code inspiration.
import mss
import numpy as np
import cv2
import torch
import time
from hubconf import custom
import pyautogui
import win32api, win32con, win32gui
model = custom(path_or_model='yolov7-e6e.pt')


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
        out = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        labels, cord_thres = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        cv2.imshow('s', out)
        centers = [img_w / 2, img_h / 2]
        
        #detect boxes
        detected_boxes = []
        for i in range(n):
            row = cord[i]
            xmin, ymin, xmax, ymax = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
            left, right, top, bottom = int(xmin * img_w), int(xmax * img_w), int(ymin * img_h), int(ymax * img_h)
            detected_boxes.append((left, right, top, bottom))
        # Pixel difference between crosshair(center) and the closest object
        x = centers[0] - img_w/2
        y = centers[1] - img_h/2 - (detected_boxes[0][2] - detected_boxes[0][1]) * 0.45

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

cv2.destroyAllWindows()
