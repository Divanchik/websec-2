import requests
import sys
import os
from time import sleep, time

def get_from(link: str, count=10) -> str:
    link_status: int
    for i in range(count):
        reply = requests.get(link)
        link_status = reply.status_code
        if reply.status_code in range(200, 300):
            return reply.text
        sleep(1)
    print(f"Status {link_status}:", link)
    sys.exit(os.EX_UNAVAILABLE)
