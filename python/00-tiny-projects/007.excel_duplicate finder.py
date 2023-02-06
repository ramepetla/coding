from time import sleep
from numpy.lib.function_base import diff
import pandas as pd

# Fetching Complete DATA from Excel Workbook

exception_records = pd.read_excel('C:\Accenture_Data\My Backup\Work\Accenture\Clients\Hersheys\PC & VM\Full Scan - PC - SUSE & RHEL - September 23rd 2021 - Exception & Solutions.xlsx', 
                    sheet_name='Need Approval', usecols="A:O",nrows=675,engine='openpyxl')


# Reading Required Rows and Adding to List

exceptions_2d_list = []

for index, rows in exception_records.iterrows():
    required_columns = [rows.Technology, rows.ControlID]
    exceptions_2d_list.append(required_columns)


# Converting List into Dictionary and Grouping them based on Operating Systems


exception_list_unsorted = {}

for key, values in exceptions_2d_list:
    if key in exception_list_unsorted.keys():
        exception_list_unsorted[key].append(int(values))
    else:
        exception_list_unsorted[key] = [int(values)]


# Sorting and Removing Duplicates


exception_list = {}

for key in exception_list_unsorted:
    trim_duplicates =list(set(exception_list_unsorted[key]))
    trim_duplicates.sort()
    exception_list[key] = trim_duplicates

'''
for key, values in exception_list.items():
    print(key, values)
'''
unique_control_ids = []

print("Unique Control IDs:")
for key, values in exception_list.items():
    for value in values:
        unique_control_ids.append(value)

unique_control_ids.sort()
print(list(set(unique_control_ids)))


# Fetching Complete DATA from Excel Workbook

solution_records = pd.read_excel('C:\Accenture_Data\My Backup\Work\Accenture\Clients\Hersheys\PC & VM\Full Scan - PC - SUSE & RHEL - September 23rd 2021 - Exception & Solutions.xlsx', 
                    sheet_name='Solutions', usecols="A:O",nrows=168,engine='openpyxl')


solutions_2d_list = []

for index, rows in solution_records.iterrows():
    required_columns = [rows.Technology, rows.ControlID]
    solutions_2d_list.append(required_columns)


# Converting List into Dictionary and Grouping them based on Operating Systems

solution_list_unsorted = {}


for key, values in solutions_2d_list:
    if key in solution_list_unsorted.keys():
        solution_list_unsorted[key].append(int(values))
    else:
        solution_list_unsorted[key] = [int(values)]

# Sorting and Removing Duplicates

solution_list = {}

for key in solution_list_unsorted:
    trim_duplicates =list(set(solution_list_unsorted[key]))
    trim_duplicates.sort()
    solution_list[key] = trim_duplicates

'''
for key, values in solution_list.items():
    print(key, values)
'''


# Fetching Complete DATA from Excel Workbook

report_records = pd.read_excel('C:\Accenture_Data\My Backup\Work\Accenture\Clients\Hersheys\PC & VM\Ad-hoc PC Scan Report.xlsx', 
                    sheet_name='PC', usecols="A:O",nrows=485,engine='openpyxl')


report_2d_list = []

for index, rows in report_records.iterrows():
    required_columns = [rows.Technology, rows.ControlID]
    report_2d_list.append(required_columns)


# Converting List into Dictionary and Grouping them based on Operating Systems

report_list_unsorted = {}

for key, values in report_2d_list:
    if key in report_list_unsorted.keys():
        report_list_unsorted[key].append(int(values))
    else:
        report_list_unsorted[key] = [int(values)]

# Sorting and Removing Duplicates

report_list = {}

for key in report_list_unsorted:
    trim_duplicates = list(set(report_list_unsorted[key]))
    trim_duplicates.sort()
    report_list[key] = trim_duplicates

# Final List After Exclusions

report_list_after_exclusion = {}


for key, values in report_list.items():
    to_exclude = exception_list.get(key)
    for value in values:
        if value not in to_exclude:
            if key in report_list_after_exclusion.keys():
                report_list_after_exclusion[key].append(int(value))
            else:
                report_list_after_exclusion[key] = [int(value)]


print("Fixed But FAILED")
print(report_list_after_exclusion)