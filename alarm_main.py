from snoozer_stopper import SnoozerStoper
from alarm_player import AlarmPlayer
from alarm import Alarm
import time
import datetime
import sys
import os
from threading import Event

now = datetime.datetime.now()

if "linux" in sys.platform:
    wakeup_time = datetime.datetime.combine(now.date(), datetime.time(hour=7, minute=20, second=0, microsecond=0))
    if (wakeup_time-now).days < 0:
        wakeup_time += datetime.timedelta(days=abs((wakeup_time-now).days))
else:
    wakeup_time = now + datetime.timedelta(minutes=1)

print(f"setting time for {wakeup_time}")

if __name__ == "__main__":

    stop_event = Event()

    alarm_player = AlarmPlayer("http://icecast.vrtcdn.be/stubru.aac")

    alarm = Alarm(stop_event=stop_event)
    alarm.play_alarm_callback = alarm_player.start
    alarm.set_on_days([0, 1, 2, 3, 4])
    alarm.set_alarm_time(datetime.datetime.combine(datetime.datetime.now().date(),
                                                   datetime.time(hour=7, minute=20, second=0, microsecond=0)))
    # alarm.set_alarm_time(datetime.datetime.now() + datetime.timedelta(seconds=70))
    alarm.start()

    while not stop_event.is_set():

        snoozer_stopper = SnoozerStoper(snooze_time=600)
        snoozer_stopper.start()

        while not snoozer_stopper.stop_pressed():
            time.sleep(1)
        alarm_player.stop()
        snoozer_stopper.join()

    print("Main says bye")

    print("Alarm will restart")
    os.execv(sys.executable, ['python3'] + sys.argv)

