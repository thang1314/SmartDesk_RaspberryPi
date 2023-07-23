import io
import picamera
import socketio

ADDRESS = 'http://172.20.10.2:1010'

sio = socketio.Client()
sio.connect(ADDRESS)
camera = picamera.PiCamera(resolution='640x480', framerate=9)

camera_check = False

def handle_stream():
    global camera
    global camera_check

    stream = io.BytesIO()

    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        if camera_check:
            stream.seek(0)
            sio.emit('video', stream.read())
            stream.seek(0)
            stream.truncate()
        else:
            break

@sio.on('request-stream')
def handle_request_stream():
    global camera
    global camera_check
    camera_check = True
    handle_stream()

@sio.on('cancel')
def cancel_handle():
    global camera
    global camera_check
    camera_check = False