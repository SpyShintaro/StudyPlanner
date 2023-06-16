from datetime import datetime
import calendar

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

def map_dates(self):
    """
    Maps all dates in the month to weekdays for use in calendar, and returns a tuple containg the first weekday of the month, and the final day
    """
    today = datetime.today()

    starting_weekday, month_range = calendar.monthrange(today.year, today.month)

    
    dates = [0] * (starting_weekday - 1) + [date for date in range(month_range + 1)][::-1] # Adds 0 for each day until the starting weekday of the month, after which it appends the date to each element of the list

    return dates