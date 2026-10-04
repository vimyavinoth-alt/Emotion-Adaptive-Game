# Emotion Adaptive Game using AI

A beginner-friendly AI + game-development project in Python.

## Project idea

The game observes the player's facial emotion through a webcam and adapts the game difficulty.

### Adaptation examples

| Emotion | Game response |
|---|---|
| Happy | Harder |
| Neutral | Normal |
| Sad | Easier |
| Angry | Easier |
| Fear | Easier |
| Surprise | Harder |

The project uses:

- Python
- Pygame
- OpenCV
- DeepFace

## Important: webcam is optional

If the webcam cannot be opened, the game automatically enters **Demo Mode**. This lets you demonstrate the project even on a computer where camera permissions, drivers, or privacy settings are unavailable.

## Installation

Recommended: **Python 3.12**.

Open Command Prompt in this project folder:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

The first DeepFace run can take a while because AI model files may need to be prepared/downloaded.

## Controls

- Left Arrow: move left
- Right Arrow: move right
- Q / Esc: quit

## Project structure

```text
Emotion_Adaptive_Game/
├── main.py
├── game.py
├── emotion_engine.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How the AI works

1. OpenCV captures frames from the webcam.
2. DeepFace analyzes facial emotion.
3. The emotion is smoothed over several predictions.
4. The adaptation engine maps emotion to a difficulty profile.
5. Pygame changes target speed and spawn rate.
6. If the webcam is unavailable, Demo Mode cycles through emotions.

## Academic note

Facial-expression recognition is probabilistic and should not be treated as a definitive measurement of a person's actual internal emotional state. This project is intended as an educational prototype.

## GitHub

Create a GitHub repository and upload these files. A typical workflow is:

```bash
git init
git add .
git commit -m "Initial emotion adaptive game"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
