import math
import random
import pygame


EMOTION_SETTINGS = {
    "happy": {
        "difficulty": "HARD",
        "target_speed": 7.5,
        "spawn_interval": 0.75,
        "lives": 3,
        "message": "You're doing great! Challenge increased."
    },
    "neutral": {
        "difficulty": "NORMAL",
        "target_speed": 5.0,
        "spawn_interval": 1.05,
        "lives": 3,
        "message": "Normal adaptive difficulty."
    },
    "sad": {
        "difficulty": "EASY",
        "target_speed": 3.2,
        "spawn_interval": 1.55,
        "lives": 5,
        "message": "Difficulty reduced to support the player."
    },
    "angry": {
        "difficulty": "EASY",
        "target_speed": 3.5,
        "spawn_interval": 1.45,
        "lives": 5,
        "message": "Difficulty reduced to keep the game comfortable."
    },
    "fear": {
        "difficulty": "EASY",
        "target_speed": 3.0,
        "spawn_interval": 1.65,
        "lives": 5,
        "message": "Fewer/faster-to-handle challenges."
    },
    "surprise": {
        "difficulty": "HARD",
        "target_speed": 7.0,
        "spawn_interval": 0.8,
        "lives": 3,
        "message": "Surprise detected! Challenge increased."
    },
    "disgust": {
        "difficulty": "NORMAL",
        "target_speed": 5.0,
        "spawn_interval": 1.05,
        "lives": 3,
        "message": "Normal adaptive difficulty."
    },
}

WIDTH, HEIGHT = 1000, 650
PLAY_WIDTH = 700
FPS = 60


class Target:
    def __init__(self, speed):
        self.size = 30
        self.x = random.randint(10, PLAY_WIDTH - self.size - 10)
        self.y = -self.size
        self.speed = speed

    @property
    def rect(self):
        return pygame.Rect(self.x, int(self.y), self.size, self.size)

    def update(self):
        self.y += self.speed


class EmotionAdaptiveGame:
    def __init__(self, emotion_engine):
        pygame.init()
        pygame.display.set_caption("Emotion Adaptive Game - AI Demo")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 30)
        self.big_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 24)

        self.engine = emotion_engine
        self.running = True
        self.score = 0
        self.misses = 0
        self.emotion = "neutral"
        self.last_emotion = "neutral"
        self.targets = []
        self.spawn_timer = 0.0
        self.start_time = pygame.time.get_ticks()
        self.last_status = ""
        self.demo_emotions = ["neutral", "happy", "neutral", "sad"]
        self.demo_index = 0
        self.next_demo_change = pygame.time.get_ticks() + 7000

        self.player = pygame.Rect(325, HEIGHT - 75, 50, 40)

    def settings(self):
        return EMOTION_SETTINGS.get(self.emotion, EMOTION_SETTINGS["neutral"])

    def _demo_emotion(self):
        now = pygame.time.get_ticks()
        if now >= self.next_demo_change:
            self.demo_index = (self.demo_index + 1) % len(self.demo_emotions)
            self.next_demo_change = now + 7000
        return self.demo_emotions[self.demo_index]

    def update_emotion(self):
        emotion, frame, status = self.engine.update()

        if frame is None:
            # Allows the project to be demonstrated even when webcam access
            # is unavailable on the development laptop.
            emotion = self._demo_emotion()
            status = "DEMO MODE - webcam unavailable"

        if emotion != self.last_emotion:
            self.last_emotion = emotion
            self.last_status = EMOTION_SETTINGS.get(
                emotion, EMOTION_SETTINGS["neutral"]
            )["message"]
            # Rebalance active targets immediately when emotion changes.
            for target in self.targets:
                target.speed = self.settings()["target_speed"]

        self.emotion = emotion
        return frame, status

    def spawn_target(self):
        if len(self.targets) < 8:
            self.targets.append(Target(self.settings()["target_speed"]))

    def draw_text(self, text, x, y, font=None):
        surface = (font or self.font).render(text, True, (240, 240, 240))
        self.screen.blit(surface, (x, y))

    def draw(self, status):
        self.screen.fill((22, 24, 30))

        # Play area
        pygame.draw.rect(self.screen, (35, 38, 48), (0, 0, PLAY_WIDTH, HEIGHT))
        pygame.draw.line(self.screen, (90, 95, 110), (PLAY_WIDTH, 0), (PLAY_WIDTH, HEIGHT), 2)

        # Player
        pygame.draw.rect(self.screen, (70, 160, 255), self.player, border_radius=8)

        # Targets
        for target in self.targets:
            pygame.draw.circle(
                self.screen,
                (255, 215, 70),
                (int(target.x + target.size / 2), int(target.y + target.size / 2)),
                target.size // 2,
            )

        # HUD
        self.draw_text(f"Score: {self.score}", 20, 18)
        self.draw_text(f"Emotion: {self.emotion.upper()}", 20, 52)
        self.draw_text(f"Difficulty: {self.settings()['difficulty']}", 20, 86)
        self.draw_text(f"Misses: {self.misses}", 20, 120)

        self.draw_text("AI ADAPTATION", PLAY_WIDTH + 25, 25, self.big_font)
        self.draw_text("Emotion changes", PLAY_WIDTH + 25, 85)
        self.draw_text("game difficulty.", PLAY_WIDTH + 25, 112)
        self.draw_text("← / →  Move", PLAY_WIDTH + 25, 175)
        self.draw_text("ESC     Quit", PLAY_WIDTH + 25, 205)
        self.draw_text("Q       Quit", PLAY_WIDTH + 25, 235)

        # Emotion mapping
        y = 290
        for name, label in [
            ("happy", "Happy → Hard"),
            ("neutral", "Neutral → Normal"),
            ("sad", "Sad → Easy"),
            ("angry", "Angry → Easy"),
            ("fear", "Fear → Easy"),
        ]:
            self.draw_text(label, PLAY_WIDTH + 25, y, self.small_font)
            y += 30

        status_text = status[:45]
        self.draw_text(status_text, 20, HEIGHT - 45, self.small_font)

        if self.last_status:
            self.draw_text(self.last_status[:60], 20, HEIGHT - 22, self.small_font)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False

            keys = pygame.key.get_pressed()
            speed = 420 * dt
            if keys[pygame.K_LEFT]:
                self.player.x -= int(speed)
            if keys[pygame.K_RIGHT]:
                self.player.x += int(speed)

            self.player.x = max(0, min(PLAY_WIDTH - self.player.width, self.player.x))

            _, status = self.update_emotion()

            self.spawn_timer += dt
            if self.spawn_timer >= self.settings()["spawn_interval"]:
                self.spawn_timer = 0
                self.spawn_target()

            for target in self.targets[:]:
                target.update()

                if target.rect.colliderect(self.player):
                    self.score += 1
                    self.targets.remove(target)
                elif target.y > HEIGHT:
                    self.misses += 1
                    self.targets.remove(target)

            self.draw(status)

        pygame.quit()
