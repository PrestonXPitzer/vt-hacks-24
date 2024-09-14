import torch
import cv2
from PIL import Image
import numpy as np

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
    frame_resized = cv2.resize(frame, (640, 640))
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

def generate_frames():
    """
    Generate frames with bounding boxes around the detected people.
    """
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess the frame
        frame_pil = preprocess_image(frame)

        # Perform inference on the frame
        results = model(frame_pil)

        # Draw bounding boxes around the detected people
        for pred in results.pred[0]:
            x1, y1, x2, y2, conf, cls = pred
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        #reduce the size of the image to 80% of the original size
        frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')