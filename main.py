import time
from game import EmotionAdaptiveGame
from emotion_engine import EmotionEngine

def main():
    # The game works even without a webcam. If the camera/AI is unavailable,
    # it automatically switches to demo mode so the project can still be shown.
    emotion_engine = EmotionEngine()
    game = EmotionAdaptiveGame(emotion_engine)

    try:
        game.run()
    finally:
        emotion_engine.close()

if __name__ == "__main__":
    main()
