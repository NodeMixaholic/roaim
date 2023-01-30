import torch
import torchvision.transforms as transforms
from PIL import Image

def detect(net, image):
    # Convert numpy array to PyTorch tensor
    image = torch.from_numpy(image)
    # Add batch dimension
    image = image.unsqueeze(0)
    # Normalize the image
    mean = [0.5, 0.5, 0.5]
    std = [0.5, 0.5, 0.5]
    image = (image / 255.0 - mean) / std
    # Pass the image through the network
    with torch.no_grad():
        output = net(image)
    # Extract the bounding boxes and confidence scores from the output
    boxes = output[0][:, :4].detach().numpy()
    confidences = output[0][:, 4].detach().numpy()
    # Filter detections with low confidence
    mask = confidences > 0.5
    boxes = boxes[mask]
    confidences = confidences[mask]
    return boxes, confidences
