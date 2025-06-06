# timer-service/models.py

import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0.0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            return "Timer started."
        return "Timer already running."

    def pause(self):
        if self.running:
            self.elapsed += time.time() - self.start_time
            self.running = False
            return "Timer paused."
        return "Timer is not running."

    def reset(self):
        self.start_time = None
        self.elapsed = 0.0
        self.running = False
        return "Timer reset."

    def status(self):
        current_elapsed = self.elapsed
        if self.running:
            current_elapsed += time.time() - self.start_time
        return {
            "running": self.running,
            "elapsed": round(current_elapsed, 2)
        }
