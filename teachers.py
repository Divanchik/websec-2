import requests
from time import sleep
import sys
import os
import re
import json
from tqdm import tqdm


def get_from(link: str, count=10) -> str:
    while count > 0:
        reply = requests.get(link).text
        if reply.find("503 Service Temporarily Unavailable") < 0:
            return reply
        count -= 1
        sleep(1)
    print("Fail:", link)
    sys.exit(os.EX_UNAVAILABLE)


teachers = {}
template = "https://ssau.ru/staff?page={0}&letter=0"


raw = re.sub("\n", " ", get_from("https://ssau.ru/staff"))
page_max = max(list(map(lambda x: int(x), re.findall(r"(?<=page=)\d+", raw))))
for i in tqdm(range(1, page_max + 1)):
    tmp_raw = re.sub("\n", " ", get_from(template.format(i)))
    tmp_info = re.findall(r"https://ssau.ru/staff/\d+.*?(?=</a>)", tmp_raw)
    for j in tmp_info:
        tmp = re.sub("-.+>", "", j)
        tmp = re.sub(r".*/", "", tmp).strip().split(" ", 1)
        teachers[tmp[1]] = tmp[0]


with open("teachers.json", "w") as f:
    json.dump(teachers, f, indent=4, ensure_ascii=False, sort_keys=True)