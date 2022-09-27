from mywebfunc import *
import re
import json

teachers = {}
template = "https://ssau.ru/staff?page={0}&letter=0"


raw = re.sub("\n", " ", get_from("https://ssau.ru/staff"))
page_max = max(list(map(lambda x: int(x), re.findall(r"(?<=page=)\d+", raw))))
for i in range(page_max):
    tmp_raw = re.sub("\n", " ", get_from(template.format(i+1)))
    tmp_info = re.findall(r"https://ssau.ru/staff/\d+.*?(?=</a>)", tmp_raw)
    for j in tmp_info:
        tmp = re.sub("-.+>", "", j)
        tmp = re.sub(r".*/", "", tmp).strip().split(" ", 1)
        teachers[tmp[1]] = STAFF_SCHED_TEMP.format(tmp[0])


with open("schedule_staff.json", "w") as f:
    json.dump(teachers, f, indent=4, ensure_ascii=False, sort_keys=True)
