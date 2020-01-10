import re
import json
from mdutils import MdUtils
from bs4 import BeautifulSoup as bs4
from os import listdir
from os.path import isfile, join


def get_number(s):
    if type(s) is str:
        return re.findall(r'\d+', s)
    else:
        return []


def clean_html(raw_html):
    soup = bs4(raw_html, "html.parser")
    for i in soup.findAll('a'):
        i.clear()
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', str(soup))


def read_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def create_notebook(name, title):
    md_file = MdUtils(file_name=name)
    md_file.write("#%% md\n")
    md_file.write("# " + title + "\n")
    return md_file


def write_md_file(md_file, number, text):
    md_file.write("#%% md\n")
    md_file.write("## Aufgabe " + number + "\n")
    md_file.write(text)
    md_file.write("#%%\n")


def get_topics(json_file):
    with open(json_file) as f:
        data = json.load(f)
    topics = set()
    for item in data:
        topics.add(item['topic'])
    topics = set([i['topic'] for i in data])
    return topics


onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
for file in onlyfiles:
    print(file)
    if file.endswith(".json"):
        json_data = read_json(file)
        name = file.split(".")[0]
        md_file = create_notebook(name=name, title=name)

        for item in json_data:
            if item['number'] is None or len(get_number(item['number'])) == 0:
                continue
            clean_num = get_number(item['number'])[0]
            clean_text = clean_html(item['text'])
            write_md_file(md_file=md_file, number=clean_num, text=clean_text)
        md_file.create_md_file()
    else:
        continue
