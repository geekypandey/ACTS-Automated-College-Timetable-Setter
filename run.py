from scrape import get_pdf
from interact import Interact
import time
from utils import extract_df

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
URL = 'https://pict.edu/student/time-table-and-syllabus/'

def main():
    start = time.time()
    
    #Take user input for class,branch and division
    class_ = input("Enter your class(FE/SE/TE/BE) :").strip()
    branch_ = input("Enter your branch(COMP/IT/ENTC) :").strip()
    div_ = input("Enter your division :").strip()

    #Task 1 - Get the pdf on local machine
    get_pdf(URL,class_,branch_)

    #Task 2 - Extract the table from the downloaded timetable pdf
    df = extract_df('timetable.pdf',div_)
    
    #Task 3 - Insert the data into google calendar using its API
    service = Interact(SCOPES) 
    eventIds = service.insert_events(df)
    print(len(service))
    choice = input("Do you want to delete the inserted items? :")
    if choice.lower() in ['y','yes']:
        service.delete_events()
    end = time.time()
    print(end-start)



if __name__ == "__main__":
    main()
