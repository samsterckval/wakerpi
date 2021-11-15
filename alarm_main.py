import vlc
from snoozer_stopper import SnoozerStoper
import time
import datetime
import sys

VOL_PER_SEC = 1
VOL_START = 0
VOL_MAX = 100

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

    while wakeup_time - datetime.datetime.now() > datetime.timedelta(0, 50):
        print(wakeup_time - datetime.datetime.now())
        time.sleep(1)

    print("Let's start the buffering")

    snoozer_stopper = SnoozerStoper(snooze_time=600)
    snoozer_stopper.start()
    vol = VOL_START
    player = vlc.MediaPlayer()  # StuBru
    media = vlc.Media("http://icecast.vrtcdn.be/stubru.aac")
    player.audio_set_volume(vol)
    player.set_media(media)
    player.play()

    while True:
        state = player.get_state()
        if state == vlc.State.Playing:
            print(f"Playback on media {player.get_media()} started.")
            break
        elif state == vlc.State.Opening:
            time.sleep(0.5)
            continue
        elif state == vlc.State.Ended:
            print(f"Probably an error occured in media {player.get_media()}, going to backup song.")
            del player
            player = vlc.MediaPlayer("data/creativeminds.mp3")
            player.audio_set_volume(vol)
            player.play()
            time.sleep(0.5)
            continue
        elif state == vlc.State.Buffering:
            time.sleep(0.5)
            continue
        elif state == vlc.State.Error:
            print(f"An error occured in VLC, loading backup song")
            del player
            player = vlc.MediaPlayer("data/creativeminds.mp3")
            player.audio_set_volume(vol)
            player.play()
            time.sleep(0.5)
            continue

    tsleep = (wakeup_time - datetime.datetime.now()).seconds - 20
    print(f"Sleeping {tsleep} seconds.")
    if tsleep > 0:
        time.sleep(tsleep)

    print("Let's go")

    interval = time.time() + 1

    while not snoozer_stopper.stop_pressed():
        time.sleep(0.2)
        if time.time() > interval:
            if vol < VOL_MAX:
                vol += VOL_PER_SEC
            interval = time.time() + 1
            player.audio_set_volume(vol)

    player.stop()
    snoozer_stopper.join()
    print("Main says bye")

