import vlc
from snoozer_stopper import SnoozerStoper
import time

VOL_PER_SEC = 2
VOL_START = 20

if __name__ == "__main__":
    snoozer_stopper = SnoozerStoper(snooze_time=600)
    snoozer_stopper.start()
    vol = VOL_START
    player = vlc.MediaPlayer("http://icecast.vrtcdn.be/stubru.aac")  # StuBru
    player.audio_set_volume(vol)
    player.play()

    while not player.get_state() == vlc.State(3):
        time.sleep(0.5)
        print(f"State is currently : {player.get_state()}")
        if player.get_state() == vlc.State(6):
            print("something went wrong")
            break

    interval = time.time()

    while not snoozer_stopper.stop_pressed():
        time.sleep(0.2)
        if time.time() > interval+0.2:
            if vol < 200:
                vol += VOL_PER_SEC
            interval = time.time()
            player.audio_set_volume(vol)
            print(f"vol is now {player.audio_get_volume()}")

    player.stop()
    snoozer_stopper.join()
    print("Main says bye")

