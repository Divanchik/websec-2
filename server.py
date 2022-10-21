from datetime import datetime
import re
from flask import Flask, request, render_template, redirect
from json import load
import os
from sys import platform
app = Flask(__name__)
last_request_date = datetime.now()
group_pattern = r"\d{4}(?:[- ]\d{6}D?)?"
staff_pattern = r"(?: *[а-яА-ЯёЁ]+){1,3}"


def search(req: str):
    groupreq = re.findall(group_pattern, req)
    staffreq = re.findall(staff_pattern, req)
    print(groupreq, staffreq, "found matches")

    if len(groupreq) > 0: # if group requested
        with open("data_groups.json", encoding='utf-8') as f:
            info = load(f)
        for fac in info.values():
            for gn, gi in fac['groups'].items():
                if gn.find(groupreq[0]) >= 0:
                    return f"?groupId={gi}"
    
    elif len(staffreq) > 0: # if staff requested
        with open("data_staff.json", encoding='utf-8') as f:
            info = load(f)
        for sn, si in info.items():
            if re.search(f"{staffreq[0].strip()} |{staffreq[0].strip()}$", sn) is not None:
                return f"?staffId={si}"
    
    print("No match for group or staff pattern!")
    return None


@app.route("/grouplist") # Справочник групп
def get_grouplist():
    print(request.args.keys())
    facreq = request.args.getlist("facultyId")
    with open("data_groups.json", encoding='utf-8') as f: info = load(f)
    if len(facreq) == 0: return render_template('grouplist_temp.html', faculties=info)

    for title, fac in info.items():
        if fac['id'] == facreq[0]:     
            return render_template('groups_temp.html', title=title, groups=fac['groups'])
    
    return redirect("/grouplist", 404)
    

@app.route("/schedule") # Расписание
def get_schedule():
    arguments = list(request.args.keys())
    for i in arguments:
        if re.fullmatch("staffId|groupId|selectedWeek", i) == None:
            return redirect("/")

    id_type = list(request.args.keys())[0]
    id_val = request.args.getlist(id_type)[0]
    weekreq = request.args.getlist("selectedWeek")
    if len(weekreq) == 0:
        if platform == "linux":
            os.system(f"python3 schedule.py https://ssau.ru/rasp?{id_type}={id_val}")
        elif platform == "win32":
            os.system(f"python schedule.py https://ssau.ru/rasp?{id_type}={id_val}")
    else:
        if platform == "linux":
            os.system(f"python3 schedule.py \"https://ssau.ru/rasp?{id_type}={id_val}&selectedWeek={weekreq[0]}\"")
        elif platform == "win32":
            os.system(f"python schedule.py \"https://ssau.ru/rasp?{id_type}={id_val}&selectedWeek={weekreq[0]}\"")
    with open("schedule.json", encoding='utf-8') as f: info = load(f)

    if len(info) == 0:
        print("No schedule or not implemented error!")
        return render_template('index.html')
    return render_template('schedule_temp.html', info=info, id_type=id_type, id_val=id_val)
        
    
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