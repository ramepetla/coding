import csv
import pygal
import pandas
from os import read
from datetime import datetime
import matplotlib.pyplot as plt
from modules.custom_functions import striphypen



filename = 'C:/Accenture_Data/Rapid/py_resources/money_expenses_selected.csv'

with open(filename, encoding="utf-8") as f:
    reader = csv.reader(f)
    header_row = next(reader)
    print(header_row)
 
    for index, column_header in enumerate(header_row):
        print(index, column_header)
    
    # Store CSV Data in List

    csv_rows = []
    for row in reader:
       csv_rows.append(row)

    
    # Making Sorted and Duplicates Removed Category List
    
    sub_category_dup_list = []
    sub_category_list = []      # Category List


    for csv_row in csv_rows:
        sub_category_dup_list.append(csv_row[8])
    
    for duplicate_category in sub_category_dup_list:
        if duplicate_category not in sub_category_list:
            sub_category_list.append(duplicate_category)

    sub_category_list.sort()


    # Fetching User Desired Category

    s_no = 1
    for sub_category in sub_category_list:
        print(s_no, sub_category)
        s_no = s_no + 1
    
    selected_sub_category = int(input("Select the Category: "))
    selected_sub_category = selected_sub_category - 1
    selected_sub_category = sub_category_list[selected_sub_category]

    # Loop through all Row in CSV. Fetch Only Rows which is having Desired sub_category String

    dates, amount = [], [] 
    for record in csv_rows:
        if selected_sub_category in record[8]:
            date_split = record[1].split()
            dates.append(datetime.strptime(date_split[0], "%m/%d/%Y"))

            # Whether to Pass the String to External Function or not

            if '-' in record[4]:
                amount.append(striphypen(record[4]))
            else:
                try:
                    amount.append(int(record[4]))
                except ValueError:
                    amount.append(int(float(record[4])))
    
    hist = pygal.Bar()

    hist.x_labels = [str(date) for date in dates]
    hist.add('D6', amount)
    hist.render_in_browser()
    
    '''
    
    # Plot Data

    fig = plt.figure(dpi=120, figsize=(15,12))
    plt.plot(dates, amount, c='blue')
  
    # Format Plot

    plt.title(selected_sub_category.upper(), fontsize=14)
    plt.xlabel('DATES', fontsize=14)
    fig.autofmt_xdate()
    plt.ylabel('AMOUNT', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=8)

    # Output the Plot

    plt.show()

'''