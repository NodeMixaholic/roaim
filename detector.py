import torch
import torchvision.transforms as transforms
from PIL import Image

def detect(net, window_screenshot):
    # Convert the screenshot to PIL Image and resize it
    window_screenshot = Image.fromarray(window_screenshot)
    window_screenshot = window_screenshot.resize((416, 416))
    
    # Transform the image for input to the network
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    window_screenshot = transform(window_screenshot).unsqueeze(0)

    # Pass the image through the network
    with torch.no_grad():
        output = net(window_screenshot)
    
    # Extract the bounding boxes, confidences, and class_ids from the output
    boxes, confidences, class_ids = [], [], []
    for detection in output:
        scores, class_idx = torch.max(detection[:, 5:], dim=1)
        confidence = scores.flatten()
        try:
            boxes = detection[:, :4]
            # Filter detections with low confidence
            valid_detections = confidence > 0.5
            boxes = boxes[valid_detections]
            confidences = confidence[valid_detections]
            class_ids = class_idx[valid_detections]
            return boxes, confidences
        except:
            print("n/a")
            return 1,[0]
            
