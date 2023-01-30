import torch
import torchvision.transforms as transforms
from PIL import Image

def detect(net, image):
    # Resize and normalize the image
    transform = transforms.Compose([
        transforms.Resize((416, 416)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    image = Image.fromarray(image.astype('uint8')).convert('RGB')
    image = transform(image)
    
    # Pass the image through the network
    with torch.no_grad():
        output = net(image)
    
    # Extract the bounding boxes, confidences, and class_ids from the output
    boxes, confidences, class_ids = [], [], []
    for detection in output:
        scores, class_idx = torch.max(detection[:, 5:], dim=1)
        confidence = scores.flatten()
        boxes = detection[:, :4]
        
        # Filter detections with low confidence
        valid_detections = confidence > 0.5
        boxes = boxes[valid_detections]
        confidences = confidence[valid_detections]
        class_ids = class_idx[valid_detections]
    
    return boxes, confidences, class_ids
