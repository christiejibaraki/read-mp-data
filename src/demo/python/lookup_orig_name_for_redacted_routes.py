import urllib.request
import csv
import html

def read_csv_to_list(path_string):
    with open(path_string, 'r') as f:
        reader = csv.reader(f)
        return list(reader)


def write_list_to_csv(lines, file_name):
    with open(file_name, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)


data = read_csv_to_list('/Users/christineibaraki/Desktop/mp_route_names_PART_ONE.csv')
data2 = read_csv_to_list('/Users/christineibaraki/Desktop/mp_route_names_PART_TWO.csv')
data3 = read_csv_to_list('/Users/christineibaraki/Desktop/mp_route_names_PART_THREE.csv')

header = data.pop(0)
data2.pop(0)
data3.pop(0)

print(len(data))
print(len(data2))
print(len(data3))
total_len = len(data) + len(data2) + len(data3)
print(total_len)

data.extend(data2)
data.extend(data3)
assert(len(data) == total_len)


header.append('orig_name')
name_col = header.index('name')
id_col = header.index('id')
start_tag = 'Mountain Project has chosen not to publish the original name of this route:\\n'
end_tag = "\\n"

new_results =[header]

for row in data:
    name = row[name_col]
    row[name_col] = html.unescape(name)
    if name.strip().upper() in ['REDACTED', '[REDACTED]']:
        id = row[id_col]
        with urllib.request.urlopen('https://www.mountainproject.com/object/updates/' + id + '/redacted') as site_content:
            site_text_string = str(site_content.read())
            start_index = site_text_string.find(start_tag)
            if start_index != -1:
                orig_name = site_text_string[start_index + len(start_tag) : site_text_string.find(end_tag, start_index + len(start_tag) + 1)]
                clean_name = orig_name.strip()
                clean_name = clean_name[1:len(clean_name)-2]
                clean_name = html.unescape(clean_name)
                print(clean_name)
                row.append(clean_name)
            else:
                row.append('')
    else:
        row.append('')

    new_results.append(row)


write_list_to_csv(new_results, '/Users/christineibaraki/Desktop/mp_route_names_with_orig_names.csv')