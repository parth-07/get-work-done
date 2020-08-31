import pyperclip
import re
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    print("Invalid number of arguments given")
    sys.exit(1)

pattern = re.compile('[\s]?#include[\s]*"([\w./]+)"')

temp_file_name = 'temp.txt'
file_path = Path(sys.argv[1])
file_name = file_path.name

def handle_includes(file_path):
    dir = file_path.parent.resolve()
    file_name = file_path.name
    os.chdir(dir)
    f = open(file_name, 'r')
    content = ""
    for line in f:
            mo = pattern.match(line)
            if not mo:
                content += line
            else:
                inc_file_name = Path(mo.group(1))
                # print(inc_file_name)
                handled_content = handle_includes(inc_file_name)
                content += handled_content
                os.chdir(dir)
    f.close()
    return content

content = handle_includes(file_path)
# print(os.getcwd())
temp = open(temp_file_name, 'w')
# print(content)
temp.write(content)
temp.close()
os.replace(temp_file_name, file_name)
