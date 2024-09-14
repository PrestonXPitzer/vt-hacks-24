from flask import Flask, render_template, Response, jsonify
from controllers_yolo import generate_frames, get_pedestrian_count  # Import the controllers module
import math
import random
dataPts = []
hourlyPts = []
dailyPts = []
weeklyPts = []
lastCount = 0
#the values here should be the output of a sin wave + random noise
grubHub = [int(math.sin(x) * 3 + 4) + random.randint(1,3) for x in range(60)]
grubhub_index = 0

trueIfIncreasing = False


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('beta.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/line-length')
def line_length():
    global trueIfIncreasing
    global dataPts
    global hourlyPts
    global dailyPts
    global weeklyPts
    global lastCount

    count = get_pedestrian_count()
    if count > lastCount:
        trueIfIncreasing = True
    else:
        trueIfIncreasing = False
    lastCount = count
    
    if len(dataPts) < 60:
        dataPts.append(count)
    else:
        if len(hourlyPts) < 24:
            hourlyPts.append(sum(dataPts)/len(dataPts))
        else:
            if len(dailyPts) < 7:
                dailyPts.append(sum(hourlyPts)/len(hourlyPts))
            else:
                weeklyPts.append(sum(dailyPts)/len(dailyPts))
                dailyPts = []
            hourlyPts = []
        dataPts = []
    return jsonify(lineLength=count)

@app.route('/computed-data')
def computed_data():
    global grubhub_index
    grubhub_index += 1
    return jsonify(lineLength=get_pedestrian_count(),
                    hourlyAverage=sum(hourlyPts) / len(hourlyPts) if hourlyPts else 0,
                    dailyAverage=sum(dailyPts) / len(dailyPts) if dailyPts else 0,
                    weeklyAverage=sum(weeklyPts) / len(weeklyPts) if weeklyPts else 0,
                    isIncreasing=trueIfIncreasing,
                    grubHub=grubHub[grubhub_index % len(grubHub)])



if __name__ == '__main__':
    app.run(debug=True, host='0.0,0,0', port=5000)