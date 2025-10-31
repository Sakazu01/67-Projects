"""
SOUND ENGINE
============
handles all audio playback for meme sound effects.
plays sounds when memes trigger, stops when they fade.

this is the DJ. it drops the beats. 🔊
"""

import pygame
from pathlib import Path
from utils.helpers import log_67


class SoundEngine:
    """
    manages audio playback using pygame mixer.
    supports playing one-shot sounds and looping audio.
    """

    def __init__(self, enable_sound=True):
        log_67("🔊 initializing sound engine...")

        self.enable_sound = enable_sound
        self.current_sound = None
        self.current_channel = None

        if self.enable_sound:
            try:
                # initialize pygame mixer
                pygame.mixer.init(
                    frequency=44100,  # CD quality
                    size=-16,         # 16-bit
                    channels=2,       # stereo
                    buffer=512        # small buffer for low latency
                )
                log_67("✅ sound engine ready")
            except Exception as e:
                log_67(f"⚠️ failed to initialize sound: {e}")
                log_67("continuing without audio...")
                self.enable_sound = False
        else:
            log_67("🔇 sound disabled")

    def play(self, sound_path, loop=False):
        """
        plays a sound file.

        args:
        - sound_path: path to audio file (mp3, wav, ogg)
        - loop: if True, loops the sound indefinitely
        """
        if not self.enable_sound or not sound_path:
            return

        # resolve path
        if not Path(sound_path).exists():
            # log_67(f"⚠️ sound file not found: {sound_path}")
            return

        try:
            # stop current sound if playing
            if self.current_channel and self.current_channel.get_busy():
                self.current_channel.stop()

            # load and play sound
            sound = pygame.mixer.Sound(sound_path)
            loops = -1 if loop else 0  # -1 = infinite loop, 0 = play once

            self.current_channel = sound.play(loops=loops)
            self.current_sound = sound

            # log_67(f"🎵 playing sound: {Path(sound_path).name}")

        except Exception as e:
            log_67(f"❌ error playing sound {sound_path}: {e}")

    def stop(self):
        """stops currently playing sound"""
        if not self.enable_sound:
            return

        if self.current_channel and self.current_channel.get_busy():
            self.current_channel.stop()
            # log_67("🛑 sound stopped")

    def set_volume(self, volume):
        """
        sets playback volume.

        args:
        - volume: 0.0 (silent) to 1.0 (max)
        """
        if not self.enable_sound:
            return

        volume = max(0.0, min(1.0, volume))  # clamp to 0-1
        pygame.mixer.music.set_volume(volume)

        if self.current_sound:
            self.current_sound.set_volume(volume)

    def cleanup(self):
        """cleanup mixer resources"""
        if self.enable_sound:
            log_67("🧹 closing sound engine...")
            self.stop()
            pygame.mixer.quit()
