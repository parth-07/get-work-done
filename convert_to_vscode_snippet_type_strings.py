import os
import sys
from pathlib import Path

if len(sys.argv) != 2 :
    print("Invalid number of arguments present")
    sys.exit(1)

file_path = Path(sys.argv[1])
dir = file_path.parent.resolve()
file_name = file_path.name
temp_file_name = 'temp.txt'

os.chdir(dir)

f = open(file_name,'r')
temp = open(temp_file_name,'w')

for line in f:
    line = line.rstrip()
    line = line.replace('"','\\"')
    line = line.replace('\t','\\t')
    line = line.replace('\\n','\\\\n')
    line = '"' + line + '",\n'
    temp.write(line)

f.close()
temp.close()    
