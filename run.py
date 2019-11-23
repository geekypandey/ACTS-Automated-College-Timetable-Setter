from scrape import get_pdf
from interact import get_service,insert_events
import time

def main():
    start = time.time()
    URL = 'https://pict.edu/student/time-table-and-syllabus/'
    #Task 1 - Get the pdf on local machine
    get_pdf(URL)
    #Task 2 - Extract the table from the downloaded timetable pdf
    #Task 3 - Insert the data into google calendar using its API
    service = get_service()
    insert_events(service)
    end = time.time()
    print(end-start)



if __name__ == "__main__":
    main()
