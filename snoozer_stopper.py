from threading import Thread
import sys
from typing import Dict, Callable
from pynput import keyboard
import time


class SnoozerStoper(Thread):
    SNOOZE_BTN_FACTORY: Dict[str, str] = {"darwin": "<shift>+e",
                                          "linux": "<shift>+e"}
    STOP_BTN_FACTORY: Dict[str, str] = {"darwin": "<shift>+w",
                                        "linux": "<shift>+w"}

    def __init__(self, snooze_time: int):
        Thread.__init__(self)
        self.snooze_time: int = snooze_time
        self.snoozed: bool = False
        self.stopped: bool = False
        self.hotkey_dict: Dict[str, Callable] = {self.SNOOZE_BTN_FACTORY[sys.platform]: self._snooze,
                                                 self.STOP_BTN_FACTORY[sys.platform]: self._stop}
        self.listener: keyboard.GlobalHotKeys = keyboard.GlobalHotKeys(self.hotkey_dict)

    def snooze_pressed(self) -> bool:
        return self.snoozed

    def stop_pressed(self) -> bool:
        return self.stopped

    def _snooze(self) -> None:
        print("Snooze pressed")
        self.snoozed = True

    def _stop(self) -> None:
        print("Stop pressed")
        self.stopped = True

    def run(self) -> None:
        for key, func in self.hotkey_dict.items():
            print(f"Press {key} to {str.strip(func.__name__, '_')}")

        self.listener.start()

        while not self.stop_pressed():
            time.sleep(0.2)

        self.listener.stop()
        self.listener.join()

        print("Input thread quitting.")
