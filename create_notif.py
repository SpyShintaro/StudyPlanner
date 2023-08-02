"""
create_notif

Author: Jake Hickey
Date: 31/07/2023
Description: A program to be run by task scheduler to make a notification on Windows
"""

from win10toast import ToastNotifier
import sys

def show_notif(args):
    toast = ToastNotifier()

    toast.show_toast(
        args[1],
        args[2],
        duration = 1,
        threaded = True
    )

    sys.exit()

if __name__ == "__main__":
    show_notif(sys.argv)