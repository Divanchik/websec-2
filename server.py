from datetime import datetime
import re
from flask import Flask, request, render_template, redirect
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

    if len(groupreq) > 0: # if group requested
        with open("data_groups.json") as f:
            info = load(f)
        for fac in info.values():
            for gn, gi in fac['groups'].items():
                if gn.find(groupreq[0]) >= 0:
                    return f"?groupId={gi}"
    
    elif len(staffreq) > 0: # if staff requested
        with open("data_staff.json") as f:
            info = load(f)
        for sn, si in info.items():
            if sn.find(staffreq[0]) >= 0:
                return f"?staffId={si}"
    
    print("No match for group or staff pattern!")
    return None

@app.route("/grouplist") # Справочник групп
def get_grouplist():
    facreq = request.args.getlist("facultyId")
    with open("data_groups.json") as f:
        info = load(f)
    if len(facreq) == 0:
        return render_template('grouplist_temp.html', faculties=info)
    for title, fac in info.items():
        if fac['id'] == facreq[0]:     
            return render_template('groups_temp.html', title=title, groups=fac['groups'])
    

@app.route("/schedule") # Расписание
def get_schedule():
    schedreq = [request.args.getlist("groupId"), request.args.getlist("staffId")]
    res_id: str
    if len(schedreq[0]) != 0: # if group requested
        res_id = schedreq[0][0]
        os.system(f"python3 connect.py https://ssau.ru/rasp?groupId={res_id}")
        with open("data_groups.json") as f:
            info = load(f)
        for k, v in info.items():
            for gn, gi in v['groups'].items():
                if gi == res_id:
                    ans = gn
        with open("group_schedule.json", encoding='utf-8') as f:
            info: dict = load(f)
        if len(info) == 0:
            print("No schedule or not implemented error!")
            return render_template('index.html')
        return render_template('group_temp.html', dates=info[0], info=info[1], title=ans)

    elif len(schedreq[1]) != 0: # if staff requested
        res_id = schedreq[1][0]
        os.system(f"python3 connect.py https://ssau.ru/rasp?staffId={res_id}")
        with open("data_staff.json") as f:
            info = load(f)
        for sn, si in info.items():
            if si == res_id:
                ans = sn
        with open("group_schedule.json", encoding='utf-8') as f:
            info: dict = load(f)
        if len(info) == 0:
            print("No schedule or not implemented error!")
            return render_template('index.html')
        return render_template('group_temp.html', dates=info[0], info=info[1], title=ans)
        
    

@app.route("/") # Поисковая страница
def main():
    sreq = request.args.getlist("SearchRequest")
    if len(sreq) == 0: return render_template('index.html')

    res_id = search(sreq[0])
    
    if res_id == None:
        print("Unable to find requested schedule!")
        return render_template('index.html')
    return redirect(f"/schedule{res_id}")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)