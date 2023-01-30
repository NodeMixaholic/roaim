import cv2
import numpy as np
from mss import mss

def detect(net, window_screenshot):
    # Create a 4D blob from the window_screenshot
    blob = cv2.dnn.blobFromImage(window_screenshot, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Run forward pass to get the detections
    layer_outputs = net.forward(net.getLayerNames())

    # Initialize lists to store detections
    boxes = []
    confidences = []
    class_ids = []

    # Loop over each of the layer outputs
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Get the bounding box coordinates
                box = detection[0:4] * np.array([window_screenshot.shape[1], window_screenshot.shape[0], window_screenshot.shape[1], window_screenshot.shape[0]])
                (center_x, center_y, width, height) = box.astype("int")

                # Calculate the top-left and bottom-right coordinates of the bounding box
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maximum suppression to suppress overlapping detections
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

    # Extract positions and classes of detected objects
    objects = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        x, y, w, h = box
        objects.append([x + w / 2, y + h / 2, class_ids[i]])

    return objects
