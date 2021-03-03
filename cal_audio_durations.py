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

duration_reg = re.compile(r'^Duration\s+:\s+(?:(?P<minutes>\d+)\s+min\s*)?(?:(?P<seconds>\d+)\s+s\s*)?(?:(?P<milliseconds>\d+)\s+ms\s*)?$',re.IGNORECASE)
duration_exist_reg = re.compile('duration',re.IGNORECASE)

total_min=0
total_sec=0
total_ms = 0

for filename in os.listdir() :
    duration = subprocess.Popen(['mediainfo',filename],stdout = subprocess.PIPE)
    duration = subprocess.run(['grep','-i','duration','-m 1'],stdin=duration.stdout,capture_output=True)
    duration = duration.stdout.decode('utf-8')
    if not duration_exist_reg.search(duration) :
        continue
    print(filename,duration)
    song_duration = duration_reg.match(duration)
    if not song_duration:
        print("Unable to get duration of ",filename)
        sys.exit(1)

    min = 0
    sec = 0
    ms = 0
    if song_duration['minutes'] :
        min = int(song_duration['minutes'])
    if song_duration['seconds'] :
        sec = int(song_duration['seconds'])
    if song_duration['milliseconds']:
        ms = int(song_duration['milliseconds'])
    
    total_min+=min
    total_sec+=sec
    total_ms+=ms
    
total_hour = 0
total_sec+=(total_ms)//100
total_min+=(total_sec)//60
total_hour+=(total_min)//60
total_min = total_min%60
total_sec = total_sec%60
total_ms = total_ms%100

print(total_hour,"hours",end=' ')
print(total_min,"minutes",end=' ')
print(total_sec,"seconds",end=' ')
print(total_ms,"milliseconds")