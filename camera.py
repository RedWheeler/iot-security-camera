import picamera
import pigpio
import io


class Camera:
    MIN_ANGLE = 50
    MAX_ANGLE = 140
    SERVO_1 = 17
    SERVO_2 = 18

    def __init__(self):
        self.__stream = io.BytesIO()
        self.__camera = picamera.PiCamera()
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
        if self.MIN_ANGLE < angle < self.MAX_ANGLE:
            self.__servo1_rotation = angle
            self.__pi.set_servo_pulsewidth(self.SERVO_1, 500 + (angle / 180) * 2000)
        else:
            raise ValueError(f"Value must be between {self.MIN_ANGLE} and {self.MAX_ANGLE}")

    @property
    def servo2_rotation(self):
        return self.__servo2_rotation

    @servo2_rotation.setter
    def servo2_rotation(self, angle):
        if self.MIN_ANGLE < angle < self.MAX_ANGLE:
            self.__servo2_rotation = angle
            self.__pi.set_servo_pulsewidth(self.SERVO_2, 500 + (angle / 180) * 2000)
        else:
            raise ValueError(f"Value must be between {self.MIN_ANGLE} and {self.MAX_ANGLE}")

    def get_frame(self):
        # Clear stream
        self.__stream.seek(0)
        self.__stream.truncate(0)
        # Read new image into stream
        self.__camera.capture(self.__stream, format='jpeg')
        return self.__stream
