from threading import Thread, Event
from datetime import datetime, timedelta, time
import time as tm
from typing import List, Callable
from alarm_player import AlarmPlayer
import calendar


def dummy_stop() -> None:
    print("Dummy stop called")


def dummy_alarm_print() -> AlarmPlayer:
    print("Dummy alarm is going off!")

    tmp = AlarmPlayer("tmp")
    return tmp


class Alarm(Thread):

    def __init__(self, stop_event: Event = None):
        Thread.__init__(self, name="WakerPiAlarmThread")
        self._target_time: time = datetime.now().time()
        self._on_days: List[int] = []
        self._wake_signal: Event = Event()
        if stop_event is None:
            stop_event = Event()
        self._stop_event = stop_event
        self.play_alarm_callback: Callable = dummy_alarm_print
        self.stop_alarm_callback: Callable = dummy_stop
        self.player: AlarmPlayer = dummy_alarm_print()

    def stop_alarm(self) -> None:
        if self.player is not None:
            print("stopping player")
            self.player.stop()
            self._stop_event.set()
            self._wake_signal.set()
        else:
            print("player unknown")
            self.stop_alarm_callback()

    def get_next_alarm(self) -> datetime:
        """
        Get the datetime object for the next alarm
        :return: Next alarm as datetime
        """

        next_target = datetime.now()
        next_target = next_target.replace(hour=self._target_time.hour,
                                          minute=self._target_time.minute,
                                          second=self._target_time.second,
                                          microsecond=self._target_time.microsecond)

        # Is the alarm today?
        if datetime.now().time() > self._target_time:

            # If it is, add a day until we have the next "on-day"
            for i in range(7):
                next_target = next_target + timedelta(days=1)
                if next_target.weekday() in self._on_days:
                    break

        if len(self._on_days) == 0:
            next_target = next_target + timedelta(days=99)

        return next_target

    def get_next_alarm_str(self) -> str:
        """
        Get next alarm as string
        :return: str
        """

        return self.get_next_alarm().strftime("%Y-%m-%d %H:%M:%S")

    def stop(self) -> None:
        """
        Attempt to stop the thread
        :return: None
        """
        self._stop_event.set()
        self._wake_signal.set()

    def get_next_alarm_delta(self) -> timedelta:
        """
        Get the timedelta to next alarm
        :return: timedelta
        """

        delta: timedelta = self.get_next_alarm() - datetime.now()

        # print(f"got alarm delta - {delta}")

        return delta

    def get_alarm_time(self) -> time:
        """
        get a time object with alarm time
        :return: datetime.time
        """

        return self._target_time

    def get_alarm_time_str(self) -> str:
        """
        Get alarm time as string
        :return: str
        """

        return self._target_time.strftime("%H:%M:%S")

    def set_alarm_time(self, alarm: datetime) -> None:
        """
        Set a new alarm time.  Date part of it will be ignored
        :param alarm: datetime object
        :return: None
        """

        self._target_time = alarm.time()
        print(f"Set alarm time to : {self._target_time}")

        # Wake the thread so the sleep time can be updated
        self._wake_signal.set()

    def get_on_days(self) -> List[int]:
        """
        Get the on_days list
        :return: List[int]
        """

        return self._on_days

    def set_on_days(self, on_days: List[int]) -> None:
        """
        Example : [0, 1, 2, 3, 4] for workdays
        :param on_days: list with weekday ints that alarm is on
        :return: None
        """

        # first check if we aren't trying to use days that don't exist
        on_days_checked = []
        for v in on_days:
            if v <= 6:
                on_days_checked.append(v)

        # Sort it small to big
        on_days_checked.sort()

        # Store it
        self._on_days = on_days_checked
        print(f"Set alarm days to : {', '.join(map(str, [calendar.day_name[i] for i in self._on_days]))}")

        # Wake the thread so that the sleep time can be updated
        self._wake_signal.set()

    def run(self) -> None:

        while not self._stop_event.is_set():

            # Get the delta, and sleep until the alarm should go off
            delta = self.get_next_alarm_delta()
            print(f"Delta to next alarm : {delta}")
            self._wake_signal.wait(timeout=int(delta.total_seconds()-60))
            self._wake_signal.clear()

            # Get the delta after waking up
            delta = self.get_next_alarm_delta()
            print(f"Delta to next alarm : {delta}")
            if delta.total_seconds() < 60:

                # Play the alarm
                self.player = self.play_alarm_callback()
                # self.stop_alarm_callback = self.play_alarm_callback()

                if self._stop_event.is_set():
                    break

                self._wake_signal.wait(timeout=65)
                continue

            else:
                tm.sleep(0.5)

        print("Alarm Thread going down, bye!")
