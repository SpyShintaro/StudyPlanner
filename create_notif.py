"""
create_notif

Author: Jake Hickey
Date: 31/07/2023
Description: A program to be run by task scheduler to make a notification on Windows
"""

from win10toast import ToastNotifier
import sys

def show_notif(args):
    """
    Automatic function to be called by the task scheduler task
    """
    toast = ToastNotifier()

    if args[2] == "":
        descr = "No description given"
    else:
        descr = args[2]

    toast.show_toast(
        args[1],
        descr,
        duration = 10,
        threaded = True
    )

    sys.exit()

if __name__ == "__main__":
    show_notif(sys.argv)