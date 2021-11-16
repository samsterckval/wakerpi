from threading import Thread
import sys
from typing import Dict, Callable
import time

if "darwin" in sys.platform:
    from pynput import keyboard
elif "linux" in sys.platform:
    import os


def str_to_bool(s) -> bool:
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError("{s} is not a bool")


class SnoozerStoper(Thread):
    SNOOZE_BTN_FACTORY: Dict[str, str] = {"darwin": "<shift>+e",
                                          "linux": "<shift>+e"}
    STOP_BTN_FACTORY: Dict[str, str] = {"darwin": "<shift>+w",
                                        "linux": "<shift>+w"}

    if "linux" in sys.platform:
        PATH_TO_TMP = f"/run/user/{os.getuid()}/wakerpi/"
        PATH_TO_SNOOZE = os.path.join(PATH_TO_TMP, "snooze")
        PATH_TO_STOP = os.path.join(PATH_TO_TMP, "stop")

    def __init__(self, snooze_time: int):
        Thread.__init__(self)
        self.snooze_time: int = snooze_time
        self.snoozed: bool = False
        self.stopped: bool = False
        if "darwin" in sys.platform:
            self.hotkey_dict: Dict[str, Callable] = {self.SNOOZE_BTN_FACTORY[sys.platform]: self._snooze,
                                                     self.STOP_BTN_FACTORY[sys.platform]: self._stop}
            self.listener: keyboard.GlobalHotKeys = keyboard.GlobalHotKeys(self.hotkey_dict)

        elif "linux" in sys.platform:

            if not os.path.exists(self.PATH_TO_TMP):
                os.makedirs(self.PATH_TO_TMP)
                print(f"Created run directory @ {self.PATH_TO_TMP}")

            with open(self.PATH_TO_SNOOZE, "w+") as f:
                f.write("False")
                f.close()

            with open(self.PATH_TO_STOP, "w+") as f:
                f.write("False")
                f.close()

    def snooze_pressed(self) -> bool:
        return self.snoozed

    def stop_pressed(self) -> bool:
        return self.stopped

    def reset_stop(self):
        with open(self.PATH_TO_STOP, "w+") as f:
            f.write("False")
            f.close()

    def reset_snooze(self):
        with open(self.PATH_TO_SNOOZE, "w+") as f:
            f.write("False")
            f.close()

    def _snooze(self) -> None:
        print("Snooze pressed")
        self.snoozed = True

    def _stop(self) -> None:
        print("Stop pressed")
        self.stopped = True

    def read_snooze(self):
        with open(self.PATH_TO_SNOOZE, "r") as f:
            snz = f.readline()
            f.close()
            self.snoozed = str_to_bool(snz)

    def read_stop(self):
        with open(self.PATH_TO_STOP, "r") as f:
            snz = f.readline()
            f.close()
            self.stopped = str_to_bool(snz)

    def run(self) -> None:
        if "darwin" in sys.platform:
            for key, func in self.hotkey_dict.items():
                print(f"Press {key} to {str.strip(func.__name__, '_')}")

            self.listener.start()

            while not self.stop_pressed():
                time.sleep(0.2)

            self.listener.stop()
            self.listener.join()

        elif "linux" in sys.platform:
            while not self.stop_pressed():
                time.sleep(0.2)
                self.read_snooze()
                self.read_stop()

        print("Input thread quitting.")
