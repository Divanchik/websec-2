from mywebfunc import *
import re
import json
link1 = "https://ssau.ru/rasp?groupId=531873987"
time1 = time()

line_filters = [
    r"schedule__item(?=(?:_show)? ?\")",
    r"(?<=time-item\">).+?(?=<)",
    r"(?<=head-date\">).*?(?=<)",
    r"(?<=color-type-\d\">).*?(?=<)",
    r"(?<=place\">).*?(?=<)",
    r"(?<=\d\" >).*?(?=<)",
    r"(?<=group\">).*?(?=<)",
    r"Подгруппы: \d"
]
line_filters1 = list(map(lambda x: r"(?:{0})".format(x), line_filters))
lines = re.findall("|".join(line_filters1), get_from(link1))
for i in range(len(lines)): lines[i] = lines[i].strip()
while "" in lines: lines.remove("")


rows = {'dates':[lines[i] for i in range(6)]}
match = re.fullmatch
p_time = r"\d{2}:\d{2}"
p_subj = r"schedule__item(?:_show)?"

i = 6
while i < len(lines):
    if match(p_time, lines[i]):
        rows[lines[i] + " " + lines[i+1]] = []
        i += 2
    elif match(p_subj, lines[i]):
        last_key = list(rows.keys())[len(rows.keys())-1]
        rows[last_key].append("")
        i += 1
    else:
        last_key = list(rows.keys())[len(rows.keys())-1]
        last_ind = len(rows[last_key])-1
        rows[last_key][last_ind] += lines[i] + ";"
        i += 1

if int(input("dump? (1/0): ")) == 1:
    with open("group_schedule.json", "w") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)
