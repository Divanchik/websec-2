from datetime import datetime
from time import sleep
import re
from typing import Any
from flask import Flask, request, render_template
from json import load
import os
app = Flask(__name__)
last_request_date = datetime.now()
group_pattern = r"\d{4}(?:[- ]\d{6}D?)?"
staff_pattern = r"(?: *[а-яА-ЯёЁ]+){1,3}"
def search(req: str):
    groupreq = re.findall(group_pattern, req)
    staffreq = re.findall(staff_pattern, req)
    print(groupreq, staffreq, "found matches")
    info: dict
    searchstr: str
    if len(groupreq) > 0:
        searchstr = groupreq[0]
        with open("schedule_groups.json") as f:
            info = load(f)
    elif len(staffreq) > 0:
        searchstr = staffreq[0]
        with open("schedule_staff.json") as f:
            info = load(f)
    else:
        print("No match for group or staff pattern!")
        return False
    for k, i in info.items():
        if k.find(searchstr) >= 0 or k.find(searchstr) >= 0:
            os.system(f"python3 connect.py {i}")
            return k
    return False

@app.route("/")
def main():
    sreq = request.args.getlist("SearchRequest")
    request_date_diff = datetime.now() - last_request_date
    if len(sreq) == 0:
        return render_template('index.html')
    ans = search(sreq[0])
    sleep(2)
    if ans == False:
        print("Unable to find requested schedule!")
        return render_template('index.html')
    with open("group_schedule.json", encoding='utf-8') as f:
        info: dict = load(f)
    if len(info) == 0:
        print("No schedule or not implemented error!")
        return render_template('index.html')
    return render_template('group_temp.html', dates=info[0], info=info[1], title=ans)
    # os.system("python3 update_groups.py")
    # os.system("python3 update_staff.py")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)