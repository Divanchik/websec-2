import sys
import requests
import re
from time import sleep
import json


def get_from(link: str, count=10):
    while count > 0:
        reply = requests.get(link).text
        if reply.find("503 Service Temporarily Unavailable") < 0:
            return reply
        count -= 1
        sleep(1)
    return "fail"

a = requests.get("https://ssau.ru/rasp")
b = re.findall(r"/rasp/faculty/.*?(?=</a>)", a.text)

info = []
faculty = {}
for i in b:
    info.append("https://ssau.ru" + re.sub("\".*?>", "", i).strip())
print("Got", len(info), "faculties")
for i in range(len(info)):
    tmp = info[i].split(" ", 1)
    faculty[tmp[1]] = [tmp[0]]


key0 = list(faculty.keys())[0]
link0 = faculty[key0][0]
print("Getting", link0)
fac_req = get_from(link0)
if fac_req == "fail":
    print("Service not available")
    sys.exit()

gr_ids = re.findall(r"(?<=groupId=).*?\d{4}-\d{6}D", fac_req)
for i in gr_ids:
    re.sub("\"(?=)\d{4}-\d{6}D")
# with open("fac_log1.txt", "w") as f:
#     f.write(fac_req.text)

