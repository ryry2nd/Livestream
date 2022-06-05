#imports
from flask import Flask, Response, render_template
from waitress import serve
import cv2, time

#init vars
FPS = 60
COMPRESSION = 18
SIZE = (256, 256)
THREADS = 6
PORT = 8080
HOST = '0.0.0.0'

ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), COMPRESSION]
camera = cv2.VideoCapture(0)
app = Flask('app')

#generates the camera frames
def gen_frames():
    lastFrameTime = time.time()
    while True:
        success, frame = camera.read()  # read the camera frame
        if success:
            ret, buffer = cv2.imencode('.jpg', cv2.resize(frame, SIZE), ENCODE_PARAM)
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
    print("Livestream started!")
    serve(app, host=HOST, port=PORT, threads=THREADS)

#runs if it is not being imported
if __name__ == '__main__':
    main()