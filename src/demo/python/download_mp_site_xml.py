import urllib.request
import gzip
import csv
import requests

#cd "/Applications/Python 3.6/"
#sudo "./Install Certificates.command"


def read_csv_to_list(path_string):
    with open(path_string, 'r') as f:
        reader = csv.reader(f)
        return list(reader)


def get_all_sitemap_xml_urls(sitemap_url = 'https://www.mountainproject.com/sitemap.xml'):

    with urllib.request.urlopen(sitemap_url) as sitemap:
        return sitemap.read()


def extract_xml_urls_to_list(all_urls_as_string = None):

    pos = 0
    max_pos = len(all_urls_as_string) - 1
    url_list = []
    target_start_tag = '<sitemap><loc>'
    target_end_tag = '</loc></sitemap>'

    while pos < max_pos:
        found_index = all_urls_as_string.find(target_start_tag, pos + 1)
        if found_index == -1:
            break
        end_index = all_urls_as_string.find(target_end_tag, found_index)
        url = all_urls_as_string[found_index + len(target_start_tag):end_index]
        url_list.append(url)
        pos = found_index

    return url_list


def get_route_urls_from_sitexml(url_to_site_xml_gz = None):
    route_urls = []

    with urllib.request.urlopen(url_to_site_xml_gz) as zip:

        with gzip.open(zip) as f:

            site_xml_string = str(f.read())
            pos = 0
            max_pos = len(site_xml_string) - 1
            target_start_tag = 'https://www.mountainproject.com/route/'
            target_end_tag = '</loc>'

            while pos < max_pos:
                found_index = site_xml_string.find(target_start_tag, pos + 1)
                if found_index == -1:
                    break
                end_index = site_xml_string.find(target_end_tag, found_index)
                url = site_xml_string[found_index:end_index]
                route_urls.append(url)
                pos = found_index

    return route_urls


def extract_id_from_route_url(route_url = None):
    target = '/route/'
    target_index = route_url.find(target)
    start_index = target_index + len(target)
    id = route_url[start_index: route_url.find('/', start_index)]
    return id


def subset_route_id_list(all_route_ids):
    route_id_subset_lists = []

    id_list = all_route_ids
    start = 0
    chunk_size = 200
    max_index = len(id_list) - 1

    while True:
        end_index = start + chunk_size
        if end_index > max_index:
            route_id_subset_list = id_list[start: max_index + 1]
            route_id_subset_lists.append(route_id_subset_list)
            break
        route_id_subset_list = id_list[start: end_index]
        route_id_subset_lists.append(route_id_subset_list)
        start = end_index

    return route_id_subset_lists


# # get all sitemap xml urls as string
# all_sitemap_xml_url = str(get_all_sitemap_xml_urls())
#
# # parse all sitemap xml urls to list
# xml_url_list = extract_xml_urls_to_list(all_sitemap_xml_url)
#
# # read gz files from sitemap xml url list, extract all route urls
# route_url_list = []
# for xml_url in xml_url_list:
#     route_url_list.extend(get_route_urls_from_sitexml(xml_url))
#
# # create route id list
# route_id_list = [extract_id_from_route_url(x) for x in route_url_list]
#
# # create list of lists, where inner lists contain (max) 200 route ids
# route_id_subsets_list = subset_route_id_list(route_id_list)
#
# ## write copy of route ids
# with open('/Users/christineibaraki/Desktop/mp_route_ids_16_September_2020.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(route_id_subsets_list)

route_id_subsets_list = read_csv_to_list('/Users/christineibaraki/Desktop/mp_route_ids_16_September_2020.csv')

response_json_list = []
url = 'https://www.mountainproject.com/data/get-routes?'


start_index = 1110 #481, 0
KEY = None

for index in range(start_index, len(route_id_subsets_list)):
    route_id_subset = route_id_subsets_list[index]
    route_id_list_string = ','.join(route_id_subset)

    try:
        r = requests.get(url = url, params = {'routeIds':route_id_list_string, 'key': KEY})
        response_json_list.extend(r.json()['routes'])
        print('repsonse json list size: ' + str(len(response_json_list)))
    except:
        print("Error index = " + str(index))
        break

### parse response json lst
variables_to_write = ['id',
                      'name',
                      'type',
                      'rating',
                      'stars',
                      'starVotes',
                      'pitches',
                      'location',
                      'url',
                      'longitude',
                      'latitude']

results = [variables_to_write]
for response_dict in response_json_list:
    if 'id' in response_dict:
        new_row = [response_dict[var] if var in response_dict else '' for var in variables_to_write]
        new_row = ['; '.join(x) if isinstance(x, list) else x for x in new_row ]
        results.append(new_row)

file_name = '/Users/christineibaraki/Desktop/mp_route_names_PART_THREE.csv'
with open(file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(results)

