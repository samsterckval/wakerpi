from flask import Flask, render_template, request
import os, sys


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
                with open(PATH_TO_SNOOZE, "w+") as f:
                    f.write("True")
                    f.truncate()
                    f.close()
        else:
            print("unknown thing")
    elif request.method == 'GET':
        return render_template('main.html')

    return render_template("main.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)