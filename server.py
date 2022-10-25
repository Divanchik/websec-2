from datetime import datetime
import re
from flask import Flask, request, render_template, redirect
from json import load
import os
from sys import platform
app = Flask(__name__)
last_request_date = datetime.now()
group_pattern = r"\d{4}(?:[- ]\d{6}D?)?"


def staff_search(req: str):
    req = req.strip()
    info = {}
    found = {}
    with open("data_staff.json", encoding='utf-8') as f: info = load(f)
    for name, id in info.items():
        if re.search(f"{req} |{req}$", name, flags=re.IGNORECASE) is not None:
            found[name] = id
    return found


def group_search(req: str):
    req = req.strip()
    info = {}
    found = {}
    with open("data_groups.json", encoding='utf-8') as f: info = load(f)
    for facname in info.keys():
        for title, id in info[facname]['groups'].items():
            if title.find(req) >= 0:
                found['title'] = id
    return found


def search(req: str):
    groupreq = re.findall(group_pattern, req)

    if len(groupreq) > 0: # if group requested
        found = group_search(req)
    else:
        found = staff_search(req)
    if len(found.values()) == 0: return None, None
    print(f"[search] found {len(found.values())} entries")

    if len(groupreq) > 0:
        return "?groupId=", found
    return "?staffId=", found


@app.route("/grouplist") # Справочник групп
def get_grouplist():
    print(request.args.keys())
    facreq = request.args.getlist("facultyId")
    with open("data_groups.json", encoding='utf-8') as f: info = load(f)
    if len(facreq) == 0: return render_template('faculties_temp.html', faculties=info)

    for title, fac in info.items():
        if fac['id'] == facreq[0]:     
            return render_template('groups_temp.html', title=title, groups=fac['groups'])
    
    return redirect("/grouplist", 404)
    

@app.route("/schedule") # Расписание
def get_schedule():
    # search incorrect arguments
    arguments = list(request.args.keys())
    for i in arguments:
        if re.fullmatch("staffId|groupId|selectedWeek|selectedWeekday", i) == None:
            return redirect("/", 400)

    id_type = list(request.args.keys())[0]
    id_val = request.args.getlist(id_type)[0]
    week = request.args.getlist("selectedWeek")
    weekday = request.args.getlist("selectedWeekday")
    option_week = "" if len(week) == 0 else f"&selectedWeek={week[0]}"
    option_day = "" if len(weekday) == 0 else f"&selectedWeekday={weekday[0]}"
    py_com = "python3" if platform == "linux" else "python"
    os.system(f"{py_com} schedule.py \"https://ssau.ru/rasp?{id_type}={id_val}{option_week}{option_day}\"")
    with open("schedule.json", encoding='utf-8') as f: info = load(f)

    if len(info) == 0:
        print("No schedule or not implemented error!")
        return render_template('index.html')
    return render_template('schedule_temp.html', info=info, id_type=id_type, id_val=id_val)
        
    
@app.route("/") # Поисковая страница
def main():
    sreq = request.args.getlist("SearchRequest")
    if len(sreq) == 0: return render_template('index.html')
    print(f"[/] search request ({sreq[0]})")
    link_type, found = search(sreq[0])

    if link_type == None:
        print("Unable to find requested schedule!")
        return render_template('index.html')
    elif len(found.values()) == 1:
        for i in found.values():
            return redirect(f"/schedule{link_type}{i}")
    return render_template("entries_temp.html", link_type=link_type, found=found)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
