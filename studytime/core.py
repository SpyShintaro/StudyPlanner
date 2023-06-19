# Imports
if __name__ == "__main__": # Band-Aid fix for if I want to directly test this module in particular (deleting later)
    from time_class import *
else:
    from studytime.time_class import *

from datetime import datetime
import calendar
import json

class SaveInstance:
    """
    Data handler for StudyTime saves
    """
    def __init__(self, file_name: str):
        """
        Caches relevant data from json file
        """
        self.file_name = file_name
        self.data = self.load_file()
    
    def generate_new_year(self, year) -> list:
        """
        Generates a new year instance 
        """
        new_year = []

        for month in range(1, 13):
            current_month = Month(month, year, [Date(date) for date in map_dates(year, month) if date != 0]).prepare_dict()
            new_year.append({f"{current_month['name']}": current_month['data']}) # Generates a dictionary item for each month, involving the dates
        
        return new_year
    
    def new_file(self):
        """
        Generates a new file
        """
        file_path = f"studytime/app_data/{self.file_name}.json"
        now = datetime.today()

        template = {f"{now.year}": self.generate_new_year(now.year)}
        
        with open(file_path, "w") as f:
            json.dump(template, f, indent = 4)
        
        return template

    def update_file(self, year):
        """
        Gets new year data, and updates the JSON file accordingly
        """
        file_path = f"studytime/app_data/{self.file_name}.json"
        template = {f"{year}": self.generate_new_year(year)}

        with open(file_path, "r") as f: # Loading JSON file into Python Object
            data = json.load(f)
        
        data.update(template) # Adding template to the JSON/Python object

        with open(file_path, "w") as f: # Rewrites JSON file using updated data
            json.dump(data, f, indent=4)
        
        return template
    
    def load_file(self) -> str:
        """
        Loads json file given the relevant filename. If there's no corresponding file, it makes a new file.
        """
        file_path = f"studytime/app_data/{self.file_name}.json"

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                print(data["2023"])
        except FileNotFoundError:
            print(self.new_file())

    def organise_times(self, data):
        """
        Handles the creation of year, month, and date objects
        """
        self.years = []
        for year in data: # Accessing year array
            self.years.append(Year(year))


class Task:
    """
    The standard type of StudyTime object, this indicates any one-time activity that is set for the user to complete by a certain time
    """
    def __init__(self, name: str, date_set: datetime.date, deadline: datetime, subject):
        """
        Creates a dictionary object
        """
        self.name = name
        self.date_set = date_set
        self.deadline = deadline
        self.subject = subject
    
    def generate_task(self):
        """
        Saves the task into various other objects
        """
        item_data = {
            "name": f"{self.name}",
            "subject": f"{self.subject}",
            "date set": f"{self.date_set}",
        }

def map_dates(year: int, month: int) -> list[int]:
    """
    Maps all dates in the month to weekdays for use in calendar, and returns a tuple containg the first weekday of the month, and the final day
    """

    starting_weekday, month_range = calendar.monthrange(year, month)
    
    dates = [0] * (starting_weekday - 1) + [date for date in range(month_range + 1)] # Adds 0 for each day until the starting weekday of the month, after which it appends the date to each element of the list

    return dates

if __name__ == "__main__":
    save = SaveInstance("date")