import os, time
with open("pdf.list", "w") as ofile: # ofile: output file
    for root, dirs, files in os.walk("/Drives/Downloads/Z-Book Library/Test/"):
        for f in files:
            ofile.write(f + '\n')
time.sleep(1)

list = [' ( PDFDrive.com )'] # list containing strings to be searched in line of pdf.list

with open('pdf.list') as oldfile, open('npdf.list', 'w') as newfile: # npdf is new file which contains lines having strings from list
    for l in oldfile:
        for word in list:
            if word in l:
                newfile.write(l)
time.sleep(1)
with open('npdf.list', "r") as filelist:
    for sfn in filelist:
        #nsfn = sfn.replace("\n","")
        src = sfn.replace("\n","")
        for string in list:
            tfn = sfn.replace(string,"") # Target File Name
            dst = tfn.replace("\n", "")
        os.rename(src,dst)
