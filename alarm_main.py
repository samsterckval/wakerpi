from snoozer_stopper import SnoozerStoper
from alarm_player import AlarmPlayer
import time
import datetime
import sys
import os

now = datetime.datetime.now()

if "linux" in sys.platform:
    wakeup_time = datetime.datetime.combine(now.date(), datetime.time(hour=7, minute=20, second=0, microsecond=0))
    if (wakeup_time-now).days < 0:
        wakeup_time += datetime.timedelta(days=abs((wakeup_time-now).days))
else:
    wakeup_time = now + datetime.timedelta(minutes=1)

print(f"setting time for {wakeup_time}")

if __name__ == "__main__":
    if datetime.date.today().weekday() >= 5:  # then it's a weekend, no wakeup then yet, since this is a test phase
        exit()

    while wakeup_time - datetime.datetime.now() > datetime.timedelta(0, 60):
        print(wakeup_time - datetime.datetime.now())
        time.sleep(1)

    print("Let's start the Alarm")

    alarm_player = AlarmPlayer("http://icecast.vrtcdn.be/stubru.aac")
    alarm_player.start()

    snoozer_stopper = SnoozerStoper(snooze_time=600)
    snoozer_stopper.start()

    while not snoozer_stopper.stop_pressed():
        time.sleep(0.5)

    alarm_player.stop()
    snoozer_stopper.join()
    print("Main says bye")

    print("Alarm will restart")
    os.execv(sys.executable, ['python3'] + sys.argv)

