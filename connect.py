import argparse
from mywebfunc import *
import re
import json

parser = argparse.ArgumentParser(description='Get schedule.')
parser.add_argument("dest", type=str)
parser.add_argument("id", type=str)
args = parser.parse_args()
link1 = f"https://ssau.ru/rasp?{args.dest}Id={args.id}"
print(link1)

line_filters = [
    r".*schedule__item[^s].*",
    r".*time-item.*",
    r".*head-date.*",
    r".*schedule__discipline.*",
    r".*schedule__place.*",
    r".*staffId.*",
    r".*schedule__group\".*",
    r"Подгруппы: \d"
]

raw = re.sub(r".*schedule__head\".*", "", get_from(link1))
line_filters1 = list(map(lambda x: f"(?:{x})", line_filters))
lines = re.findall("|".join(line_filters1), raw)
for i in range(len(lines)): lines[i] = lines[i].strip()


for i in range(len(lines)):
    if lines[i].find("Подгруппы") >= 0:
        continue
    elif lines[i].find("schedule__item") < 0:
        lines[i] = re.sub("<.*?>", "", f"<{lines[i]}>").strip()
    else:
        lines[i] = "schedule__item"
while "" in lines: lines.remove("")


# for i in lines:
#     print(i)

dates = [lines[i] for i in range(6)]
rows = {}
match = re.fullmatch
p_time = r"\d{2}:\d{2}"
p_subj = r"schedule__item"

i = 6
while i < len(lines):
    if match(p_time, lines[i]):
        rows[lines[i] + " " + lines[i+1]] = []
        i += 2
    elif match(p_subj, lines[i]):
        last_key = list(rows.keys())[len(rows.keys())-1]
        rows[last_key].append([])
        i += 1
    else:
        last_key = list(rows.keys())[len(rows.keys())-1]
        last_ind = len(rows[last_key])-1
        rows[last_key][last_ind].append(lines[i])
        i += 1 

if int(input("dump? (1/0): ")) == 1:
    with open("group_schedule.json", "w") as f:
        json.dump([dates, rows], f, indent=4, ensure_ascii=False)
