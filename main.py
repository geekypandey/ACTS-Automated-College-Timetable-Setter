import calendar
import sys
from collections import namedtuple
from collections import defaultdict
from datetime import date
from datetime import datetime
from datetime import timedelta

import camelot
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from google_calendar import get_service
from google_calendar import create_event

pd.options.mode.chained_assignment = None

URL = 'https://pict.edu/student/time-table-and-syllabus/'
branch_range = {'common': (1, 2),
                'comp': (2, 5),
                'entc': (5, 9),
                'it': (9, 12)}
year_number = {'fe': 0, 'se': 0, 'te': 1, 'be': 2}
fname = 'timetable.pdf'
Data = namedtuple('Data', ['summary', 'start_time', 'end_time'])


# Exceptions

def download_pdf(year: str, branch: str):
    if year == 'fe':
        branch = 'common'
    start, end = branch_range[branch]
    idx = year_number[year]
    res = requests.get(URL)

    soup = bs(res.text, 'html.parser')
    table = soup.find('table')

    rows = table.find_all('tr')[start: end]
    target_row = rows[idx]
    target_col = target_row.find_all('td')[-1]
    target_link = target_col.find('a')
    if not target_link:
        print('Timetable not found.')
        print('Exiting...')
        sys.exit(1)
    target_link = target_link['href']

    res = requests.get(target_link, stream=True)

    with open(fname, 'wb') as f:
        f.write(res.content)
    print(f'Downloaded the timetable @ {fname}...')


def fill_empty(df):
    for idx, cell in enumerate(df['Monday']):
        if 'break' in cell.lower():
            df.iloc[idx][2:] = cell
        if cell.strip() == '' and idx > 0:
            df['Monday'].iloc[idx] = df['Monday'].iloc[idx-1]
    columns = df.columns[2:].tolist()
    for col in columns:
        for idx, cell in enumerate(df[col]):
            if cell.strip() == '' and idx > 0:
                df[col].iloc[idx] = df[col].iloc[idx-1]
    return df


def extract_table(page_number: int):
    tables = camelot.read_pdf(fname, pages=page_number)
    df = tables[0].df
    header = df.loc[0]
    df = df[1:]
    df.columns = header
    df = fill_empty(df)
    print('Table successfully extracted...')
    return df


def extract_data(df):
    data = defaultdict(list)
    for day in df.columns[1:]:
        for idx, cell in enumerate(df[day]):
            if not cell:
                continue
            start, end = df['Time'].iloc[idx].split('to')
            start = start.strip()
            end = end.strip()
            if start >= '08:00' and start < '12:00':
                start = start + ' am'
            else:
                start = start + ' pm'
            if end >= '08:00' and end < '12:00':
                end = end + ' am'
            else:
                end = end + ' pm'

            if data[day] and data[day][-1].summary == cell:
                d = data[day].pop()
                d = Data(summary=d.summary, start_time=d.start_time, end_time=end)
                data[day].append(d)
            else:
                d = Data(summary=cell, start_time=start, end_time=end)
                data[day].append(d)
    return data


def get_input(msg: str) -> str:
    inp = input(msg)
    inp = inp.lower().strip()
    return inp


def filter_and_add_datetime(data):
    today = date.today()
    curr = today
    result = []
    d_format = '%Y-%m-%d %I:%M %p'
    for day in calendar.day_name[today.weekday():]:
        for d in data[day]:
            start_time = datetime.strptime(str(curr) + f' {d.start_time}', d_format)
            end_time = datetime.strptime(str(curr) + f' {d.end_time}', d_format)
            new_d = Data(d.summary, start_time.isoformat(), end_time.isoformat())
            result.append(new_d)
        curr += timedelta(days=1)
    return result


if __name__ == '__main__':
    year = get_input('Enter your year (FE/SE/TE/BE): ')
    branch = get_input('Enter your branch (COMP/IT/ENTC): ')
    division = get_input('Enter your division: ')

    if year not in ['fe', 'se', 'te', 'be']:
        print('Enter valid year (FE/SE/TE/BE)')
        print('Exiting')
        sys.exit(1)

    if branch not in ['comp', 'entc', 'it']:
        print('Enter valid branch (COMP/ENTC/IT)')
        print('Exiting')
        sys.exit(1)

    print('Downloading timetable...')
    download_pdf(year, branch)
    df = extract_table(division)
    data = extract_data(df)
    data = filter_and_add_datetime(data)
    service = get_service()
    eventIds = []
    print('Creating event....')
    for d in tqdm(data):
        eventIds.append(create_event(d, service))
    with open('events.log', 'w+') as f:
        f.write('\n'.join(eventIds))
