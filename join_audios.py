import subprocess as sub
import re
import sys
import pyperclip
from pathlib import Path
audio = re.compile('(?<!res[0-9])(.mp3|.mpeg|.wav)$',re.IGNORECASE)

if len(sys.argv) != 2 :
    print("Invalid arguments supplied , try again with valid command line arguments")
    sys.exit(1)

path = sub.check_output(['pwd'],cwd=sys.argv[1])
path=path.decode('utf-8')
if path.endswith('\n') :
    path = path[:-1]
if not path.endswith('/') :
    path+='/'
all_files = sub.Popen(['find','.','-printf','%f\n'],cwd=sys.argv[1],stdout=sub.PIPE)
all_files=sub.check_output(['sort','-n','-'],stdin=all_files.stdout)
all_files = all_files.decode('utf-8')
all_files=all_files.split('\n')
# print(all_files)
# print(path)
for f in all_files :
    f=path+f
    # print(f)
# all_files.sort()
all_files = [Path(path+f) for f in all_files]
command = "ffmpeg "
n=0
for f in all_files :
    if audio.search(str(f)) != None :
        print(f.name)
        command+="-i \""+str(f)+"\" "
        n+=1
command+="-filter_complex "
command+="\"concat=n="+str(n)+":v=0:a=1[aout]\" "
command+="-map '[aout]' "
command+="-codec:a libmp3lame -q:a 5 res1.mp3"        
print(command)
pyperclip.copy(command)