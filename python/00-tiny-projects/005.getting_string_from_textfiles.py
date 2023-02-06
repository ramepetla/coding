import os

job_status_types = []
filelist = []

string = 'Final Job Status:'

files = os.listdir('.')

files.remove('plans')

for file in files:
    matching_line = [ line for line in open(file).readlines() if string in line ]  
    job_status_types += matching_line

job_status_types = list(set(job_status_types))

for status in job_status_types:
    print(status)