from pathlib import Path
import os
import pyperclip
import sys
import subprocess 
import re

if len(sys.argv) != 2 :
    print("Wrong number of arguments given , exiting program")
    sys.exit(1)
    
folder_path = Path(sys.argv[1])

os.chdir(folder_path)

reg = re.compile(r'(\d+)\s+min\s+(\d+)\s+s')
reg_duration = re.compile('duration',re.IGNORECASE)

total_min=0
total_sec=0

for filename in os.listdir() :
    duration = subprocess.Popen(['mediainfo',filename],stdout = subprocess.PIPE)
    duration = subprocess.run(['grep','-i','duration','-m 1'],stdin=duration.stdout,capture_output=True)
    duration = duration.stdout.decode('utf-8')
    if not reg_duration.search(duration) :
        continue
    # print(filename)
    match = reg.search(duration)
    min = int(match[1])
    sec = int(match[2])
    # print(filename,min,"minutes",sec,"seconds")
    total_min+=min
    total_sec+=sec

total_hour = 0
total_min+=(total_sec)//60
total_hour+=(total_min)//60
total_min = total_min%60
total_sec = total_sec%60

print(total_hour,"hours",end=' ')
print(total_min,"minutes",end=' ')
print(total_sec,"seconds",end=' ')