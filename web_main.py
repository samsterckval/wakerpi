from flask import Flask, render_template, request
import os
import sys
from threading import Thread, Event
from alarm import Alarm
from alarm_player import init_and_play
import datetime
import calendar


stop_event = Event()

alarm = Alarm(stop_event=stop_event)
alarm.play_alarm_callback = init_and_play
alarm.start()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

PATH_TO_SNOOZE = f"/run/user/{os.getuid()}/wakerpi/snooze"
PATH_TO_STOP = f"/run/user/{os.getuid()}/wakerpi/stop"


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('snooze') == 'SNOOZE':
            if "darwin" in sys.platform:
                print("Snooze")
            else:
                with open(PATH_TO_SNOOZE, "w+") as f:
                    f.write("True")
                    f.truncate()
                    f.close()
        elif request.form.get('stop') == 'STOP':
            if "darwin" in sys.platform:
                print("Stop")
            else:
                alarm.stop()
                # with open(PATH_TO_STOP, "w+") as f:
                #     f.write("True")
                #     f.truncate()
                #     f.close()
        else:
            if request.form.get('set') == 'SET':
                print(request.form)
                on_days = []
                for id, name in enumerate(list(calendar.day_name)):
                    if request.form.get(name) == 'On':
                        on_days.append(id)

                alarm.set_on_days(on_days)

                alarm_time_str = request.form.get('alarmTime')
                if len(alarm_time_str) < 6:
                    alarm.set_alarm_time(alarm=datetime.datetime.strptime(alarm_time_str, '%H:%M'))
                else:
                    alarm.set_alarm_time(alarm=datetime.datetime.strptime(alarm_time_str, '%H:%M:%S'))
            else:
                print("unknown thing")

    return render_template('index.html',
                           delta=alarm.get_next_alarm_str(),
                           on_days=alarm.get_on_days(),
                           day_name=enumerate(list(calendar.day_name)),
                           alarm_time=alarm.get_alarm_time_str())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
