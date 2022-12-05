# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Candidates_database')

if __name__ == "__main__":
    print("This program is called 'CV generator'. It serves to create a nice looking CV to increase your"
          "chances to find a job of your dream. The application can be used by recruiters and candidates"
          "as well. As a recruiter you can add a new candidate, delete one or view candidates profiles."
          "Candidates can just check their profile.")