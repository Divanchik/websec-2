from mywebfunc import *
import re
import json
from tqdm import tqdm


raw = re.sub("\n", " ", get_from("https://ssau.ru/rasp"))
lines = re.findall("<a href=\"/rasp/faculty/\d+\?course=1\" class=\"h3-text\">.*?</a>", raw)
faculty = {}
for i in lines:
    new_name = re.findall(r"(?<=>).*?(?=<)", i)[0].strip() # faculty name
    new_id = re.findall(r"\d+(?=\?)", i)[0] # faculty id
    faculty[new_name] = {"id": new_id}


for name, fac in tqdm(faculty.items(), desc="Processing groups"):
    fac_id = fac['id']
    faculty[name]["groups"] = {}
    raw = get_from(f"https://ssau.ru/rasp/faculty/{fac_id}?course=1")
    courses = list(map(lambda x: int(x), re.findall(r"(?<=course=)\d+", raw)))
    if len(courses) == 0: continue
    for course_id in courses:
        raw = get_from(f"https://ssau.ru/rasp/faculty/{fac_id}?course={course_id}")
        for i in re.findall(r"(?<=groupId=).*?\d{4}-\d{6}D", raw):
            t = re.sub("\".*(?=\d{4}-\d{6}D)", " ", i).split()
            faculty[name]["groups"][t[1]] = t[0]


with open("data_groups.json", "w") as f:
    json.dump(faculty, f, indent=4, ensure_ascii=False, sort_keys=True)
