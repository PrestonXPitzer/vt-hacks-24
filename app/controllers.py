import cv2

cap = cv2.VideoCapture(0)

# Load the Haar cascade
cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'
print("Loading the Haar cascade xml, this may take a while...")
cascade = cv2.CascadeClassifier(cascade_path)
print("Load Complete!")

def get_pedestrian_count():
    ret, frame = cap.read()
    if not ret:
        return 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pedestrians = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    count = len(pedestrians)  # This can be replaced with a region of interest check at some point, but for now
    # just return the number of pedestrians detected

    return count

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pedestrians = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw bounding boxes
        for (x, y, w, h) in pedestrians:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')