from scrape import get_pdf
from utils import extract_json
from interact import get_service,insert_events

def main():
    URL = 'https://pict.edu/student/time-table-and-syllabus/'
    #Task 1 - Get the pdf on local machine
    get_pdf(URL)
    #Task 2 - Extract the table from the downloaded timetable pdf
    extract_json('timetable.pdf')
    #Task 3 - Insert the data into google calendar using its API
    service = get_service()
    insert_events(service)




if __name__ == "__main__":
    main()
