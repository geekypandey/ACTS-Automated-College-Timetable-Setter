from scrape import get_pdf
from interact import get_service,insert_events,delete_events
import time

def main():
    start = time.time()
    class_ = input("Enter your class(FE/SE/TE/BE) :")
    branch_ = input("Enter your branch(COMP/IT/ENTC) :")
    URL = 'https://pict.edu/student/time-table-and-syllabus/'
    #Task 1 - Get the pdf on local machine
    get_pdf(URL,class_,branch_)
    #Task 2 - Extract the table from the downloaded timetable pdf
    #Task 3 - Insert the data into google calendar using its API
    service = get_service()
    eventIds = insert_events(service)
    choice = input("Do you want to delete the inserted items?(y/n) :")
    if choice == 'y':
        delete_events(service,eventIds)
    end = time.time()
    print(end-start)



if __name__ == "__main__":
    main()
