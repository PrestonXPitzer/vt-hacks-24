from flask import Flask, render_template, Response, jsonify
from controllers import generate_frames, get_pedestrian_count  # Import the controllers module

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
    return jsonify(lineLength=count)

if __name__ == '__main__':
    app.run(debug=True)