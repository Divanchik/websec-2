from cmath import inf
from datetime import datetime
from flask import Flask, request, render_template
from runpy import run_path
from json import load
app = Flask(__name__)
last_request_date = datetime.now()
def update_info():
    run_path("update_groups.py")
    run_path("update_staff.py")

@app.route("/")
def main():
    with open("group_schedule.json") as f:
        info: dict = load(f)
    reqId = request.args.getlist("Id")
    request_date_diff = datetime.now() - last_request_date
    return render_template('group_temp.html', dates=info[0], info=info[1], title="Расписание, 6312-100503D")
    # if len(reqId) == 0:
    #     return render_template('index.html')
    # return render_template('group_temp.html', title='test title', header='test header')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)