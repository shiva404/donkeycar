# """
# My CAR CONFIG
#
# Overrides for config.py. createcar copies defaults here as comments;
# uncomment or add lines below to change behavior without editing config.py.
# """

# Xbox One / Series controller (xpadneo on Pi)
# Left stick X = steering, right stick Y = throttle (also LT/RT)
USE_JOYSTICK_AS_DEFAULT = True
CONTROLLER_TYPE = "xbox"
JOYSTICK_DEVICE_FILE = "/dev/input/js0"
JOYSTICK_MAX_THROTTLE = 0.5
JOYSTICK_STEERING_SCALE = 1.0
# Flip if forward/back is inverted on the right stick
JOYSTICK_THROTTLE_DIR = -1.0
JOYSTICK_DEADZONE = 0.01

# PWM values from calibrate (update after measuring on YOUR car).
# Reverse on most ESCs requires: reverse -> stopped -> reverse again.
PWM_STEERING_THROTTLE = {
    "PWM_STEERING_PIN": "PCA9685.1:40.1",
    "PWM_THROTTLE_PIN": "PCA9685.1:40.0",
    "PWM_STEERING_SCALE": 1.0,
    "PWM_STEERING_INVERTED": False,
    "PWM_THROTTLE_SCALE": 1.0,
    "PWM_THROTTLE_INVERTED": False,
    "STEERING_LEFT_PWM": 460,
    "STEERING_RIGHT_PWM": 290,
    "THROTTLE_FORWARD_PWM": 395,
    "THROTTLE_STOPPED_PWM": 390,
    "THROTTLE_REVERSE_PWM": 330,
}

# Camera: use "MOCK" until rpicam-hello --list-cameras works, then "PICAM"
# CAMERA_TYPE = "PICAM"
