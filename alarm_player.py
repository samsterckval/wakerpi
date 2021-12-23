from threading import Thread, Event
import vlc
import time
import math
from typing import Callable


def init_and_play() -> Callable:
    player = AlarmPlayer("http://icecast.vrtcdn.be/stubru.aac")
    player.start()
    return player.stop


class AlarmPlayer(Thread):

    def __init__(self,
                 media: str,
                 backup_media: str = "data/creativeminds.mp3",
                 start_volume: int = 20,
                 max_volume: int = 100,
                 upbeat: int = 30,
                 refesh_rate: int = 5):
        """

        :param media: media to play
        :param backup_media: backup media, used if media errors out
        :param start_volume: volume to hit exactly 60s after trigger
        :param upbeat: seconds to reach start volume
        :param refesh_rate: refresh rate of the loop
        """
        Thread.__init__(self)
        self._media: str = media
        self._backup_media: str = backup_media
        self._player: vlc.MediaPlayer = vlc.MediaPlayer()
        self._media: vlc.Media = vlc.Media(media)
        self._volume: int = 0
        self._start_volume: int = start_volume
        self._max_volume: int = max_volume
        self._player.audio_set_volume(self._volume)
        self._player.set_media(self._media)
        self._upbeat: int = upbeat
        self._tick_length: float = 1/refesh_rate
        self._vol_per_tick: float = self._start_volume/self._upbeat * self._tick_length
        self._stop: Event = Event()

    def run(self) -> None:
        """
        Start this thread 60s before the alarm should go off
        :return:
        """

        target = time.time() + 60

        self._player.play()

        print("Alarm trying to buffer, let's see if it works")

        fails = 0
        succes = False

        while not self._stop.is_set() and fails < 4 and not succes:
            fails += 1
            timeout = time.time() + 5

            while not self._stop.is_set() and time.time() < timeout:
                state = self._player.get_state()

                if state == vlc.State.Playing:
                    print(f"Playback on media {self._player.get_media()} started.")
                    succes = True
                    break
                elif state == vlc.State.Opening:
                    print("Alarm still opening")
                    self._stop.wait(0.5)
                    continue
                elif state == vlc.State.Ended:
                    print(f"State = Ended; Probably an error occured in media {self._player.get_media()}, {'retrying' if fails < 4 else 'going to backup song'}")
                    break
                elif state == vlc.State.Buffering:
                    print("Buffering")
                    self._stop.wait(0.5)
                    continue
                elif state == vlc.State.Error:
                    print(f"State = Error; Probably an error occured in media {self._player.get_media()}, {'retrying' if fails < 4 else 'going to backup song'}")
                    break

            if not succes:
                self._player = vlc.MediaPlayer()
                self._player.audio_set_volume(self._volume)
                self._player.set_media(self._media)
                self._player.play()

        if not succes:
            print("Loading backup song")
            self._player = vlc.MediaPlayer(self._backup_media)
            self._player.audio_set_volume(self._volume)
            self._stop.wait(0.05)
            self._player.play()
            self._stop.wait(0.5)

        tsleep = target - time.time() - self._upbeat
        print(f"Alarm sleeping {tsleep} seconds.")
        if tsleep > 0:
            self._stop.wait(tsleep)

        print("Rise and shine!")

        while not self._stop.is_set():
            self._stop.wait(self._tick_length)
            if self._volume < self._max_volume:
                self._volume += self._vol_per_tick
            self._player.audio_set_volume(math.floor(self._volume))

        self._player.stop()
        del self._player
        print("Alarm says bye.")

    def stop(self):
        self._stop.set()
