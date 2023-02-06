
'''
    AUTHOR: ramepetla@gmail.com
            R A M E S H P E T L A
            
     VERSION: 0.1

     This Script is tested on
              Windows 10 with Python 3.10.6

  **************************************************************************************************************
  *                                                                                                            *
  *  '_____'                    (\ _ /)        ^---^         _______                (____)                     *
  *   (O,O)      |><((('>       ( 'X' )       ( 'O' )        (' V ')                 (OO)                      *
  *   /)_)                      C(")(")       ( uuu )       ((_____))       /----------V                       *
  *     "                                                      ^ ^         /|         ||                       *
  *                                                                       ||         ||                        *
  *                                                                     ~~~~~~      ~~~~~~                     *
  **************************************************************************************************************
   
   USAGE:
   
   >
   
   Flow:

   > 


   KNOWN ISSUE 1: 

   >  If the Local Mount is Memory Card, then Format the Memory Card with ext4 and Populate entries in /etc/fstab e.g.,
      "/dev/mmcblk0p1  /media/ramesh/MMC_DATA ext4 defaults 0 0". Now change the Required Ownership with chown.
      Data Sync issues found with exFat Filesystem.
'''


import pikepdf, os, PyPDF2
from datetime import datetime


# INPUT

working_dir = 'C:\\My_Drive\\Temp\\pdf_documents_rename\\'
common_file_name = 'HSBC_Credit_Card_Statement'


# Function to Get TimeStamp

def current_timestamp():
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    return timestamp

# Log File Path Generation

log_file_path = 'C:\My_Drive\Workspace\backups\scripts\logs\\' + 'name_the_document_based_on_content' +'_' + current_timestamp() + '.log'


# Function to Exclude PDF Files with Specific Strings (from excluded_strings)

excluded_strings = ['excluded', 'decrypted', '.txt', '.xlsx', '.xls', 'renamed']

def excl_file_with_str(rec_file_name):
   
   string_match = [True for excluded_string in excluded_strings if excluded_string in rec_file_name]

   if True in string_match:
      return None
   else:
      return rec_file_name
      

# Get the File Names the Current Directory

pdf_files_raw = os.listdir(working_dir)

# Adding File Names (doesn't contain excluded strings) to List 

pdf_files = []

for pdf_file_raw in pdf_files_raw:
   file_name = excl_file_with_str(pdf_file_raw)

   if(file_name != None):
      pdf_files.append(file_name)


# PDF Passwords

pdf_passwords = ['300587995980', '300587041972', '300587891115', '1115rame3005']


# Function to Decrypt PDF Password. To Save PDF File without Password

def pdf_decrypt(pdf_file_path, file_no):

   for pdf_pass in pdf_passwords:
      
      try:
         source_pdf = pikepdf.open(pdf_file_path, password=pdf_pass)
         decrypt_pdf_name = working_dir + 'decrypted_' + str(file_no) + '.pdf'
         source_pdf.save(decrypt_pdf_name)
         return decrypt_pdf_name
         break
      except pikepdf._qpdf.PasswordError as err:
         continue

# Function to Read the Document

def pdf_extract_text(pdf_filename):

   # Creating PDF File Object
   pdfFileObj = open(pdf_filename, 'rb')

   # Creating PDF Reader Object
   pdfReaderObj = PyPDF2.PdfReader(pdfFileObj)

   # Creating First Page Object
   pdfFirstPageObj = pdfReaderObj.pages[0]

   # Extracing Text
   pdfExtractText = pdfFirstPageObj.extract_text()

   # Closing PDF File Object
   pdfFileObj.close()

   # Writing Extrated Text to File
   with open('extracted_pdf_text.txt', 'w') as tfile:
      tfile.write(pdfExtractText)
      tfile.close()
   
   # Reading Text File
   with open('extracted_pdf_text.txt', 'r') as tfile:
      lines = tfile.readlines()
      for line in lines:
         if 'To' in line:
            date_split = line.split()
   return date_split


# File Name Generation

short_months = { 'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12' }

def filename_creation(rec_list):
   
   try:
      from_month = short_months[rec_list[1]]
      to_month = short_months[rec_list[5]]
      file_name = working_dir + rec_list[2] + from_month + rec_list[0] + '_' + rec_list[6] + to_month + rec_list[4] + '_' + common_file_name + '.pdf'
      return file_name
   
   except KeyError as err:
      file_name = "unable_to_rename_"
      return file_name
   
# Rename the File

def file_rename(source_name, target_name):

   try:
      os.rename(source_name, target_name)
   
   except FileExistsError as err:
      print("File {} Already Exists".format(target_name))

# Loop through the files in the current directory

doc_no = 1

#logfile = open(log_file_path, "w")  # LOGGGING NOT HAPPENING

for pdf_file in pdf_files:

   print("Processing Document ", pdf_file)
   source_pdf_file_path = working_dir + pdf_file
   rename_source_pdf_file_path = working_dir + 'renamed_' + pdf_file
   decrypted_file_path = pdf_decrypt(source_pdf_file_path, doc_no)
   pdf_extracted_date_list = pdf_extract_text(decrypted_file_path)
   target_pdf_file_path = filename_creation(pdf_extracted_date_list)

   if 'unable_to_rename_' in target_pdf_file_path:
      rename_source_pdf_file_path = working_dir + 'unable_to_rename_' + pdf_file
   else:
      rename_source_pdf_file_path = rename_source_pdf_file_path

   file_rename(decrypted_file_path, target_pdf_file_path)
   file_rename(source_pdf_file_path, rename_source_pdf_file_path)
   doc_no = doc_no + 1

#logfile.close()