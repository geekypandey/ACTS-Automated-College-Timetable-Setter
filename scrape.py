#Task 1 - Get the Required timetable from the college website
#Web scrapping
import requests
from bs4 import BeautifulSoup as bs
import os
import sys

#url to be scrapped(College website pages showing the link of all timetables)
#URL = 'https://pict.edu/student/time-table-and-syllabus/'

def get_pdf(URL):
    #sending request
    res = requests.get(URL)

    soup = bs(res.text,'html.parser')

    table = soup.find('table')

    for link in table.find_all('a'):
        if link.text == 'TE ALL':
            target = link
            break
    timetable_pdf = target['href']

    print('Downlaoding your timetable......')
    os.system(f'wget -O timetable.pdf {timetable_pdf}')
    if os.path.exists('timetable.pdf'):
        print('Successfully donwloaded your timetable.')
    else:
        print('Problem in downloading your timetable.\n Exiting...')
        sys.exit(1)
