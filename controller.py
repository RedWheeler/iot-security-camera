import sys
import pigpio

MIN_ANGLE = 50
MAX_ANGLE = 140

pi = pigpio.pi()


def rotate_servo(gpio, angle):
    if MIN_ANGLE < angle < MAX_ANGLE:
        pi.set_servo_pulsewidth(gpio, 500 + (angle / 180) * 2000)
    else:
        print(f"Must enter between {MIN_ANGLE}-{MAX_ANGLE}, you gave: {str(angle)}")


should_sweep = False
while True:
    # Check if new command was issued via STDIN
    for line in sys.stdin:
        if line == "sweep":
            should_sweep = True

        elif line.startswith("rotate="):
            should_sweep = False
            rotation = int(line.split("rotate=", 1)[1])
            rotate_servo(17, rotation)

    if should_sweep:
        # Sweeping code
        pass
