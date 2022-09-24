import requests
import re
import json
from time import time
link1 = "https://ssau.ru/rasp?groupId=531873998&selectedWeek=4&selectedWeekday=1"
time1 = time()


responce = requests.get(link1)
filter_string = r"(?:schedule__item (?:schedule__item_show)?\".*)|(?:time-item.*?</)|(?:schedule__head-date.*?</)|(?:discipline.*?</)|(?:schedule__place.*?</)|(?:href=\"/rasp\?staffId=\d+\".*?</)|(?:schedule__group.*?</)"
lines = re.findall(filter_string, responce.text)


match = re.fullmatch
p_time = r"\d{2}:\d{2}"
p_subj = r"subject"
info = []


for line in lines:
    print(line)
    tmp = '<' + line + '>'
    if tmp.find('schedule__item') < 0:
        tmp = re.sub("<.*?>", "", tmp).strip()
        if len(tmp) > 0: info.append(tmp)
    else:
        info.append("subject")
rows = {'dates':[info[i] for i in range(6)]}


i = 6
while i < len(info):
    if match(p_time, info[i]):
        rows[info[i] + " " + info[i+1]] = []
        i += 2
    elif match(p_subj, info[i]):
        last_key = list(rows.keys())[len(rows.keys())-1]
        rows[last_key].append("")
        i += 1
    else:
        last_key = list(rows.keys())[len(rows.keys())-1]
        last_ind = len(rows[last_key])-1
        rows[last_key][last_ind] += info[i] + ";"
        i += 1

print("time passed:", round(time() - time1, 3), "sec")
if int(input("dump? (1/0): ")) == 1:
    with open("rows.json", "w") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)

