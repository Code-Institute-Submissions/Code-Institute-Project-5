# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from rich.table import Table
from rich.console import Console
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Candidates_database")


def isRecruiter():
    """
    This function checks if you are a recruiter.
    """
    temp = ""
    while temp != "recruiter" and temp != "candidate" and temp != "q":
        temp = input(
            "Please tell us if you are a recruiter or a candidate (Press q to exit):\n"
        )
        temp = temp.lower()
    return temp


def getNames(worksheet):
    """
    This function loads names from google sheets.
    """
    names = []
    candidates = worksheet.get_all_records()

    for i in range(len(candidates)):
        names.append(candidates[i]["Full name"])

    return names


def getName(names):
    """
    This function checks if name is in the list.
    """
    name = ""
    while name not in names:
        if name == "Q":
            break

        if len(names) == 0:
            print("There is no candidate in the list...")
            break

        name = input("Choose a candidate (Press q to exit):\n")
        name = name.title()

    return name


def checkValue(value):
    """
    This function checks if value is empty string.
    """
    try:
        if len(value) == 0:
            raise ValueError("Empty string")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again!")
        return False

    return True


def deleteCandidate():
    """
    This function delete a candidate from google sheets.
    """
    worksheet = SHEET.worksheet("database")
    CandidatesNames = getNames(worksheet)

    print("List of all available candidates...")
    for CandidateName in CandidatesNames:
        print(CandidateName)

    CandidateName = getName(CandidatesNames)

    for i in range(len(CandidatesNames)):
        if CandidateName == CandidatesNames[i]:
            worksheet.delete_rows(i + 2)
            print("Deleting the candidate from the database...")


def addNewCandidate():
    """
    This function add a new candidate to google sheets.
    """
    CandidateData = []
    print("First of all we want to know your contact data.")

    while True:
        FullName = input("Please give us your full name:\n")
        if checkValue(FullName):
            CandidateData.append(FullName)
            break

    while True:
        Role = input("Which open position are you looking for?\n")
        if checkValue(Role):
            CandidateData.append(Role)
            break

    while True:
        Address = input("Could you please tell us your location?\n")
        if checkValue(Address):
            CandidateData.append(Address)
            break

    while True:
        Phone = input("Your phone number:\n")
        if checkValue(Phone):
            CandidateData.append(Phone)
            break

    while True:
        Email = input("Your email:\n")
        if checkValue(Email):
            CandidateData.append(Email)
            break

    while True:
        Languages = input("Which languages are you speaking?\n")
        if checkValue(Languages):
            CandidateData.append(Languages)
            break

    while True:
        Skills = input("Tell us more about your skills:\n")
        if checkValue(Skills):
            CandidateData.append(Skills)
            break

    while True:
        Software = input("Which PC Software are you using?\n")
        if checkValue(Software):
            CandidateData.append(Software)
            break

    while True:
        Equipment = input("Which lab equipment are you frequently using?\n")
        if checkValue(Equipment):
            CandidateData.append(Equipment)
            break

    while True:
        Hobbies = input("Tell us something about your hobbies:\n")
        if checkValue(Hobbies):
            CandidateData.append(Hobbies)
            break

    print("\n")
    print("Please share some data for the main part of CV\n")

    while True:
        Introduction = input("Give introduction to the main part of CV:\n")
        if checkValue(Introduction):
            CandidateData.append(Introduction)
            break

    while True:
        WorkHistory = input("Tell us more about your experience:\n")
        if checkValue(WorkHistory):
            CandidateData.append(WorkHistory)
            break

    while True:
        Education = input("Where did you study?\n")
        if checkValue(Education):
            CandidateData.append(Education)
            break

    worksheet = SHEET.worksheet("database")
    worksheet.append_row(CandidateData)
    print("New candidate was added!")


def PrintCV(role):
    """
    This function prints your CV based on data from google sheets.
    """
    worksheet = SHEET.worksheet("database")
    CandidatesNames = getNames(worksheet)

    if role == "recruiter":
        print("List of all available candidates...")
        for CandidateName in CandidatesNames:
            print(CandidateName)

    if role == "recruiter":
        CandidateName = getName(CandidatesNames)
    else:
        CandidateName = ""
        while CandidateName == "" and CandidateName != "Q":
            CandidateName = input("Your name (Press q to exit):\n")
            CandidateName = CandidateName.title()

    if CandidateName not in CandidatesNames:
        print("Your name is not in the database, but you can add a new candidate")
        addNewCandidate()
    else:
        if CandidateName != "Q":
            data = worksheet.get_all_records()

            for i in range(len(CandidatesNames)):
                if data[i]["Full name"] == CandidateName:
                    break

            os.system("clear")

            if CandidateName != "Q":
                table = Table(title=CandidateName)
                table.add_column("Contacts", width=80)
                table.add_column("", width=100)

                candidate = data[i]["Full name"] + "\n" + data[i]["Role"] + "\n"

                temp = data[i]["Address"].split(",")
                candidate += "Address:" + "\n"
                for addr in temp:
                    candidate += "\t" + addr + "\n"

                candidate += "Phone:" + "\n" + "\t" + str(data[i]["Phone number"]) + "\n"
                candidate += "Email:" + "\n" + "\t" + data[i]["Email"] + "\n"

                temp = data[i]["Languages"].split(",")
                candidate += "Languages:" + "\n"
                for language in temp:
                    candidate += "\t" + language + "\n"

                temp = data[i]["Skills"].split(",")
                candidate += "Skills:" + "\n"
                for skill in temp:
                    candidate += "\t" + skill + "\n"

                temp = data[i]["Software"].split(",")
                candidate += "PC Software:" + "\n"
                for software in temp:
                    candidate += "\t" + software + "\n"

                temp = data[i]["Lab equipment"].split(",")
                candidate += "Lab equipment:" + "\n"
                for equipment in temp:
                    candidate += "\t" + equipment + "\n"

                temp = data[i]["Hobbies"].split(",")
                candidate += "Hobbies:" + "\n"
                for hobby in temp:
                    candidate += "\t" + hobby + "\n"

                main = data[i]["Introduction"] + "\n" + "\n"

                temp = data[i]["Experience"].split(".")
                main += "Work History" + "\n"
                for work in temp:
                    main += work + "\n"

                temp = data[i]["Education"].split(".")
                main += "Education" + "\n"
                for education in temp:
                    main += education + "\n"

                table.add_row(candidate, main)
                console = Console()
                console.print(table)


if __name__ == "__main__":
    print(
        """
    __  ______     __  __     __               
   / / / / __ \   / / / /__  / /___  ___  _____
  / /_/ / /_/ /  / /_/ / _ \/ / __ \/ _ \/ ___/
 / __  / _, _/  / __  /  __/ / /_/ /  __/ /    
/_/ /_/_/ |_|  /_/ /_/\___/_/ .___/\___/_/     
                           /_/                 
    """
    )
    print(
        "This program is called 'HR Helper'. It serves to make easier routine work of HR managers and "
        "to create a nice looking CV. The application can be used by recruiters and candidates "
        "as well. As a recruiter you can add a new candidate, delete one or view candidates profiles. "
        "Candidates can just check their profile.\n"
    )

    while True:
        you = isRecruiter()

        if you == "recruiter":
            os.system("clear")
            # Recruiter can delete existing candidate, add a new one to the database or view available profiles
            choice = ""
            while choice != "delete" and choice != "add" and choice != "load":
                choice = input(
                    "Delete a candidate, add a new one to the list or load existing profiles [delete/add/load]:\n"
                )
                choice = choice.lower()

            if choice == "delete":
                # Delete existing candidate from the database
                deleteCandidate()
                os.system("clear")

            elif choice == "add":
                # Add new candidate to the database
                addNewCandidate()

            elif choice == "load":
                PrintCV("recruiter")

        elif you == "candidate":
            PrintCV("candidate")

        elif you == "q":
            break
