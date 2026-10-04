import time
from collections import Counter, deque

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from deepface import DeepFace
except Exception:
    DeepFace = None


class EmotionEngine:
    """
    Webcam emotion detector.

    The detector is intentionally optional:
    - If OpenCV/DeepFace/camera are unavailable, the game continues in demo mode.
    - Predictions are smoothed over several frames to reduce rapid emotion changes.
    """

    def __init__(self, camera_index=0, analyze_every=1.5, smoothing_window=5):
        self.camera_index = camera_index
        self.analyze_every = analyze_every
        self.last_analysis = 0.0
        self.last_emotion = "neutral"
        self.history = deque(maxlen=smoothing_window)
        self.camera = None
        self.available = False
        self.error = ""

        if cv2 is None:
            self.error = "OpenCV is not installed."
            return

        if DeepFace is None:
            self.error = "DeepFace could not be imported."
            return

        self._open_camera()

    def _open_camera(self):
        try:
            self.camera = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            if not self.camera.isOpened():
                self.camera.release()
                self.camera = cv2.VideoCapture(self.camera_index)

            self.available = bool(self.camera.isOpened())
            if not self.available:
                self.error = "Camera could not be opened. Demo mode is active."
        except Exception as exc:
            self.available = False
            self.error = f"Camera error: {exc}"

    def update(self):
        """
        Returns: (emotion, camera_frame, status_message)
        """
        if not self.available:
            return self.last_emotion, None, self.error

        ok, frame = self.camera.read()
        if not ok:
            self.available = False
            self.error = "Camera frame could not be read. Demo mode is active."
            return self.last_emotion, None, self.error

        now = time.time()
        if now - self.last_analysis >= self.analyze_every:
            try:
                result = DeepFace.analyze(
                    frame,
                    actions=["emotion"],
                    enforce_detection=False,
                    silent=True,
                )
                if isinstance(result, list):
                    result = result[0]

                emotion = str(result.get("dominant_emotion", "neutral")).lower()
                self.history.append(emotion)
                self.last_analysis = now

                if self.history:
                    self.last_emotion = Counter(self.history).most_common(1)[0][0]
            except Exception:
                # Keep the previous stable emotion instead of crashing the game.
                self.last_analysis = now

        return self.last_emotion, frame, "AI camera mode"

    def close(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None
