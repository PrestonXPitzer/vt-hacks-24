print("Attempting to import the detector (includes tensorflow)")
from rpidetect.detector import Detector
print("Attempting to import the VideoCapture, rectangle, and imencode functions from cv2")
from cv2 import VideoCapture, rectangle, imencode
print("CV2 and detector imported successfully")
# Initialize the video capture object
print("Initializing the video capture object")
cap = VideoCapture(0)
print("Video capture object initialized successfully")
model_path = 'rpidetect/model/model.tflite'
input_shape = (192, 192)
score_th = 0.4
nms_th = 0.5
num_threads = None


def get_pedestrian_count():
    ret, frame = cap.read()
    if not ret:
        return 0

    detector = Detector(model_path, input_shape, score_th, nms_th, num_threads)
    pedestrians = detector.detect(frame)
    count = len(pedestrians)

    return count

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detector = Detector(model_path, input_shape, score_th, nms_th, num_threads)
        pedestrians = detector.detect(frame)

        for pedestrian in pedestrians:
            x1, y1, x2, y2 = pedestrian
            rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        ret, jpeg = imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
