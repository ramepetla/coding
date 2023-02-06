from datetime import datetime
import os, shutil
# GLOBAL Declerations
# cts = Current Time Stamp
cts = datetime.now().strftime("%Y%m%d_%H%M%S")
# END OF GLOBAL Declerations 
# Backup of Files to Other Locations 
# bakfiles = backup files
bakfiles = open("/Drives/My Drive/My Backup/File & Settings Backup/Scripts/Input/backupfilelist.txt" , "r+")
# bf = backup files
for bf in bakfiles:
    # nfn = New File Name
    nfn = bf.replace("\n", "") # here new lines will be replaced, otherwise, each line will bring new line along with it
    base = os.path.basename(nfn)
    # fn = File Name  |  fe = File Extension
    fn = os.path.splitext(base) [0]
    fe = os.path.splitext(base) [1]
    # bl = Backup Location
    bl = '/Drives/My Drive/My Backup/File & Settings Backup/File Backups/Important Files/'
    shutil.copy(nfn, bl +  'backup' + '_' +fn + '_' + cts + fe)
# END OF Backup of Files to Other Locations
#-----------------------------------------------------------------------------------------------------#

