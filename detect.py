import cv2
import numpy as np

def detect(net, image):
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(net.getUnconnectedOutLayersNames())
    
    boxes, confidences, class_ids = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.5:
                box = detection[0:4] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
                (center_x, center_y, width, height) = box.astype("int")
                
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))
                
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                
    return boxes, confidences, class_ids
