import torch
import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as T


def detect(model, image):
    image = np.array(Image.fromarray(image))
    transform = T.Compose([
        T.Resize(640),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    image = Image.fromarray(image)
    image_tensor = transform(image).unsqueeze(0)
    output = model(image_tensor)

    boxes = output[0]['boxes'].detach().numpy()
    scores = output[0]['scores'].detach().numpy()
    labels = output[0]['labels'].detach().numpy()

    return boxes, scores, labels
