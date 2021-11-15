import vlc
from snoozer_stopper import SnoozerStoper
import time


if __name__ == "__main__":
    snoozer_stopper = SnoozerStoper(snooze_time=600)
    snoozer_stopper.start()
    player = vlc.MediaPlayer("http://icecast.vrtcdn.be/stubru_tgs.aac")  # StuBru
    player.play()

    while not snoozer_stopper.stop_pressed():
        time.sleep(0.2)

    player.stop()
    snoozer_stopper.join()
    print("Main says bye")

