import os
from docx import Document
from docx.shared import Inches, Mm

# Install Moduel python-docx Instead of docx

'''
     Author:   ramepetla@gmail.com
               R A M E S H P E T L A
     Version: 0.1
     Python: 3.6.5
     USAGE: 
     Instructions: 
            Switch to Directory where Images are Stored
            Run the Python Script
     Dependancy: 
            python-docx 

'''

source_images = os.listdir('C:\img_to_doc\SUMA_RISE_DEPLOYMENT_1\\')

document = Document()

section = document.sections[0]
section.page_height = Mm(297)
section.page_width = Mm(210)
section.left_margin = Mm(25.4)
section.right_margin = Mm(25.4)
section.top_margin = Mm(25.4)
section.bottom_margin = Mm(25.4)
section.header_distance = Mm(12.7)
section.footer_distance = Mm(12.7)

for image in source_images:
    document.add_picture(image, width=Inches(6.0))

document_name = input("Enter Document Name: ")

document.save('C:\img_to_doc\\' + document_name + '.docx')