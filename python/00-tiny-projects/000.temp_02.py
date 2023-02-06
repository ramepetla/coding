import pikepdf, os, PyPDF2

# INPUT

working_dir = 'C:\\My_Drive\\Temp\\pdf_documents_rename\\'

# Function to Exclude PDF Files with Specific Strings

excluded_strings = ['excluded', 'decrypted', '.txt']

def excl_file_with_str(rec_file_name):
   
    string_match = [True for excluded_string in excluded_strings if excluded_string in rec_file_name]

    if True in string_match:
        return None
    else:
        return rec_file_name



      

# Get the Files in the Current Directory

pdf_files_raw = os.listdir(working_dir)

# Adding Files doesn't contain excluded strings to List 

pdf_files = []

for pdf_file_raw in pdf_files_raw:
   file_name = excl_file_with_str(pdf_file_raw)

   if(file_name != None):
      pdf_files.append(file_name)

print(pdf_files)


