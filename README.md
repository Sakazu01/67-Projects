# 67 PROJECTS
## MEME GESTURE DETECTOR

```
███████╗███████╗    ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗███████╗
██╔════╝╚════██║    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝██╔════╝
███████╗    ██╔╝    ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   ███████╗
██╔════╝   ██╔╝     ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   ╚════██║
███████╗   ██║      ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   ███████║
╚══════╝   ╚═╝      ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   ╚══════╝

MEME GESTURE DETECTOR - where motion meets brainrot
```

> **brainrot made code. motion → meme energy.**

---

## 🔥 WHAT IS THIS

A real-time gesture detection system that spawns memes when you move.

The concept is simple but cursed:
1. Camera watches your upper body
2. AI detects your gestures (hands, pose, face)
3. When you match a meme gesture → meme appears on screen
4. Stop the gesture → meme fades instantly

It's like your computer is possessed by meme energy and reacts to your every move.

---

## ✨ FEATURES

- **Real-time gesture tracking** using MediaPipe
  - Hands (peace signs, pointing, open palms)
  - Body pose (T-pose, salute, arms crossed)
  - Face expressions (sigma stare, wide eyes)

- **Meme overlay system**
  - Transparent PNG/GIF overlays
  - Configurable position, scale, opacity
  - Instant fade when gesture stops

- **Sound effects**
  - Audio triggers per meme
  - Synchronized with gesture state

- **Expandable architecture**
  - Add new memes via JSON config
  - Drop images in `/assets/memes`
  - No code changes needed

- **Clean modular codebase**
  - Separation of concerns
  - Easy to understand and modify
  - Documented with chaotic energy

---

## 📦 INSTALLATION

### Requirements
- Python 3.8+
- Webcam
- Your sanity (optional)

### Setup

```bash
# clone or download this repo
cd 67-Projects

# create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

### Add Meme Assets

The system needs meme images to work. Add your memes to `assets/memes/`:

Required meme files (create placeholder images if needed):
- `sigma_stare.png`
- `peace_sign.png`
- `skibidi_salute.gif`
- `tpose.png`
- `pointing.png`
- `open_palm.png`
- `arms_crossed.png`
- `double_hand.png`

Optionally add sounds to `assets/sounds/`:
- `sigma.mp3`
- `vine_boom.mp3`
- `skibidi.mp3`

> **Pro tip:** Use transparent PNGs for best results. The system supports alpha channels.

---

## 🚀 USAGE

Run the detector:

```bash
python main.py
```

### Controls
- **Q** or **ESC** - Quit the application
- Just move and let the chaos unfold

### Supported Gestures

| Gesture | How to trigger | Meme |
|---------|---------------|------|
| **Peace Sign** | ✌️ two fingers up | peace_sign |
| **Salute** | Hand to forehead | skibidi_salute |
| **T-Pose** | Arms horizontal, extended | tpose_dominance |
| **Pointing** | Index finger extended | pointing_moment |
| **Open Palm** | Show full hand | open_palm_vibes |
| **Arms Crossed** | Cross arms over chest | arms_crossed_boss |
| **Double Hand Raise** | Both hands up | double_hand |
| **Sigma Stare** | Hold still, intense gaze | sigma_stare |

---

## ⚙️ CONFIGURATION

Edit `config/memes.json` to customize memes and gestures.

### Example Meme Definition

```json
{
  "name": "peace_sign",
  "description": "throw up the peace sign ✌️",
  "triggers": {
    "gesture": "peace_sign"
  },
  "image": "peace_sign.png",
  "sound": "vine_boom.mp3",
  "position": "top-right",
  "scale": 0.25,
  "opacity": 0.85
}
```

### Trigger Types

1. **Single gesture:**
   ```json
   "triggers": { "gesture": "peace_sign" }
   ```

2. **Multiple gestures (AND):**
   ```json
   "triggers": { "gestures": ["hand_raised_left", "hand_raised_right"] }
   ```

3. **Any gesture (OR):**
   ```json
   "triggers": { "any_of": ["tpose", "arms_crossed"] }
   ```

4. **Conditions with thresholds:**
   ```json
   "triggers": { "conditions": { "face_stillness": {">": 0.7} } }
   ```

### Position Options
- `center`, `top-left`, `top-right`, `bottom-left`, `bottom-right`
- `top-center`, `bottom-center`

---

## 🛠️ PROJECT STRUCTURE

```
67-projects/
├── main.py                      # entry point - runs the system
├── core/
│   ├── motion_tracker.py        # MediaPipe gesture detection
│   ├── meme_matcher.py          # gesture → meme mapping logic
│   ├── renderer.py              # overlay + visualization
│   └── sound_engine.py          # audio playback
├── assets/
│   ├── memes/                   # meme images/GIFs
│   └── sounds/                  # audio effects
├── config/
│   └── memes.json               # meme definitions
├── utils/
│   └── helpers.py               # utility functions
└── requirements.txt             # dependencies
```

---

## 🎨 ADDING YOUR OWN MEMES

1. **Create/find a meme image**
   - PNG with transparency works best
   - Or use GIF for animations

2. **Add to assets**
   ```bash
   cp your_meme.png assets/memes/
   ```

3. **Define in config**
   Add entry to `config/memes.json`:
   ```json
   {
     "name": "your_meme",
     "description": "your description here",
     "triggers": {
       "gesture": "peace_sign"
     },
     "image": "your_meme.png",
     "position": "center",
     "scale": 0.4,
     "opacity": 0.8
   }
   ```

4. **Run and test**
   ```bash
   python main.py
   ```

That's it. No code changes needed.

---

## 🐛 TROUBLESHOOTING

### Webcam not detected
- Check if camera is connected
- Try changing camera index in `main.py` (line 30):
  ```python
  self.cap = cv2.VideoCapture(0)  # try 1, 2, etc.
  ```

### Gestures not detecting
- Ensure good lighting
- Stand ~1-2 meters from camera
- Check that upper body is fully visible

### Memes not showing
- Verify image files exist in `assets/memes/`
- Check file names match config
- Look for errors in console

### Low FPS / Lag
- Lower webcam resolution in `main.py`
- Reduce meme image sizes
- Set `show_landmarks=False` in renderer

### Sound not playing
- Check audio files in `assets/sounds/`
- Verify pygame installed correctly
- Check system audio settings

---

## 🧪 DEVELOPMENT

### Running in debug mode

Set `show_landmarks=True` in renderer to see detected keypoints.

### Live config reload

Edit `config/memes.json` while running, then call:
```python
detector.meme_matcher.reload_config()
```

### Custom gesture detection

Add your own gesture detectors in `motion_tracker.py`:
```python
def _is_custom_gesture(self, landmarks):
    # your detection logic here
    return True  # if detected
```

Then extract feature in `_extract_features()`:
```python
if self._is_custom_gesture(pose_lm):
    features['custom_gesture'] = True
```

---

## 🌊 THE 67 PHILOSOPHY

This project embodies the 67 aesthetic:
- **Chaotic but organized** - Clean code, cursed concept
- **Experimental** - Try weird shit and see what happens
- **Expandable** - Built to be hacked and extended
- **Brainrot energy** - Memes meet machine learning

It's what happens when you give AI 48 hours of no sleep and unlimited meme access.

---

## 📜 LICENSE

This is experimental chaos. Do whatever you want with it.

If you build something cool, let the world know.
If you break something, that's part of the experience.

---

## 🤝 CONTRIBUTING

This is 67 Projects. There are no rules.

Add gestures. Add memes. Add chaos.
Break things. Fix things. Make it weirder.

Just keep it modular and documented.

---

## 📞 SUPPORT

If something breaks:
1. Check the troubleshooting section
2. Read the error message
3. Google it
4. Try turning it off and on again
5. Add more memes (this always helps)

If nothing works, you've achieved true 67 status.

---

## 🔮 FUTURE IDEAS

- [ ] Multi-person gesture detection
- [ ] Gesture combos (sequence-based triggers)
- [ ] AI-generated memes on the fly
- [ ] VR integration (memes in 3D space)
- [ ] Networked meme battles
- [ ] Gesture-controlled music visualization
- [ ] TikTok integration (record meme moments)
- [ ] Voice commands + gestures
- [ ] AR mode with phone camera

The possibilities are endless.
The brainrot is eternal.

---

```
Built with chaos, powered by memes.
This is 67 Projects.

Stay weird. 🔥
```
