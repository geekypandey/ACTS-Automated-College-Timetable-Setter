import requests
from bs4 import BeautifulSoup as bs
import os
import sys

#URL = 'https://pict.edu/student/time-table-and-syllabus/'

def get_pdf(URL,class_='TE',div_='COMP'):
    year = {'FE':1,'SE':2,'TE':3,'BE':4}
    div = {'COMP':1,'IT':2,'ENTC':3}
    
    if class_ == 'FE':
        class_name = 'FE All Div.'
    else:
        class_name = f'{class_} ALL'

    res = requests.get(URL)

    if res.status_code != requests.codes.okay:
        print(f'Error {res.status_code}')
        sys.exit(1)
        
    soup = bs(res.text,'html.parser')

    table = soup.find('table')
    
    count = 1
    for link in table.find_all('a'):
        if link.text == class_name:
            if class_ == 'FE':
                target = link
                break
            elif count == div[div_]:
                target = link
                break
            count += 1
    timetable_pdf = target['href']

    print('Downlaoding your timetable......')
    os.system(f'wget -O timetable.pdf {timetable_pdf}')
    if os.path.exists('timetable.pdf'):
        print('Successfully donwloaded your timetable.')
    else:
        print('Problem in downloading your timetable.\n Exiting...')
        sys.exit(1)

