"""
MOTION TRACKER
==============
uses MediaPipe to detect:
- upper body pose
- hand gestures
- facial landmarks

extracts gesture patterns for the meme matcher to analyze.
this module is the eyes. it sees everything. 👁️
"""

import cv2
import mediapipe as mp
import numpy as np
from utils.helpers import log_67


class MotionTracker:
    """
    handles all gesture and motion detection using MediaPipe.
    detects pose, hands, and face landmarks in real-time.
    """

    def __init__(self):
        log_67("👀 initializing motion tracking...")

        # initialize MediaPipe solutions
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils

        # create detector instances
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1  # 0=lite, 1=full, 2=heavy (we use balanced)
        )

        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6,
            max_num_hands=2  # track both hands
        )

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_faces=1,
            refine_landmarks=True  # get iris landmarks too
        )

        log_67("✅ motion tracker ready")

    def detect(self, frame):
        """
        main detection method. analyzes frame and extracts all gesture data.

        returns a dict with:
        - pose_landmarks: body keypoints
        - hand_landmarks: hand keypoints (left/right)
        - face_landmarks: facial keypoints
        - gesture_features: extracted high-level features
        """
        # convert BGR to RGB (MediaPipe uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # run all detectors
        pose_results = self.pose.process(rgb_frame)
        hand_results = self.hands.process(rgb_frame)
        face_results = self.face_mesh.process(rgb_frame)

        # extract landmarks
        gesture_data = {
            'pose_landmarks': pose_results.pose_landmarks,
            'hand_landmarks': hand_results.multi_hand_landmarks,
            'hand_labels': hand_results.multi_handedness if hand_results.multi_handedness else [],
            'face_landmarks': face_results.multi_face_landmarks[0] if face_results.multi_face_landmarks else None,
            'gesture_features': {}
        }

        # extract high-level features for easier gesture matching
        gesture_data['gesture_features'] = self._extract_features(gesture_data)

        return gesture_data

    def _extract_features(self, gesture_data):
        """
        extracts high-level gesture features from raw landmarks.
        makes it easier for meme_matcher to identify gestures.

        features include:
        - hand_raised_left / hand_raised_right
        - peace_sign_detected
        - pointing_detected
        - face_confidence (how still/focused the face is)
        - arms_crossed
        - salute_detected
        """
        features = {}

        # === HAND FEATURES ===
        if gesture_data['hand_landmarks']:
            for idx, hand_lm in enumerate(gesture_data['hand_landmarks']):
                # determine which hand (left/right)
                hand_label = gesture_data['hand_labels'][idx].classification[0].label

                # get wrist position (landmark 0)
                wrist = hand_lm.landmark[0]

                # check if hand is raised (wrist above y=0.5, where 0=top, 1=bottom)
                if wrist.y < 0.5:
                    features[f'hand_raised_{hand_label.lower()}'] = True

                # detect peace sign (index and middle finger extended)
                if self._is_peace_sign(hand_lm):
                    features['peace_sign'] = True

                # detect pointing (only index finger extended)
                if self._is_pointing(hand_lm):
                    features['pointing'] = True

                # detect open palm (all fingers extended)
                if self._is_open_palm(hand_lm):
                    features[f'open_palm_{hand_label.lower()}'] = True

        # === POSE FEATURES ===
        if gesture_data['pose_landmarks']:
            pose_lm = gesture_data['pose_landmarks'].landmark

            # detect salute (right hand near head)
            if self._is_salute(pose_lm):
                features['salute'] = True

            # detect arms crossed
            if self._is_arms_crossed(pose_lm):
                features['arms_crossed'] = True

            # detect T-pose (arms out horizontally)
            if self._is_tpose(pose_lm):
                features['tpose'] = True

        # === FACE FEATURES ===
        if gesture_data['face_landmarks']:
            face_lm = gesture_data['face_landmarks'].landmark

            # detect sigma stare (minimal movement, focused gaze)
            features['face_stillness'] = self._calculate_face_stillness(face_lm)

            # detect if eyes are wide open (shock/surprise)
            features['eyes_wide'] = self._is_eyes_wide(face_lm)

        return features

    # === HAND GESTURE DETECTORS ===

    def _is_peace_sign(self, hand_landmarks):
        """detects peace sign ✌️"""
        lm = hand_landmarks.landmark
        # check if index (8) and middle (12) tips are above their PIPs (6, 10)
        # and ring (16) and pinky (20) are below their PIPs (14, 18)
        index_up = lm[8].y < lm[6].y
        middle_up = lm[12].y < lm[10].y
        ring_down = lm[16].y > lm[14].y
        pinky_down = lm[20].y > lm[18].y
        return index_up and middle_up and ring_down and pinky_down

    def _is_pointing(self, hand_landmarks):
        """detects pointing gesture 👉"""
        lm = hand_landmarks.landmark
        index_up = lm[8].y < lm[6].y
        middle_down = lm[12].y > lm[10].y
        ring_down = lm[16].y > lm[14].y
        pinky_down = lm[20].y > lm[18].y
        return index_up and middle_down and ring_down and pinky_down

    def _is_open_palm(self, hand_landmarks):
        """detects open palm 🖐️"""
        lm = hand_landmarks.landmark
        # all fingertips above their middle joints
        fingers_up = [
            lm[8].y < lm[6].y,   # index
            lm[12].y < lm[10].y, # middle
            lm[16].y < lm[14].y, # ring
            lm[20].y < lm[18].y  # pinky
        ]
        return sum(fingers_up) >= 3  # at least 3 fingers up

    # === POSE DETECTORS ===

    def _is_salute(self, pose_landmarks):
        """detects salute gesture (hand near forehead)"""
        # right wrist (16) near right eye/forehead (2)
        right_wrist = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        right_eye = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE.value]

        # calculate distance
        distance = np.sqrt(
            (right_wrist.x - right_eye.x)**2 +
            (right_wrist.y - right_eye.y)**2
        )

        return distance < 0.15  # threshold for "near head"

    def _is_arms_crossed(self, pose_landmarks):
        """detects arms crossed pose"""
        left_wrist = pose_landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        left_shoulder = pose_landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # wrists should be near opposite shoulders
        left_wrist_near_right = abs(left_wrist.x - right_shoulder.x) < 0.2
        right_wrist_near_left = abs(right_wrist.x - left_shoulder.x) < 0.2

        return left_wrist_near_right and right_wrist_near_left

    def _is_tpose(self, pose_landmarks):
        """detects T-pose (assert dominance)"""
        left_wrist = pose_landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        left_shoulder = pose_landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = pose_landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # wrists should be horizontally aligned with shoulders
        left_horizontal = abs(left_wrist.y - left_shoulder.y) < 0.1
        right_horizontal = abs(right_wrist.y - right_shoulder.y) < 0.1

        # wrists should be far from body (arms extended)
        left_extended = abs(left_wrist.x - left_shoulder.x) > 0.3
        right_extended = abs(right_wrist.x - right_shoulder.x) > 0.3

        return left_horizontal and right_horizontal and left_extended and right_extended

    # === FACE DETECTORS ===

    def _calculate_face_stillness(self, face_landmarks):
        """
        calculates how still the face is (for sigma stare detection).
        returns a value 0-1 where 1 = perfectly still.
        in a real implementation, this would track variance over frames.
        for now, we return a placeholder.
        """
        # TODO: implement frame-to-frame variance tracking
        return 0.8  # placeholder

    def _is_eyes_wide(self, face_landmarks):
        """detects wide open eyes (shock face)"""
        # MediaPipe face mesh indices for eyelids
        # upper eyelid: 159, lower eyelid: 145 (right eye)
        upper = face_landmarks[159]
        lower = face_landmarks[145]

        # calculate vertical distance
        eye_openness = abs(upper.y - lower.y)

        return eye_openness > 0.02  # threshold for "wide open"

    def draw_landmarks(self, frame, gesture_data):
        """
        draws detected landmarks on frame for visualization.
        useful for debugging.
        """
        # draw pose
        if gesture_data['pose_landmarks']:
            self.mp_drawing.draw_landmarks(
                frame,
                gesture_data['pose_landmarks'],
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

        # draw hands
        if gesture_data['hand_landmarks']:
            for hand_lm in gesture_data['hand_landmarks']:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_lm,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

        return frame

    def cleanup(self):
        """release MediaPipe resources"""
        log_67("🧹 closing motion tracker...")
        self.pose.close()
        self.hands.close()
        self.face_mesh.close()
