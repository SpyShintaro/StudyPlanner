# Imports
if __name__ == "__main__": # Band-Aid fix for if I want to directly test this module in particular (deleting later)
    from time import *
else:
    from studytime.time import *

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
        data = self.load_file()
    
    def generate_new_year(self, year) -> list:
        new_year = []

        for month in range(1, 13):
            new_year.append([dates for dates in map_dates(year, month) if dates != 0])
        
        return new_year
    
    def new_file(self):
        """
        Generates a new file
        """
        file_path = f"studytime/app_data/{self.file_name}.json"
        now = datetime.today()

        template = {f"{now.year}": self.generate_new_year(now.year)}
        
        with open(file_path, "a") as f:
            json.dump(template, f, indent = 4)
        
        return template
    
    def load_file(self) -> str:
        """
        Loads json file given the relevant filename. If there's no corresponding file, it makes a new file.
        """
        file_path = f"studytime/app_data/{self.file_name}.json"

        try:
            with open(file_path) as f:
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
    def __init__(self, name, date_set: datetime, deadline: datetime):
        self.name = f"{deadline} {name}"
        self.date_set = date_set
        self.deadline = deadline
    
    def generate_task(self):
        """
        Saves the task into various other objects
        """

def map_dates(year, month) -> list[int]:
    """
    Maps all dates in the month to weekdays for use in calendar, and returns a tuple containg the first weekday of the month, and the final day
    """

    starting_weekday, month_range = calendar.monthrange(year, month)
    
    dates = [0] * (starting_weekday - 1) + [date for date in range(month_range + 1)] # Adds 0 for each day until the starting weekday of the month, after which it appends the date to each element of the list

    return dates

if __name__ == "__main__":
    save = SaveInstance("date")