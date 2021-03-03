import sys
import yaml

if len(sys.argv) != 2:
    print("invalid arguments, try again with correct arguments")
    sys.exit(1)
    
yaml_file = sys.argv[1]

with open(yaml_file,'r') as f:
    try :
        data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(e)
        
rows_source = data['rows']
sorted(rows_source , key=lambda x: x['name'])
rows = []
width = {
    'Name':0,
    'Examples':0,
    'resources':0
}
def updateWidths(row) :
    for key,val in row.items():
        width[key] = max(width[key],len(val)+10)
for row_source in rows_source:
    row = {}
    row['Name'] = "[{}]({})".format(row_source['name'],data['sourceBaseLink']+'/'+row_source['source']+'.hpp')
    row['Examples'] = "[Link]({})".format(data['examplesBaseLink']+'/'+row_source['source'])
    row['resources'] = ""
    for key,val in row_source['resources'].items():
        row["resources"] += "[{}]({}), ".format(key,val)
    updateWidths(row)
    rows.append(row)

for row in rows:
    print(row,"\n")
print(width)

with open('temp-table.txt','w') as out_file:
    width['Good resources to study'] = width['resources']
    for heading in data['headings']:
        out_file.write('| ')
        out_file.write(heading)
        space_required = width[heading] - len(heading)
        out_file.write(' '*space_required)
        out_file.write(' ')
    
    out_file.write(' |')
    out_file.write('\n')
    
    for heading in data['headings']:
        out_file.write('| ')
        out_file.write('-'*width[heading])
        out_file.write(' ')
    
    out_file.write(' |')
    
    out_file.write('\n')
    for row in rows:
        for key,val in row.items():
            out_file.write('| ')
            out_file.write(val)
            space_required = width[key] - len(val)
            out_file.write(' '*space_required)
            out_file.write(' ')
        
        out_file.write(' |')
        out_file.write('\n')
        
        
        