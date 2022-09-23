import sys
import requests
import re
import os
from time import sleep
import json

group_link_format = "https://ssau.ru/rasp?groupId={0}"


def get_from(link: str, count=10):
    while count > 0:
        reply = requests.get(link).text
        if reply.find("503 Service Temporarily Unavailable") < 0:
            return reply
        count -= 1
        sleep(1)
    print("Fail:", link)
    sys.exit(os.EX_UNAVAILABLE)


b = re.findall(r"/rasp/faculty/.*?(?=</a>)", get_from("https://ssau.ru/rasp"))

info = ["https://ssau.ru" + re.sub("\".*?>", "", i).strip() for i in b]
print("Got", len(info), "faculties")


faculty = {}
for i in range(len(info)):
    tmp = info[i].split(" ", 1)
    faculty[tmp[1]] = [tmp[0]]

for title, data in faculty.items():
    raw = get_from(data[0])
    for i in re.findall(r"(?<=groupId=).*?\d{4}-\d{6}D", raw):
        t = re.sub("\".*(?=\d{4}-\d{6}D)", " ", i)
        print(t)


# with open("fac_log1.txt", "w") as f:
#     f.write(fac_req.text)

