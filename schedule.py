# import argparse
from json import dump, dumps
import re
import requests
import sys
import os
from time import sleep

# print("argv1", sys.argv[1])

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


# parser = argparse.ArgumentParser(description='Get schedule.')
# parser.add_argument("link", type=str)
# args = parser.parse_args()

data = {}
page_raw = get_from(sys.argv[1])
page_raw = re.sub("\n", " ", page_raw)

# title
title = re.search("<h2 class=\"h2-text info-block__title\">(.*?)</h2>", page_raw)
data['title'] = title.group(1).strip()

# weeks
weeks = re.findall("(\d{1,2}) неделя", page_raw)
weeks = list(map(lambda x: int(x), weeks))
data['weeks'] = weeks
# print(sys.argv[1], data)

# days dates
head_dates = re.findall("schedule__head-date.*?(\d{2}\.\d{2}\.\d{4})", page_raw)
data['dates'] = head_dates

# weekday nav items
weekdays = re.findall("class=\"weekday-nav__item (weekday-nav__item_active|) \" ><div class=\"caption-text weekday-nav__item-weekday\"> ([а-я]+)</div><div class=\"subtitle-text weekday-nav__item-date\"> ([\d]+)", page_raw)
data['weekdays'] = weekdays

data['rows'] = []
# lessons timespans
time_spans = re.findall("\"schedule__time\".*?(\d\d:\d\d).*?(\d\d:\d\d)", page_raw)
for t in time_spans:
    data['rows'].append({'timespan':t})

# cells
lesson_group = "(lesson-color-type-(\d)\">([а-яА-Я ё-]+)</div><div class=\"caption-text schedule__place\">([а-яА-ЯA-Z ё\d-]*)</div>(?:<div class=\"schedule__teacher\"> *(?:<a class=\"caption-text\" href=\".*?(\?staffId=\d+)\" >|)([\.а-яА-ЯA-Z ё\d-]*)|))"
items = re.findall("<div class=\"schedule__item (schedule__item_show|)\">(.*?)</div>(?=<div class=\"schedule__item|</div></div></div></div><div class=\"footer\">)", page_raw)

cells = []
for i in items:
    is_showing = "s_item_show" if i[0]=="schedule__item_show" else ""
    lessons = re.findall(lesson_group, i[1])
    cells.append({'is_showing':is_showing, 'lessons':[{'type':j[1], 'title':j[2], 'place':j[3], 'staffid':j[4], 'staff':j[5]} for j in lessons]})

for i in range(len(time_spans)):
    data['rows'][i]['items'] = []
    for j in range(len(head_dates)):
        data['rows'][i]['items'].append(cells[i*len(head_dates)+j])

# print(dumps(data, indent=4, ensure_ascii=False))

with open("schedule.json", "w", encoding='utf-8') as f:
        dump(data, f, indent=4, ensure_ascii=False)
