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
    
    # Extract the bounding boxes and confidence scores from the output
    boxes = output[0][:, :4].detach().numpy()
    confidences = output[0][:, 4].detach().numpy()
    # Filter detections with low confidence
    mask = confidences > 0.5
    boxes = boxes[mask]
    confidences = confidences[mask]
    
    return boxes, confidences
