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


def isRecruiter():
    temp = ""
    while temp != "recruiter" and temp != "candidate":
        temp = input("Please tell us if you are a recruiter or a candidate: ")
        temp = temp.lower()
    return temp


def deleteCandidate():
    print("List of all available candidates...")
    worksheet = SHEET.worksheet("database")
    candidatesList = worksheet.get_all_records()
                
    names = []
    for i in range(len(candidatesList)):
        name = candidatesList[i]["Full name"]
        names.append(name)
        print(name)

    name = ""
    while name not in names:
        name = input("Choose the candidate you want to delete: ")
        name = name.title()
                
    print("Deleting the candidate from the database...")

    for i in range(len(candidatesList)):
        if name == candidatesList[i]["Full name"]:
            worksheet.delete_row(i+2)
            break


def addNewCandidate():
    while True:
        contacts = input("Could you please tell us your contact data? (Press q to exit)\n"
                         "Example: Full name, Role, Address, Phone number, Email, Languages you "
                         "speak, Your skills, Your hobbies\n")

        education = input("Please tell us something about your education\n")

        if contacts == "q":
            print("Failed to add a new candidate...")
            break

        contacts = contacts.split(",")

        try:
            if len(contacts) == 0:
                raise ValueError("Error! Empty string!")
        except ValueError as e:
            print(f"{e} Please try again.")
        else:
            break

    if contacts != "q":
        worksheet = SHEET.worksheet("database")
        worksheet.append_row(contacts)
        print("New candidate was added!")


if __name__ == "__main__":
    print("This program is called 'CV generator'. It serves to create a nice looking CV to increase your "
          "chances to find a job of your dream. The application can be used by recruiters and candidates "
          "as well. As a recruiter you can add a new candidate, delete one or view candidates profiles."
          "Candidates can just check their profile.")
    
    while True:
        you = isRecruiter()

        if you == "recruiter":
            # Recruiter can delete existing candidate, add a new one to the database or view available profiles
            choice = ""
            while choice != "delete" and choice != "add" and choice != "load":
                choice = input("Delete a candidate, add a new one to the list or load existing profiles [delete/add/load]: ")
                choice = choice.lower()
            
            if choice == "delete":
                # Delete existing candidate from the database
                print("Deleting the candidate...")
                deleteCandidate()

            elif choice == "add":
                # Add new candidate to the database
                print("Adding a new candidate...")
                addNewCandidate()

            elif choice == "load":
                pass

            elif you == "candidate":
                pass
