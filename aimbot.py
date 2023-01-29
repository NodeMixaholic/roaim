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
        img_w, img_h,w2,h2 = image.shape[2], image.shape[1], imaage.shape[4], image.shape[3]
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)             
        results = model(img)
        results.render()
        out = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        try:
            labels, cord_thres = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        except:
            labels, cord_thres = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
        cv2.imshow('s', out)
        
        newdata = []
        if len(results) >=2:
                for x in test:
                    item, confidence_rate, imagedata = x
                    x1, y1, w_size, h_size = imagedata
                    x_start = round(x1 - (w_size/2))
                    y_start = round(y1 - (h_size/2))
                    x_end = round(x_start + w_size)
                    y_end = round(y_start + h_size)
                    data = (item, confidence_rate, (x_start, y_start, x_end, y_end), w_size, h_size)
                    newdata.append(data)

        elif len(results) == 1:
                item, confidence_rate, imagedata = test[0]
                x1, y1, w_size, h_size = imagedata
                x_start = round(x1 - (w_size/2))
                y_start = round(y1 - (h_size/2))
                x_end = round(x_start + w_size)
                y_end = round(y_start + h_size)
                data = (item, confidence_rate, (x_start, y_start, x_end, y_end), w_size, h_size)
                newdata.append(data)

        else:
                newdata = False
        n = 0
        centers = [(newdata[0][1] - newdata[0][0]) / 2, (newdata[0][2] - newdata[0][3]) / 2]
        # Pixel difference between crosshair(center) and the closest object
        x = centers[0] - img_w/2
        y = centers[1] - img_h/2 - (newdata[0][1] - newdata[0][0]) * 0.45

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
