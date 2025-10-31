"""
MEME MATCHER
============
the logic layer that maps detected gestures to memes.
loads meme definitions from config and matches them to current gesture state.

this is where chaos meets order. 🧠
"""

import json
from pathlib import Path
from utils.helpers import log_67


class MemeMatcher:
    """
    matches gesture features to meme definitions.
    loads meme configs and performs real-time matching.
    """

    def __init__(self, config_path='config/memes.json'):
        log_67("🧠 initializing meme matcher...")

        self.config_path = Path(__file__).parent.parent / config_path
        self.memes = []
        self.last_matched = None  # track last matched meme for state management

        # load meme definitions
        self._load_memes()

        log_67(f"✅ loaded {len(self.memes)} meme definitions")

    def _load_memes(self):
        """loads meme definitions from config file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.memes = config.get('memes', [])

            # validate and enrich meme data
            for meme in self.memes:
                # ensure required fields exist
                if 'name' not in meme or 'triggers' not in meme:
                    log_67(f"⚠️ skipping invalid meme definition: {meme}")
                    continue

                # resolve asset paths
                if 'image' in meme:
                    meme['image_path'] = str(Path(__file__).parent.parent / 'assets' / 'memes' / meme['image'])

                if 'sound' in meme:
                    meme['sound_path'] = str(Path(__file__).parent.parent / 'assets' / 'sounds' / meme['sound'])

        except FileNotFoundError:
            log_67(f"⚠️ config file not found: {self.config_path}")
            log_67("using empty meme list")
        except json.JSONDecodeError as e:
            log_67(f"❌ error parsing config: {e}")
            log_67("using empty meme list")

    def match(self, gesture_data):
        """
        matches current gesture data to a meme.

        returns:
        - meme dict if match found
        - None if no match
        """
        features = gesture_data.get('gesture_features', {})

        if not features:
            return None  # no features detected, no meme

        # iterate through memes and check if triggers match
        for meme in self.memes:
            if self._check_triggers(meme['triggers'], features):
                # match found!
                self.last_matched = meme
                return meme

        # no match found
        return None

    def _check_triggers(self, triggers, features):
        """
        checks if gesture features match meme triggers.

        triggers can be:
        - single feature: {"gesture": "peace_sign"}
        - multiple features (AND): {"gestures": ["hand_raised_right", "peace_sign"]}
        - any feature (OR): {"any_of": ["tpose", "arms_crossed"]}

        returns True if triggers match current features.
        """
        # single feature trigger
        if 'gesture' in triggers:
            return features.get(triggers['gesture'], False)

        # multiple features (AND logic)
        if 'gestures' in triggers:
            return all(features.get(g, False) for g in triggers['gestures'])

        # any of multiple features (OR logic)
        if 'any_of' in triggers:
            return any(features.get(g, False) for g in triggers['any_of'])

        # complex condition with thresholds
        if 'conditions' in triggers:
            return self._check_conditions(triggers['conditions'], features)

        log_67(f"⚠️ unknown trigger format: {triggers}")
        return False

    def _check_conditions(self, conditions, features):
        """
        checks complex conditions with thresholds.
        example: {"face_stillness": {">": 0.7}}
        """
        for feature, condition in conditions.items():
            feature_value = features.get(feature)

            if feature_value is None:
                return False

            # check comparison operators
            if isinstance(condition, dict):
                for operator, threshold in condition.items():
                    if operator == '>':
                        if not (feature_value > threshold):
                            return False
                    elif operator == '<':
                        if not (feature_value < threshold):
                            return False
                    elif operator == '>=':
                        if not (feature_value >= threshold):
                            return False
                    elif operator == '<=':
                        if not (feature_value <= threshold):
                            return False
                    elif operator == '==':
                        if not (feature_value == threshold):
                            return False
            else:
                # direct value check
                if feature_value != condition:
                    return False

        return True

    def reload_config(self):
        """reloads meme config (useful for live updates during dev)"""
        log_67("🔄 reloading meme config...")
        self.memes = []
        self._load_memes()
        log_67(f"✅ reloaded {len(self.memes)} memes")
