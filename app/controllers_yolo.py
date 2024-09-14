import torch
import cv2
from PIL import Image
import numpy as np
import time

# Load the YOLOv5 model outside of the functions
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.4  # Confidence threshold
model.iou = 0.5  # IoU threshold
model.classes = None  # Detect all classes
model.agnostic = False  # Class-agnostic NMS
print("Shape Loaded Successfully, attempting to start camera")
cap = cv2.VideoCapture(0)
print("Cameara Started Successfully")
def preprocess_image(frame):
    """
    Preprocess the input frame to the required dimensions for YOLOv5.
    """
    # Resize the frame to 640x640 pixels 
    frame_resized = cv2.resize(frame, (240, 240))
    # Convert the frame to a PIL image
    frame_pil = Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
    return frame_pil

def get_pedestrian_count():
    """
    Detect the number of people in the frame and return the count.
    """
    ret, frame = cap.read()
    if not ret:
        return 0

    # Preprocess the frame
    frame_pil = preprocess_image(frame)

    # Perform inference on the frame
    results = model(frame_pil)

    # Get the number of people detected
    count = (results.pred[0][:, -1] == 0).sum().item()  # Class '0' is 'person' in COCO dataset

    return count

def generate_frames(fps=2):
    delay = 1.0 / fps  # Calculate the delay between frames

    while True:
        # Wait for the delay period before capturing the next frame
        time.sleep(delay)

        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')