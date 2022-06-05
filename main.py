#imports
from flask import Flask, Response, render_template
from waitress import serve
import cv2, time

#init vars
FPS = 30
camera = cv2.VideoCapture(0)
app = Flask('app')

#generates the camera frames
def gen_frames():
    lastFrameTime = time.time()
    while True:
        success, frame = camera.read()  # read the camera frame
        if success:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
            ret, buffer = cv2.imencode('.jpg', cv2.resize(frame, (256, 256)), encode_param)
            yield(b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

            sleepTime = 1./FPS - (time.time() - lastFrameTime)
            if sleepTime > 0:
                time.sleep(sleepTime)
            lastFrameTime = time.time()

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
    serve(app, host='0.0.0.0', port=8080, threads=6)

#runs if it is not being imported
if __name__ == '__main__':
    main()