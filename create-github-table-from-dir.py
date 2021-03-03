import os
from pathlib import Path
import argparse
import json
import subprocess
import yaml
import copy

parser = argparse.ArgumentParser(description="Create github table from directory structure")
parser.add_argument('-d')
args = parser.parse_args()

FILES_BASE_LINK = "https://github.com/parth-07/ds-and-algos/blob/master/include/"

BASE_DIR = Path(args.d)
SOURCE_DIR = BASE_DIR/"include/dragon"
EXAMPLES_DIR = BASE_DIR/"examples/"
RESOURCES_FILE = BASE_DIR/"table-resources.yaml"

TABLE_OUT_FILE = '/home/parth/Programming/get_work_done/table-out.txt'

def source_formal_name(name):
    name = name[:name.rfind('.')]
    name = name[:1].upper() + name[1:]
    name = name.replace('-',' ')
    return name

def example_formal_name(name):
    name = name[:name.rfind('.')]
    return name

def just_name(name):
    name = name[:name.rfind('.')]
    return name

def associative_to_value(associate,sort_keys = False):
    if sort_keys:
        value = " ".join(v for k,v in sorted(associate.items(),key=lambda item: item[0]))
    else:
        value = " ".join([v for k,v in associate.items()])
    return value

def check_git_status(rel_path):
    run_res = subprocess.run(['git','status','-s','--ignored',rel_path],capture_output=True)
    # print(rel_path,run_res.stdout.decode('utf-8'))
    return run_res.stdout.decode('utf-8')[0:2]

def up_to_date_version_already_committed(rel_path):
    return check_git_status(rel_path).strip() == ''

def obtain_source_data(dir):
    source = {}
    source['files'] = {}
    for file in os.listdir(dir):
        if (dir/file).is_dir():
            source[file] = obtain_source_data(dir/file)
        else:
            # print(file,check_git_status(file/dir))
            if up_to_date_version_already_committed(dir/file):
                source['files'][file] = "["+source_formal_name(file)+"]" + "("+str((dir/file).relative_to(BASE_DIR))+")"
    # if not source['files']:
        # del source['files']
    return source

def obtain_examples_data(dir):
    examples = {}
    examples['files'] = {}
    examples['value'] = ""
    for file in os.listdir(dir):
        if (dir/file).is_dir():
            examples[file] = obtain_examples_data(dir/file)
        else:
            if up_to_date_version_already_committed(dir/file):
                examples['files'][file] = "["+example_formal_name(file)+"]" + "("+str((dir/file).relative_to(BASE_DIR))+")"
    # if not examples['files']:
    #     del examples['files']
    # else:
    examples['value'] = associative_to_value(examples['files'],sort_keys=True)
    return examples

def prepare_resources_data(data):
    for source in data:
        if 'resources' in data[source]:
            data[source]['value'] = ""
            for resource_name,resource_link in data[source]['resources'].items():
                data[source]['value'] += "["+resource_name+"]"+"("+resource_link+")" + " "
        else:
            data['source'] = prepare_resources_data(data[source])
    return data

def obtain_resources_data(absolute_resources_file):
    resources_data = {}
    with open(absolute_resources_file,'rb') as f:
        resources_data = yaml.safe_load(f)
    temp = copy.deepcopy(resources_data)
    for heading in temp:
        for source_name,source_resource_data in temp[heading].items():
            for resource_name,resource_link in source_resource_data['resources'].items():
                resources_data[heading][source_name]['resources'][resource_name] = "["+resource_name+"]"+"("+resource_link+")"
            resources_data[heading][source_name]['value'] = associative_to_value(resources_data[heading][source_name]['resources'])
    return resources_data

def compute_col_width(source_particular,examples_particular,resources_particular):
    # print(examples_particular)
    col_width = {}
    col_width['name'] = 0
    col_width['examples'] = 0
    col_width['good resources to study'] = 0
    
    EXTRA_SPACE_REQ = 2
    
    for key,value in source_particular.items():
        col_width['name'] = max(col_width['name'],len(value)+EXTRA_SPACE_REQ)
    for ex_source_name,ex_row_data in examples_particular.items():
        examples_temp_width = 0
        # print(ex_source_name,ex_row_data)
        if ex_source_name != 'value' and ex_source_name != 'files':
            examples_temp_width+=(len(ex_row_data['value']) + EXTRA_SPACE_REQ)
        col_width['examples'] = max(col_width['examples'],examples_temp_width)
    for resource_source_name,resource_row_data in resources_particular.items():
        resources_temp_width=(len(resource_row_data['value']) + EXTRA_SPACE_REQ)
        col_width['good resources to study'] = max(col_width['good resources to study'],resources_temp_width)
    
    return col_width

def write_heading(f,heading,level = 4):
    f.write("#"*level+" "+heading)
    f.write("\n")


def start_table(f,col_width):
    f.write("|")
    for col,width in col_width.items():
        width_covered = 0
        f.write(" "+col+" ")
        width_covered+=len(col)+2
        f.write(" "*(width - width_covered))
        f.write("|")
    f.write("\n")
    f.write("|")
    for col,width in col_width.items():
        f.write("-"*width)
        f.write("|")
    f.write("\n")
counter = 1

def write_row(f,row_data,col_width):
    f.write('|')
    for col,data in row_data.items():
        width_covered = 0 
        f.write(" "+data+" ")
        width_covered+=len(data)+2
        f.write(" "*(col_width[col]-width_covered))
        f.write("|")
    f.write("\n")    


os.chdir(BASE_DIR)


resources_data = obtain_resources_data(RESOURCES_FILE)
resources_json = json.dumps(resources_data,indent=4)
# print(resources_json)
    
source_data = obtain_source_data(SOURCE_DIR)
examples_data = obtain_examples_data(EXAMPLES_DIR)
resources_data = obtain_resources_data(RESOURCES_FILE)
source_json = json.dumps(source_data,indent=4)
examples_json = json.dumps(examples_data,indent=4)
# print(source_json)
# print(examples_json)



columns = ["name","examples","good resources to study"]

with open(TABLE_OUT_FILE,'w') as f:
    headings = ['number-theory','ds','tree','algos']
    for heading in headings:
        if heading == 'files':
            continue
        print("heading =",heading)
        examples_particular = examples_data[heading]
        source_particular = source_data[heading]['files']
        resources_particular = resources_data[heading]
        col_width = compute_col_width(source_particular,examples_particular,resources_particular)
        
        write_heading(f,heading.title())
        start_table(f,col_width)
        
        for source_file_name,source_file_row_data in source_particular.items():
            row_data = {}
            row_data['name'] = source_file_row_data
            row_data['examples'] = examples_particular[just_name(source_file_name)]['value']
            row_data['good resources to study'] = resources_particular[just_name(source_file_name)]['value']
            write_row(f,row_data,col_width)
        f.write("\n")
        
        