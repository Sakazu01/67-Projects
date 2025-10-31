"""
HELPERS
=======
utility functions for the 67 Projects system.
small but mighty. the unsung heroes. 🛠️
"""

from datetime import datetime
import sys


def log_67(message, level="INFO"):
    """
    custom logging function with 67 aesthetic.

    args:
    - message: the message to log
    - level: log level (INFO, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    # color codes for terminal output
    colors = {
        "INFO": "\033[96m",      # cyan
        "WARNING": "\033[93m",   # yellow
        "ERROR": "\033[91m",     # red
        "SUCCESS": "\033[92m",   # green
        "RESET": "\033[0m"       # reset
    }

    # detect level from emoji
    if "✅" in message or "🔥" in message:
        level = "SUCCESS"
    elif "⚠️" in message:
        level = "WARNING"
    elif "❌" in message:
        level = "ERROR"

    color = colors.get(level, colors["INFO"])
    reset = colors["RESET"]

    print(f"{color}[67 {timestamp}] {message}{reset}")
    sys.stdout.flush()


def calculate_distance(point1, point2):
    """
    calculates euclidean distance between two points.
    useful for gesture detection.

    args:
    - point1: (x, y) tuple or MediaPipe landmark
    - point2: (x, y) tuple or MediaPipe landmark

    returns:
    - distance as float
    """
    import math

    # handle MediaPipe landmarks
    if hasattr(point1, 'x'):
        x1, y1 = point1.x, point1.y
    else:
        x1, y1 = point1

    if hasattr(point2, 'x'):
        x2, y2 = point2.x, point2.y
    else:
        x2, y2 = point2

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def normalize_angle(angle):
    """
    normalizes angle to 0-360 range.
    """
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle


def get_angle(point1, point2, point3):
    """
    calculates angle formed by three points.
    useful for detecting bent joints (elbow, knee, etc.)

    args:
    - point1, point2, point3: landmarks forming the angle (point2 is vertex)

    returns:
    - angle in degrees
    """
    import math

    # extract coordinates
    if hasattr(point1, 'x'):
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        x3, y3 = point3.x, point3.y
    else:
        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = point3

    # calculate vectors
    vector1 = (x1 - x2, y1 - y2)
    vector2 = (x3 - x2, y3 - y2)

    # calculate angle using dot product
    dot = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    mag1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    mag2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

    if mag1 == 0 or mag2 == 0:
        return 0

    cos_angle = dot / (mag1 * mag2)
    cos_angle = max(-1, min(1, cos_angle))  # clamp to [-1, 1]

    angle = math.acos(cos_angle)
    return math.degrees(angle)


def fps_counter():
    """
    simple FPS counter generator.

    usage:
    fps = fps_counter()
    while True:
        current_fps = next(fps)
    """
    import time

    frame_times = []

    while True:
        current_time = time.time()
        frame_times.append(current_time)

        # keep only last 30 frames
        frame_times = frame_times[-30:]

        if len(frame_times) > 1:
            fps = len(frame_times) / (frame_times[-1] - frame_times[0])
            yield fps
        else:
            yield 0


def create_gradient_overlay(width, height, color1=(255, 0, 255), color2=(0, 255, 255)):
    """
    creates a gradient overlay image.
    useful for cyberpunk/glitch aesthetics.

    returns:
    - numpy array (BGR image)
    """
    import numpy as np
    import cv2

    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        ratio = y / height
        color = [
            int(color1[i] * (1 - ratio) + color2[i] * ratio)
            for i in range(3)
        ]
        gradient[y, :] = color

    return gradient


def add_glitch_effect(frame, intensity=0.1):
    """
    adds a glitch effect to frame.
    shifts color channels randomly for that brainrot aesthetic.

    args:
    - frame: input image
    - intensity: glitch intensity (0.0 - 1.0)

    returns:
    - glitched frame
    """
    import numpy as np
    import random

    if random.random() > intensity:
        return frame  # no glitch this frame

    glitched = frame.copy()
    h, w = frame.shape[:2]

    # random channel shift
    shift_x = random.randint(-10, 10)
    shift_y = random.randint(-5, 5)

    # shift red channel
    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    glitched[:, :, 2] = cv2.warpAffine(frame[:, :, 2], M, (w, h))

    return glitched


def save_screenshot(frame, prefix="67_screenshot"):
    """
    saves current frame as screenshot.

    returns:
    - saved filename
    """
    import cv2
    from datetime import datetime
    from pathlib import Path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"

    screenshots_dir = Path(__file__).parent.parent / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)

    filepath = screenshots_dir / filename
    cv2.imwrite(str(filepath), frame)

    log_67(f"📸 screenshot saved: {filename}")
    return str(filepath)


# export all functions
__all__ = [
    'log_67',
    'calculate_distance',
    'normalize_angle',
    'get_angle',
    'fps_counter',
    'create_gradient_overlay',
    'add_glitch_effect',
    'save_screenshot'
]
