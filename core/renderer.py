"""
MEME RENDERER
=============
handles all visual rendering:
- overlays meme images/GIFs on video feed
- draws gesture landmarks (optional debug mode)
- adds UI elements (labels, info)

this is the artist. it makes things pretty. 🎨
"""

import cv2
import numpy as np
from pathlib import Path
from PIL import Image
from utils.helpers import log_67


class MemeRenderer:
    """
    renders memes and overlays on the video feed.
    handles transparency, scaling, and positioning.
    """

    def __init__(self, show_landmarks=True):
        log_67("🎨 initializing meme renderer...")

        self.show_landmarks = show_landmarks
        self.meme_cache = {}  # cache loaded meme images
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        log_67("✅ renderer ready")

    def render(self, frame, gesture_data, meme=None):
        """
        main render method. takes frame and overlays everything.

        args:
        - frame: the video frame (numpy array)
        - gesture_data: detected gesture landmarks
        - meme: current active meme (or None)

        returns:
        - rendered frame with overlays
        """
        display_frame = frame.copy()

        # 1. DRAW LANDMARKS (if enabled)
        if self.show_landmarks:
            display_frame = self._draw_landmarks(display_frame, gesture_data)

        # 2. OVERLAY MEME (if active)
        if meme and 'image_path' in meme:
            display_frame = self._overlay_meme(display_frame, meme)

        # 3. DRAW UI ELEMENTS
        display_frame = self._draw_ui(display_frame, meme, gesture_data)

        return display_frame

    def _draw_landmarks(self, frame, gesture_data):
        """draws detected pose/hand landmarks on frame"""
        # import motion tracker to use its drawing utilities
        from core.motion_tracker import MotionTracker

        # create temporary tracker instance for drawing
        # (in a real app, we'd pass the tracker instance to avoid recreation)
        mp_drawing = MotionTracker().mp_drawing
        mp_pose = MotionTracker().mp_pose
        mp_hands = MotionTracker().mp_hands

        # draw pose
        if gesture_data['pose_landmarks']:
            mp_drawing.draw_landmarks(
                frame,
                gesture_data['pose_landmarks'],
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

        # draw hands
        if gesture_data['hand_landmarks']:
            for hand_lm in gesture_data['hand_landmarks']:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_lm,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

        return frame

    def _overlay_meme(self, frame, meme):
        """
        overlays meme image on the frame.
        handles transparency and positioning.
        """
        image_path = meme.get('image_path')

        if not image_path or not Path(image_path).exists():
            # log_67(f"⚠️ meme image not found: {image_path}")
            return frame

        # load meme from cache or disk
        if image_path not in self.meme_cache:
            self.meme_cache[image_path] = self._load_meme_image(image_path)

        meme_img = self.meme_cache[image_path]

        if meme_img is None:
            return frame

        # get positioning info from meme config
        position = meme.get('position', 'center')  # center, top-left, top-right, etc.
        scale = meme.get('scale', 0.5)  # size relative to frame
        opacity = meme.get('opacity', 0.9)  # transparency

        # resize meme
        frame_h, frame_w = frame.shape[:2]
        meme_h, meme_w = meme_img.shape[:2]

        # calculate new size
        new_w = int(frame_w * scale)
        new_h = int((meme_h / meme_w) * new_w)  # maintain aspect ratio

        meme_resized = cv2.resize(meme_img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # calculate position
        x, y = self._calculate_position(frame, meme_resized, position)

        # overlay with transparency
        frame = self._blend_transparent(frame, meme_resized, x, y, opacity)

        return frame

    def _load_meme_image(self, image_path):
        """
        loads meme image from disk.
        handles PNG transparency.
        """
        try:
            # use PIL to load image with alpha channel
            pil_img = Image.open(image_path)

            # convert to RGBA if not already
            if pil_img.mode != 'RGBA':
                pil_img = pil_img.convert('RGBA')

            # convert to numpy array
            img_array = np.array(pil_img)

            # convert RGBA to BGRA (OpenCV format)
            img_bgra = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGRA)

            return img_bgra

        except Exception as e:
            log_67(f"❌ error loading meme image {image_path}: {e}")
            return None

    def _calculate_position(self, frame, meme, position_key):
        """
        calculates x, y coordinates for meme placement.
        """
        frame_h, frame_w = frame.shape[:2]
        meme_h, meme_w = meme.shape[:2]

        positions = {
            'center': ((frame_w - meme_w) // 2, (frame_h - meme_h) // 2),
            'top-left': (20, 20),
            'top-right': (frame_w - meme_w - 20, 20),
            'bottom-left': (20, frame_h - meme_h - 20),
            'bottom-right': (frame_w - meme_w - 20, frame_h - meme_h - 20),
            'top-center': ((frame_w - meme_w) // 2, 20),
            'bottom-center': ((frame_w - meme_w) // 2, frame_h - meme_h - 20),
        }

        return positions.get(position_key, positions['center'])

    def _blend_transparent(self, background, overlay, x, y, opacity=1.0):
        """
        blends overlay onto background with transparency support.
        handles alpha channel properly.
        """
        bg_h, bg_w = background.shape[:2]
        ov_h, ov_w = overlay.shape[:2]

        # ensure overlay fits within background bounds
        if x < 0 or y < 0 or x + ov_w > bg_w or y + ov_h > bg_h:
            # crop overlay to fit
            x_start = max(0, x)
            y_start = max(0, y)
            x_end = min(bg_w, x + ov_w)
            y_end = min(bg_h, y + ov_h)

            ov_x_start = max(0, -x)
            ov_y_start = max(0, -y)
            ov_x_end = ov_x_start + (x_end - x_start)
            ov_y_end = ov_y_start + (y_end - y_start)

            overlay = overlay[ov_y_start:ov_y_end, ov_x_start:ov_x_end]
            x, y = x_start, y_start
            ov_h, ov_w = overlay.shape[:2]

        # extract alpha channel
        if overlay.shape[2] == 4:  # has alpha channel
            alpha = overlay[:, :, 3] / 255.0 * opacity
            overlay_rgb = overlay[:, :, :3]
        else:
            alpha = np.ones((ov_h, ov_w)) * opacity
            overlay_rgb = overlay

        # extract region of interest
        roi = background[y:y+ov_h, x:x+ov_w]

        # blend using alpha
        for c in range(3):
            roi[:, :, c] = (alpha * overlay_rgb[:, :, c] +
                           (1 - alpha) * roi[:, :, c])

        background[y:y+ov_h, x:x+ov_w] = roi

        return background

    def _draw_ui(self, frame, meme, gesture_data):
        """
        draws UI elements:
        - current meme name
        - detected gestures
        - FPS (optional)
        """
        frame_h, frame_w = frame.shape[:2]

        # draw semi-transparent top bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (frame_w, 60), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

        # draw title
        cv2.putText(frame, "67 PROJECTS - MEME DETECTOR", (10, 25),
                   self.font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)

        # draw active meme name
        if meme:
            meme_text = f"ACTIVE: {meme['name'].upper()}"
            cv2.putText(frame, meme_text, (10, 50),
                       self.font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "NO GESTURE DETECTED", (10, 50),
                       self.font, 0.6, (100, 100, 100), 2, cv2.LINE_AA)

        # draw detected features (debug)
        features = gesture_data.get('gesture_features', {})
        if features:
            y_offset = frame_h - 100
            cv2.putText(frame, "DETECTED:", (10, y_offset),
                       self.font, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
            y_offset += 20

            for feature, value in list(features.items())[:5]:  # show first 5
                text = f"  {feature}: {value}"
                cv2.putText(frame, text, (10, y_offset),
                           self.font, 0.4, (150, 150, 150), 1, cv2.LINE_AA)
                y_offset += 20

        # draw instructions
        cv2.putText(frame, "Press 'Q' or ESC to quit", (frame_w - 250, frame_h - 10),
                   self.font, 0.4, (150, 150, 150), 1, cv2.LINE_AA)

        return frame
