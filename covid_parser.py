# Copyright (C) 2020 Alex Verrico (https://AlexVerrico.com/)
# Australian covid statistics are provided by https://covid19data.com.au/

import urllib.request
import json


aus_locations = {'aus': 1, 'nsw': 1, 'vic': 2, 'qld': 3, 'sa': 4, 'wa': 5, 'tas': 6, 'nt': 7, 'act': 8}


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def download_data(url):
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
    return data


def get_state_new(data_type='cases'):
    if data_type == 'cases':
        data = download_data(r'https://infogram.com/1p0lp9vmnqd3n9te63x3q090ketnx57evn5?live')
        junk, data = data.split('dbf","chart_type_nr":10,"data":[')
        data, junk = data.split('],"custom":{"showPoints":true')
        data = data.replace(r'\u002F', '/')
        statedata = json.loads(data)
        return statedata
    elif data_type == 'deaths':
        data = download_data(r'https://e.infogram.com/90ab7c54-efe3-4d76-a3f6-19c8544249e4?live')
        junk, data = data.split('a3b","chart_type_nr":10,"data":[')
        data, junk = data.split('],"custom":{"showPoints":false')
        data = data.replace(r'\u002f', '/')
        statedata = json.loads(data)
        return statedata


def get_aus_new(data_type='cases'):
    if data_type == 'cases':
        data = download_data(r'https://infogram.com/1p7ve7kjeld1pebz2nm0vpqv7nsnp92jn2x?live')
        junk, data = data.split('a7e","chart_type_nr":1,"data":[')
        data, junk = data.split('],"custom":{"showPoints":true')
        data = data.replace(r'\u002F', '/')
        ausdata = json.loads(data)
        return ausdata
    elif data_type == 'deaths':
        data = download_data(r'https://e.infogram.com/154e01ec-a6e7-45da-8fcf-d6c9a6669ba8?live')
        junk, data = data.split('aae","chart_type_nr":1,"data":[')
        data, junk = data.split('],"custom":{"showPoints":false')
        data = data.replace(r'\u002F', '/')
        ausdata = json.loads(data)
        return ausdata


def get_country_new(country='australia', data_type='cases'):
    data = download_data(r'https://epidemic-stats.com/coronavirus/%s' % country)
    if data_type == 'cases':
        junk, data = data.split('infected_new = ')
        data, junk = data.split('const recovered_new = ')
        data = data.replace("'", '"')
        data = rreplace(data, ',', '', 1)
        countrydata = json.loads(data)
        return countrydata
    elif data_type == 'deaths':
        junk, data = data.split('deaths_new = ')
        data, junk = data.split('const infected_new = ')
        data = data.replace("'", '"')
        data = rreplace(data, ',', '', 1)
        countrydata = json.loads(data)
        return countrydata


def new_cases(location='aus'):
    if location in aus_locations:
        if location == 'aus':
            data = get_aus_new()
        else:
            data = get_state_new()
        parsed_data = [data[-1][aus_locations[location]], data[-2][aus_locations[location]]]
    elif location == 'usa':
        data = get_country_new('usa')
        parsed_data = [data[-1], data[-2]]
    else:
        data = get_country_new(location)
        parsed_data = [data[-1], data[-2]]
    return parsed_data


def new_deaths(location='aus'):
    if location in aus_locations:
        if location == 'aus':
            data = get_aus_new(data_type='deaths')
        else:
            data = get_state_new(data_type='deaths')
        parsed_data = [data[-1][aus_locations[location]], data[-2][aus_locations[location]]]
    elif location == 'usa':
        data = get_country_new('usa', data_type='deaths')
        parsed_data = [data[-1], data[-2]]
    else:
        data = get_country_new(location)
        parsed_data = [data[-1], data[-2]]
    return parsed_data
