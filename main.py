#imports
from flask import Flask, render_template, Response
import cv2

#init vars
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FPS, 10)
fps = int(camera.get(5))
app = Flask('app')

#generates the camera frames
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if success:
            ret, buffer = cv2.imencode('.jpg', cv2.resize(frame, (16, 16)))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            
            k = cv2.waitKey(1)

#the video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#root
@app.route('/')
def index():
    return render_template('index.html')

#main function
def main():
    app.run(host='0.0.0.0', port=8080)

#runs if it is not being imported
if __name__ == '__main__':
    main()