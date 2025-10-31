"""
67 PROJECTS - MEME GESTURE DETECTOR
===================================
the main brain. this is where the magic (chaos) happens.
captures video → detects gestures → spawns memes in real-time.

sleep deprivation coded this. it works tho. 🔥
"""

import cv2
import sys
from pathlib import Path

# import our custom modules (the 67 engine)
from core.motion_tracker import MotionTracker
from core.meme_matcher import MemeMatcher
from core.renderer import MemeRenderer
from core.sound_engine import SoundEngine
from utils.helpers import log_67


class MemeGestureDetector:
    """
    the main controller. orchestrates the whole meme-reactive system.
    """

    def __init__(self):
        log_67("🔥 initializing 67 Projects Meme Detector...")

        # initialize all subsystems
        self.motion_tracker = MotionTracker()
        self.meme_matcher = MemeMatcher()
        self.renderer = MemeRenderer()
        self.sound_engine = SoundEngine()

        # video capture setup
        self.cap = cv2.VideoCapture(0)  # 0 = default webcam
        if not self.cap.isOpened():
            log_67("❌ ERROR: couldn't access webcam. check ur setup bro")
            sys.exit(1)

        # set resolution (720p for that crispy feed)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        log_67("✅ system ready. entering meme dimension...")

    def run(self):
        """
        the main loop. this runs every frame.
        capture → detect → match → render → repeat
        """
        log_67("🎬 starting video feed...")

        current_meme = None  # currently active meme

        try:
            while True:
                # capture frame from webcam
                ret, frame = self.cap.read()
                if not ret:
                    log_67("⚠️ frame capture failed. skipping...")
                    continue

                # flip frame horizontally for mirror effect (more intuitive)
                frame = cv2.flip(frame, 1)

                # 1. DETECT GESTURES
                gesture_data = self.motion_tracker.detect(frame)

                # 2. MATCH GESTURE TO MEME
                matched_meme = self.meme_matcher.match(gesture_data)

                # 3. HANDLE MEME STATE CHANGES
                if matched_meme != current_meme:
                    # meme changed! update sound and visuals
                    if matched_meme:
                        log_67(f"🎯 meme triggered: {matched_meme['name']}")
                        self.sound_engine.play(matched_meme.get('sound'))
                    else:
                        log_67("💨 meme faded (no gesture detected)")
                        self.sound_engine.stop()

                    current_meme = matched_meme

                # 4. RENDER OVERLAY
                display_frame = self.renderer.render(
                    frame=frame,
                    gesture_data=gesture_data,
                    meme=current_meme
                )

                # 5. SHOW THE RESULT
                cv2.imshow('67 Projects - Meme Gesture Detector', display_frame)

                # exit on 'q' key or ESC
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:
                    log_67("👋 user exit detected. shutting down...")
                    break

        except KeyboardInterrupt:
            log_67("⚠️ keyboard interrupt. shutting down...")

        finally:
            # cleanup
            self.cleanup()

    def cleanup(self):
        """release resources like a responsible dev"""
        log_67("🧹 cleaning up resources...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.motion_tracker.cleanup()
        self.sound_engine.cleanup()
        log_67("✨ shutdown complete. stay chaotic. 67 out.")


def main():
    """entry point"""
    print("""
    ╔══════════════════════════════════════╗
    ║   67 PROJECTS                        ║
    ║   MEME GESTURE DETECTOR v1.0         ║
    ║   -----------------------------------║
    ║   brainrot made code.                ║
    ║   motion → meme energy.              ║
    ╚══════════════════════════════════════╝
    """)

    detector = MemeGestureDetector()
    detector.run()


if __name__ == "__main__":
    main()
