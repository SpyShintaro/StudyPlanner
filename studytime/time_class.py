"""
studytime.time_class

Author: Jake Hickey
Description: A library containing definitions for time classes in studytime 
"""

# Imports
from datetime import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


class Year:
    def __init__(self, year_data: dict):
        self.year = []

        for month, dates in year_data.items():
            self.year.append(Month(month, dates))


class Month:
    def __init__(self, month, date_objects: list):
        self.month = month
        self.name = f"{months[int(month) - 1]}"
        self.dates = date_objects

    def prepare_list(self) -> list:
        """
        Maps out data into dictionary for storage in JSON format
        """
        data = [date.prepare_dict() for date in self.dates]

        return data

class Date:
    def __init__(self, date: datetime.day) -> None:
        self.name = f"{str(date).rjust(2, '0')}"
        self.items = []
    
    def add_item(self, item):
        self.items[item["name"]] = {item}
    
    def prepare_dict(self) -> dict:
        data = {
            "date": self.name,
            "data": self.items
        }

        return data