from datetime import datetime
import os, shutil, sqlite3, pathlib, time, sys
import logging

def current_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return timestamp


timestamp_now = current_timestamp()

log_file_location = 'C:\My_Drive\Workspace\backups\scripts\logs\\'
log_file = log_file_location + '_' + timestamp_now + '.log'
sys.stdout = open(log_file, 'w')

for i in range(0,20):
    print("Hello", i) 