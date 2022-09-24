import requests
import sys
import os
from time import sleep, time

def get_from(link: str, count=10) -> str:
    for i in range(count):
        reply = requests.get(link).text
        if reply.find("503 Service Temporarily Unavailable") < 0:
            return reply
        sleep(1)
    print("Fail:", link)
    sys.exit(os.EX_UNAVAILABLE)

STAFF_SCHED_TEMP = "https://ssau.ru/rasp?staffId={0}"
GROUP_SCHED_TEMP = "https://ssau.ru/rasp?groupId={0}"