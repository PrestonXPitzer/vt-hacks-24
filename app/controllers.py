import cv2

# Initialize the video capture object
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
    
    count = len(pedestrians) #This can be replaced with a region of interest check at some point, but for now
    #just return the number of pedestrians detected

    return count

def generate_frames():
    while True:
        # Capture frame-by-frame
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')