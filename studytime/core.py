"""
studytime.core

Author: Jake Hickey
Description: A library containing backend logic for StudyTime processes
"""

# Imports
if __name__ == "__main__": # Band-Aid fix for if I want to directly test this module in particular (deleting later)
    from time_class import *
else:
    from studytime.time_class import *

from datetime import datetime
import calendar
import json
import re

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

        self.items = self.scan_items()

    def add_item(self, item_time: datetime, item: object):
        """
        A generic method for adding organizational items to the relevant date
        """
        year, month, day = item_time.year, item_time.month, item_time.day
        data = self.get_date(year, month, day)

        data.append(item.prepare_dict())
        data.sort(key=lambda x : x["time"]) # Sorts the date items by their timestamp in ascending order

        self.save_changes()
    
    def remove_item(self, item_name: str, item_time: datetime):
        """
        A generic method for removing organizational items to the relevant date
        """

        year, month, day = item_time.year, item_time.month, item_time.day
        data = self.get_date(year, month, day)

        for item in data:
            if item["name"] == item_name and item["time"] == str(item_time.time()): # Should be specific enough to prevent double-ups
                data.remove(item)
                self.save_changes()
                return
    
    def add_task(self, task_name: str, task_time: datetime, subject: str):
        """
        Takes new task info and appends it to the "data" list for the relevant date, before sorting it
        """
        task = Task(task_name, task_time, subject)

        self.add_item(task_time, task)
    
    def add_event(self, event_name: str, event_time: datetime):
        """
        Takes new event info and appends it to the "data" list for the relevant date, before sorting it
        """
        event = Event(event_name, event_time)

        self.add_item(event_time, event)
    
    def add_assignment(self, assignment_name: str, assignment_time: datetime, subject: str):
        """
        Takes new assignment info and appends it to the "data" list for the relevant date, before sorting it
        """
        assignment = Assignment(assignment_name, assignment_time, subject)

        self.add_item(assignment_time, assignment)

    def generate_new_year(self, year: str) -> list:
        """
        Generates a new year instance 
        """
        new_year = []

        for month in range(1, 13):
            current_month = Month(month, [Date(date) for date in map_dates(year, month) if date != 0]).prepare_list()
            new_year.append(current_month) # Generates a dictionary item for each month, involving the dates
        
        return new_year

    def get_year(self, target_year: str) -> dict:
        """
        Returns the dictionary for the target year
        """
        for year in self.data:
            if year["year"] == str(target_year): # Checks if the value of the "year" key is the year being searched for
                return year
        
        return None
    
    def get_month(self, target_year: str, target_month: int) -> list:
        """
        Returns a list for the target month. Target_month should be passed with the assumption that January = 1
        """
        year = self.get_year(target_year)

        return year["months"][target_month - 1]

    def get_date(self, target_year: str, target_month: int, target_date: str) -> list:
        """
        Returns a list of all items scheduled for the target date.
        """
        month = self.get_month(target_year, target_month)

        for date in month:
            if date["date"] == str(target_date):
                return date["data"]
    
    def new_file(self):
        """
        Generates a new file
        """
        file_path = f"studytime/app_data/{self.file_name}.json"
        now = datetime.today()

        template = [{
            "year": f"{now.year}",
            "months": self.generate_new_year(now.year)
        }]
        
        with open(file_path, "w") as f:
            json.dump(template, f, indent = 4) # Outputs empty template for the current year to a new file
        
        return template

    def add_year(self, year):
        """
        Handles adding new years to the file
        """
        file_path = f"studytime/app_data/{self.file_name}.json"
        template = {
                    "year": f"{year}",
                    "months": self.generate_new_year(year)
                    }

        with open(file_path, "r") as f: # Loading JSON file into Python Object
            data = json.load(f)
        
        """        for years in data:
            if years.keys()[0] == year:
                break
            else:
        """

        data.append(template) # Adding template to the JSON/Python object

        with open(file_path, "w") as f: # Rewrites JSON file using updated data
            json.dump(data, f, indent=4)
        
        print(self.data)

        return template
    
    def load_file(self) -> dict:
        """
        Loads json file given the relevant filename. If there's no corresponding file, it makes a new file.
        """
        file_path = f"studytime/app_data/{self.file_name}.json"

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = self.new_file()

        return data

    def scan_items(self):
        """
        Scans through the save data for any organizational items
        """
        items = []
        for year in self.data:
            for idx, month in enumerate(year["months"]):
                for date in month:
                    if date["data"] != []:
                        items.append({"date": datetime(int(year["year"]), idx + 1, int(date["date"])).strftime("%m/%d/%Y"),
                                      "data": date["data"]}) # Pretty sure this shouldn't work, but I suppose God is smiling down on me today
        
        return items

    def search_name(self, name: str) -> list:
        """
        Searches through items for results with specified name
        """
        query = re.compile(fr"{name}")
        results = []

        for date in self.items:
            print(date)
            items = date["data"]
            for item in items:
                if query.match(item["name"]):
                    results.append(item)
        
        return results

    def save_changes(self):
        """
        Writes the contents of this save instance's data attribute over the save file
        """
        file_path = f"studytime/app_data/{self.file_name}.json"

        with open(file_path, "w") as f:
            json.dump(self.data, f, indent=4)

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
    def __init__(self, name: str, date: datetime, subject):
        """
        Creates a dictionary object
        """
        self.name = name
        self.date = date
        self.time = date.time().strftime("%H:%M:%S")
        self.subject = subject
        self.completed = False
    
    def prepare_dict(self):
        """
        Returns a dictionary for the purpose of storing within the save instance
        """
        data = {
            "name": f"{self.name}",
            "subject": f"{self.subject}",
            "time": f"{self.time}",
            "completed": False,
            "type": "Task"
        }

        return data

    def mark_completed(self, complete: bool):
        self.completed = complete

class Event:
    """
    An activity that automatically marks itself as completed after the time slot regardless of user input
    """
    def __init__(self, name: str, date: datetime):
        self.name = name
        self.date = date
        self.time = date.time().strftime("%H:%M:%S")
    
    def prepare_dict(self) -> dict:
        data = {
            "name": f"{self.name}",
            "time": f"{self.time}",
            "type": "Event"
        }

        return data

class Assignment:
    """
    A cross between an event and an activity, automatically marking itself as completed, while still being tied to a subject
    """
    def __init__(self, name: str, date: datetime, subject: str):
        self.name = name
        self.date = date
        self.time = date.time().strftime("%H:%M:%S")
        self.subject = subject
        self.completed = False
    
    def prepare_dict(self):
        data = {
            "name": f"{self.name}",
            "time": f"{self.time}",
            "subject": f"{self.subject}",
            "completed": f"{self.completed}",
            "type": "Assignment"
        }

        return data

def map_dates(year: int, month: int) -> list:
    """
    Maps all dates in the month to weekdays for use in calendar, and returns a tuple containg the first weekday of the month, and the final day
    """

    year, month = int(year), int(month)
    starting_weekday, month_range = calendar.monthrange(year, month)
    
    dates = [0] * (starting_weekday - 1) + [date for date in range(month_range + 1)] # Adds 0 for each day until the starting weekday of the month, after which it appends the date to each element of the list

    return dates

if __name__ == "__main__":
    save = SaveInstance("dates")