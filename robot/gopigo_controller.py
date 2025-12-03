"""
gopigo_controller.py
Low-level wrapper around the GoPiGo3 / EasyGoPiGo3 API.
All movement commands should go through this file.
"""

import time

try:
    import easygopigo3  # Official Dexter / GoPiGo3 library
except ImportError:
    easygopigo3 = None
    print("[WARN] easygopigo3 not found. GoPiGoController will run in MOCK mode.")


class GoPiGoController:
    def __init__(self):
        if easygopigo3 is not None:
            self.bot = easygopigo3.EasyGoPiGo3()
            self.mock = False
        else:
            self.bot = None
            self.mock = True

        self.default_speed = 200

    # ---------- Motor configuration ----------

    def set_speed(self, speed: int):
        if self.mock:
            print(f"[MOCK] set_speed({speed})")
            return
        self.bot.set_speed(speed)

    # ---------- Simple movement helpers ----------

    def forward(self, seconds: float = None):
        if self.mock:
            print(f"[MOCK] forward({seconds})")
        else:
            self.bot.set_speed(self.default_speed)
            self.bot.forward()

        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, seconds: float = None):
        if self.mock:
            print(f"[MOCK] backward({seconds})")
        else:
            self.bot.set_speed(self.default_speed)
            self.bot.backward()

        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def left(self, degrees: int = 90):
        if self.mock:
            print(f"[MOCK] left({degrees})")
            return
        self.bot.turn_degrees(-degrees)

    def right(self, degrees: int = 90):
        if self.mock:
            print(f"[MOCK] right({degrees})")
            return
        self.bot.turn_degrees(degrees)

    def stop(self):
        if self.mock:
            print("[MOCK] stop() ")
            return
        self.bot.stop()

    # ---------- Encoder helpers (optional) ----------

    def read_encoders(self):
        if self.mock:
            print("[MOCK] read_encoders()")
            return 0, 0
        return self.bot.read_encoders()

    def reset_encoders(self):
        if self.mock:
            print("[MOCK] reset_encoders()")
            return
        self.bot.reset_encoders()
