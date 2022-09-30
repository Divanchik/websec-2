from mywebfunc import *
import re
import json
from tqdm import tqdm


groups = {}
b = re.findall(r"(?<=/rasp/faculty/)\d+(?=\?course=1)", get_from("https://ssau.ru/rasp"))
for grId in tqdm(b):
    raw = get_from("https://ssau.ru/rasp/faculty/{0}?course=1".format(grId))
    courses = list(map(lambda x: int(x), re.findall(r"(?<=course=)\d+", raw)))
    if len(courses) == 0: continue
    for cId in range(max(courses)):
        raw = get_from("https://ssau.ru/rasp/faculty/{0}?course={1}".format(grId, cId))
        for i in re.findall(r"(?<=groupId=).*?\d{4}-\d{6}D", raw):
            t = re.sub("\".*(?=\d{4}-\d{6}D)", " ", i).split()
            groups[t[1]] = GROUP_SCHED_TEMP.format(t[0])


with open("schedule_groups.json", "w") as f:
    json.dump(groups, f, indent=4, ensure_ascii=False, sort_keys=True)
