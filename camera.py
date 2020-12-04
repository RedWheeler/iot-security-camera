import picamera

class Camera:
    def __init__(self):
        self.image = open('stream.jpg', 'wb')
        self.camera = picamera.PiCamera()

    def get_frame(self):
        # Process and return frame
        self.camera.capture(self.image)
        return self.image
