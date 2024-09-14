from flask import Flask, render_template, Response, jsonify
from controllers_yolo import generate_frames, get_pedestrian_count  # Import the controllers module

dataPts = []
hourlyPts = []
dailyPts = []
weeklyPts = []

trueIfIncreasing = False


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/line-length')
def line_length():
    count = get_pedestrian_count()
    #increasing decresasin logic
    if 
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

@app.route('/hourly-average')
def hourly_average():
    avg = sum(hourlyPts) / len(hourlyPts) if hourlyPts else 0
    return jsonify(hourlyAverage=avg)

@app.route('/daily-average')
def daily_average():
    avg = sum(dailyPts) / len(dailyPts) if dailyPts else 0
    return jsonify(dailyAverage=avg)

@app.route('/weekly-average')
def weekly_average():
    avg = sum(weeklyPts) / len(weeklyPts) if weeklyPts else 0
    return jsonify(weeklyAverage=avg)

@app.route('/is-increasing')
def is_increasing():
    return jsonify(isIncreasing=trueIfIncreasing)



if __name__ == '__main__':
    app.run(debug=True, host='0.0,0,0', port=5000)