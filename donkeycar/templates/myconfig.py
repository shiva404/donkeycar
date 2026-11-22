# """
# My CAR CONFIG
#
# Overrides for config.py. createcar copies defaults here as comments;
# uncomment or add lines below to change behavior without editing config.py.
# """

# Xbox One / Series controller (xpadneo on Pi)
USE_JOYSTICK_AS_DEFAULT = True
CONTROLLER_TYPE = "xbox"
JOYSTICK_DEVICE_FILE = "/dev/input/js0"
JOYSTICK_MAX_THROTTLE = 0.5
JOYSTICK_STEERING_SCALE = 1.0
# Flip if forward/back is inverted on the stick
JOYSTICK_THROTTLE_DIR = -1.0
JOYSTICK_DEADZONE = 0.01

# Camera: use "MOCK" until rpicam-hello --list-cameras works, then "PICAM"
# CAMERA_TYPE = "PICAM"
