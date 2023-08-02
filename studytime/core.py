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
import calendar, json, re, difflib, win32com, win32com.client

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
        data = self.get_date(year, month, str(day).rjust(2, "0"))

        data.append(item.prepare_dict())
        data.sort(key=lambda x : x["time"]) # Sorts the date items by their timestamp in ascending order

        self.save_changes()
    
    def remove_item(self, item_name: str, item_time: datetime):
        """
        A generic method for removing organizational items to the relevant date
        """

        year, month, day = item_time.year, item_time.month, item_time.day
        data = self.get_date(year, month, str(day).rjust(2, '0'))

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
        
        self.add_year(target_year)
        self.get_year(target_year)
    
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
            if str(date["date"]) == str(target_date):
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

        """with open(file_path, "r") as f: # Loading JSON file into Python Object
            data = json.load(f)
        
                for years in data:
            if years.keys()[0] == year:
                break
            else:
        """

        self.data.append(template) # Adding template to the JSON/Python object

        with open(file_path, "w") as f: # Rewrites JSON file using updated data
            json.dump(self.data, f, indent=4)

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

    def scan_items(self) -> list:
        """
        Scans through the save data for any organizational items and returns them as a list
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
        Searches through item list for results with specified name
        """
        try:
            query = re.compile(fr"{name.lower()}+")
            results = []

            for date in self.items:
                items = date["data"]
                for item in items:
                    if query.findall(item["name"].lower()):
                        item["date"] = date["date"]
                        results.append(item)
            
            return sorted(results, key=lambda x: difflib.SequenceMatcher(None, x["name"], name).ratio(), reverse=True)
        except re.error:
            return

    def search_date(self, date_time: datetime):
        """
        Searches through item list for any items that match specified date
        """
        query = re.compile(fr"{date_time.month}/{str(date_time.day).rjust(2, '0')}/{date_time.year}")
        results = []

        for date in self.items:
            if query.findall(date["date"].lower()):
                for item in date["data"]:
                    results.append(item)
        
        return results

    def save_changes(self):
        """
        Writes the contents of this save instance's data attribute over the save file
        """
        file_path = f"studytime/app_data/{self.file_name}.json"

        with open(file_path, "w") as f:
            json.dump(self.data, f, indent=4)
        
        self.scan_items()


    def organise_times(self, data):
        """
        Handles the creation of year, month, and date objects
        """
        self.years = []
        for year in data: # Accessing year array
            self.years.append(Year(year))
    
    def set_notification(self, item: dict, time: datetime, descr: str):
        """
        Sets a Windows Toast Notification for the item
        """
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        root_folder = scheduler.GetFolder('\\')
        task_def = scheduler.NewTask(0)

        # Create trigger
        start_time = time
        TASK_TRIGGER_TIME = 1
        trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
        trigger.StartBoundary = start_time.isoformat()

        # Create action
        TASK_ACTION_EXEC = 0
        action = task_def.Actions.Create(TASK_ACTION_EXEC)
        action.ID = 'ExecAction'
        action.Path = r'C:\Users\jakei\StudyPlanner\.venv\Scripts\python.exe' # TODO replace these hardcoded file paths
        action.WorkingDirectory = r'C:\Users\jakei\StudyPlanner'
        action.Arguments = f'create_notif.py "{item["name"]}" "{descr}"'

        # Set parameters
        task_def.RegistrationInfo.Description = descr
        task_def.Settings.Enabled = True
        task_def.Settings.StopIfGoingOnBatteries = False

        # Register task
        # If task already exists, it will be updated
        TASK_CREATE_OR_UPDATE = 6
        TASK_LOGON_NONE = 0

        name = f'{item["name"]} {time.strftime("%m_%d_%Y %H_%M_%S")}'.replace(':', '_')
        
        root_folder.RegisterTaskDefinition(
            name,  # Task name
            task_def,
            TASK_CREATE_OR_UPDATE,
            '',  # No user
            '',  # No password
            TASK_LOGON_NONE)

    def remove_notification(self, item: dict, time: datetime):
        """
        Removes the notification
        """
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()
        root_folder = scheduler.GetFolder("\\")
        
        root_folder.DeleteTask()

        item_id = f"{item['time']} {time.strftime('%m-%d-%Y %H:%M:%S')}"
        root_folder.DeleteTask(item_id, 0)


class Task:
    """
    The standard type of StudyTime object, this indicates any one-time activity that is set for the user to complete by a certain time
    """
    def __init__(self, name: str, date: datetime, subject):
        """
        Creates a dictionary object
        """
        self.name = name
        self.date = f"{date.year}-{date.month}-{str(date.day).rjust(2, '0')}"
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
            "completed": f"{self.completed}",
            "type": "Task"
        }

        return data

    def edit(self, data: dict):
        self.name = data["name"]
        
        date_time = data["date"]
        self.date = f"{date_time.year}-{date_time.month}-{str(date_time.day).rjust(2, '0')}"
        self.time = date_time.time().strftime("%H:%M:%S")
        self.subject = data["subject"]

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