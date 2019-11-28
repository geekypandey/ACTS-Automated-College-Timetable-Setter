# ACTS(Automate College TimeTable Setter)
Set college timetable for a week on google calendar,based on the timetable uploaded on the college website.

## Getting Started
These instructions will help to run the code on a local mahcine.

### Setting up the environment
```
git clone https://github.com/geekypandey/ACTS.git
cd ACTS
python -m venv .venv 
. .venv/bin/activate 
pip install -r requirements.txt
```
One requirement is the credentials.json file which would be used for authentication for the Google Calendar API.
```
https://developers.google.com/calendar/quickstart/python
```
Click on the **Enable the Google Calendar API** and download the credentials.json file to the directory.

To run the application:
```
python run.py
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
