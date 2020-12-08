import picamera
import pigpio
import io
import cv2
import numpy as np


class Camera:
    MIN_ANGLE = 50
    MAX_ANGLE = 140
    SERVO_1 = 18
    SERVO_2 = 17

    def __init__(self):
        self.__camera = picamera.PiCamera()
        self.__camera.resolution = (640, 360)
        self.__hog = cv2.HOGDescriptor()
        self.__hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.should_sweep = False
        self.object_detection = False
        self.__sweep_angle = 5
        # Servo init
        self.__pi = pigpio.pi()
        self.__servo1_rotation = 90
        self.servo1_rotation = 90
        self.__servo2_rotation = 90
        self.servo2_rotation = 90

    # Increment servo 1's rotation by the specified angle
    def rotate_servo1(self, angle):
        if self.__servo1_rotation + angle > self.MAX_ANGLE:
            self.servo1_rotation = self.MAX_ANGLE
        elif self.__servo1_rotation + angle < self.MIN_ANGLE:
            self.servo1_rotation = self.MIN_ANGLE
        else:
            self.servo1_rotation = self.servo1_rotation + angle

    # Increment servo 2's rotation by the specified angle
    def rotate_servo2(self, angle):
        if self.__servo2_rotation + angle > self.MAX_ANGLE:
            self.servo2_rotation = self.MAX_ANGLE
        elif self.__servo2_rotation + angle < self.MIN_ANGLE:
            self.servo2_rotation = self.MIN_ANGLE
        else:
            self.servo2_rotation = self.servo2_rotation + angle

    @property
    def servo1_rotation(self):
        return self.__servo1_rotation

    @servo1_rotation.setter
    def servo1_rotation(self, angle):
        if self.MIN_ANGLE <= angle <= self.MAX_ANGLE:
            self.__servo1_rotation = angle
            self.__pi.set_servo_pulsewidth(self.SERVO_1, 500 + (angle / 180) * 2000)
        else:
            raise ValueError(f"Value must be between {self.MIN_ANGLE} and {self.MAX_ANGLE}")

    @property
    def servo2_rotation(self):
        return self.__servo2_rotation

    @servo2_rotation.setter
    def servo2_rotation(self, angle):
        if self.MIN_ANGLE <= angle <= self.MAX_ANGLE:
            self.__servo2_rotation = angle
            self.__pi.set_servo_pulsewidth(self.SERVO_2, 500 + (angle / 180) * 2000)
        else:
            raise ValueError(f"Value must be between {self.MIN_ANGLE} and {self.MAX_ANGLE}")

    def detect_people(self, image):
        image = cv2.imdecode(np.fromstring(image, np.uint8), 1)
        boxes, weights = self.__hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        _, result = cv2.imencode('.JPEG', image)
        return result.tobytes()

    def get_frame(self):
        if self.should_sweep:
            # flip sweep direction when min or max angle is reached
            if self.servo2_rotation >= self.MAX_ANGLE or self.servo2_rotation <= self.MIN_ANGLE:
                self.__sweep_angle *= -1
            self.rotate_servo2(self.__sweep_angle)
        # Clear stream
        stream = io.BytesIO()
        # Read new image into stream
        self.__camera.capture(stream, format='jpeg')
        stream.seek(0)
        if self.object_detection:
            return self.detect_people(stream.read())
        else:
            return stream.read()