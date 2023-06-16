"""
studytime.time

Author: Jake Hickey
Description: A library containing definitions for time classes in studytime 
"""

# Imports
from studytime import core
from datetime import datetime
import json

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class SaveInstance:
    def __init__(self, file_name: str):
        data = self.load_file(file_name)
    
    def new_file(self, file_name: str):
        file_path = f"studytime/app_data/{file_name}.json"

        now = datetime.today()
        year = []
        
        for month in range(1, 13):
            year.append([])

        template = {}
    
    def load_file(self, filename: str) -> str:
        """
        Loads json file given the relevant filename. If there's no file corresponding, it makes a new file.
        """
        file_path = f"studytime/app_data/{filename}.json"

        try:
            with open(file_path) as f:
                data = json.load(f)
                print(data["2023"])
        except FileNotFoundError:
            with open(file_path, "w") as f:
                data = json.load(f)
        return data

    def organise_times(self, data):
        self.years = []
        for year in data:
            self.years.append(Year(year))

class Year:
    def __init__(self, year_data):
        self.year = year_data

class Month:
    def __init__(self, month: datetime.month, year: datetime.year, date_objects):
        self.name = f"{months[month - 1]} {year}"
        self.dates = date_objects

class Date:
    def __init__(self, date: datetime) -> None:
        pass