#!/usr/bin/env python3

import re
import sys
from datetime import datetime

my_book = sys.argv[1]
result = ""

with open(my_book, "r", encoding="utf-8") as f:
    data = f.read()

description = data.split('<description>')
if len(description) == 2:
    description = description[1].split("</description")[0]
    title_info = description.split('<title-info>')[1].split('</title-info>')[0]
    auth = title_info.split('<author>')
    auth = [a for a in auth if 'name>' in a]
    author = []
    if auth:
        for au in auth:
            au = au.split('</author>')[0].split('<id>')[0]
            au = re.sub('<[^<]+?>', '', au).split('\n')
            au = [a.strip() for a in au]
            au = " ".join(au).strip()
            author.append(au)
        author = ", ".join(author)
    else:
        author = "Unknown"
    book_title = title_info.split('<book-title>')
    book_title = book_title[1].split('</book-title>')[0].strip() if len(book_title) == 2 else "Untitled"

    publish_info = description.split('<publish-info>')
    if len(publish_info) == 2:
        publish_info = publish_info[1].split('</publish-info>')[0]
        year = publish_info.split('<year>')
        year = year[1].split('</year>')[0] if len(year) == 2 else datetime.now().year
        output_file = f"{author} - {book_title} - {year}.txt"
    else:
        year = datetime.now().year
else:
    author, book_title, year = "Unknown", "Untitled", datetime.now().year
output_file = f"{author} - {book_title} - {year}.txt"

data = data.split("<body>")[1].split("</body>")[0]
sections = data.split('<section>')[1:]
if len(sections) == 1:
    result += f"{author} - {book_title}.\n\n"

for section in sections:
    if "<title>" in section:
        section_title = section.split('<title>')[1].split('</title>')[0]
        section_title = re.sub('<[^<]+?>', '', section_title).split("\n")
        section_title = [t.strip() for t in section_title if t.strip() not in ""]
        section_title = [t + "." if t[-1].isalpha() or t[-1].isdigit() else t for t in section_title]
        section_title = " ".join(section_title)
        result += "\n" + section_title + "\n\n"
        section_content = section.split('<section>')[0].split('</title>')[1:]
        section_content = " ".join(section_content)
        content = re.sub('<[^<]+?>', '', section_content)
        result += f"{content}\n==="
    else:
        content = re.sub('<[^<]+?>', '', section)
        result += f"{content}\n\n"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(result)
print(f"Saved to: {output_file}\n Now run: ./convert_book.py -b {output_file}")
