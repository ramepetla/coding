#!/usr/bin/env python3

'''
    AUTHOR: ramepetla@gmail.com
            R A M E S H P E T L A
            
     VERSION: 0.4

     This Script is tested on
              Pop!_OS 21.04 with Python 3.9.5

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
        1) Copies Data from One Location ot Other.

    KNOWN ISSUE 1: 
        If the Local Mount is Memory Card, then Format the Memory Card with ext4 and Populate entries in /etc/fstab e.g.,
        "/dev/mmcblk0p1  /media/ramesh/MMC_DATA ext4 defaults 0 0". Now change the Required Ownership with chown.
        Data Sync issues found with exFat Filesystem.
'''

from datetime import datetime
from sqlite3.dbapi2 import Cursor
from dirsync import sync
import os, shutil, sqlite3, pathlib, time, sys
import logging


#+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~  USER INPUT  +~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~ |

dirs_to_sync =  [ 
                  '/Drives/My Drive/My Backup/To Do',
                  '/Drives/My Drive/My Backup/My Profiles',
                  '/Drives/My Drive/My Backup/My Present Projects/My Work',
                  '/Drives/My Drive/My Backup/My Present Projects/Quick References',
                  '/Drives/My Drive/My Backup/Photos',
                  '/Drives/My Drive/My Backup/Database',
                  '/Drives/My Drive/My Backup/My Present Projects/Personal',
                  '/Drives/My Drive/Rapid',
                  '/Drives/My Drive/My Backup/My Present Projects/Work',
                  '/Drives/My Drive/My Backup/Backups', 
                ] 


# DIRECTORIES REVERSE SYNC: List of Directories which needs Data to be Synced from Target to Source

dirs_to_sync_reverse = [['/Drives/My Drive/Staging/Instant', '/gwshare/My Drive/Staging/Instant']]

# SYSTEM FILES: Systems Files Backup
# Destination: Linux_Rescue

system_files_backup_location = '/Drives/My Drive/My Backup/Backups/Linux_Rescue'

system_files = [ '/etc/fstab', '/etc/hosts', '/home/ramesh/.bash_history',
                 '/home/ramesh/.bash_aliases', '/etc/samba/smb.conf',
                 '/home/ramesh/.config/user-dirs.dirs']

# HISTORICAL FILES: Files Backup with History
# Destination: Historical_File_Backups

historical_files_backup_location = '/Drives/My Drive/My Backup/Backups/Historical_File_Backups/'

historical_files = [
                    '/Drives/My Drive/My Backup/To Do/Master.txt', 
                    '/Drives/My Drive/My Backup/To Do/Master.docx',
                    '/Drives/My Drive/My Backup/Database/SQLite/one_click_maintenance.db',
                   ] # Need to Find a way to pickup desired files having version number on Master Sheets


#+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~  GLOBAL VARIABLES  ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~ |

current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

log_file_location = '/Drives/My Drive/My Backup/Backups/Scripts/Logs/'
log_file = log_file_location + 'one_click_maintenance_' + current_timestamp + '.log'
sys.stdout = open(log_file, 'w')

files_to_copy = []   

#+~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~  FUNCTIONS  ~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~ |


# Target Path Generation

def path(file_path, search_root_dir, replace_root_dir):
    path = file_path.replace(search_root_dir, replace_root_dir)
    return path

# Parent Folder Extraction and Creation

def parent_folder(target_file):
            parent_folder = os.path.dirname(target_file)
            parent_folder = os.path.splitext(parent_folder) [0]
            pathlib.Path(parent_folder).mkdir(parents=True, exist_ok=True)
            #print("Creating Folder: ", parent_folder)  
            ''' 
             This Statement is there to check what is name of the folder it is trying to create. 
             It is observed that folder names containing dots are not able to create.
            '''

#+~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~  EXECUTION  ~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~ |

# Mounting Filesystems

is_it_mounted = os.system("df -h | grep gwshare")  # This is returning value 256, not sure WHY
if is_it_mounted == 256:
    os.system("sudo mount -t cifs //192.168.1.1/G /gwshare/ -o 'rw,uid=1000,gid=1002,username=gwshare,password=SetSD23a3,vers=2.0'")

is_it_mounted = os.system("df -h | grep MMC_DATA")  # This is returning value 256, not sure WHY
if is_it_mounted == 256:
    os.system("sudo mount /dev/mmcblk0p1  /media/ramesh/MMC_DATA")

# HISTORICAL FILES

for hist_file in historical_files:
    base = os.path.basename(hist_file)  # Extract only the Filename
    file_name = os.path.splitext(base) [0]
    file_extension = os.path.splitext(base) [1]
    shutil.copy(hist_file, historical_files_backup_location + file_name + '_' + current_timestamp + file_extension)
    
# SYSTEM FILES

for file in system_files:
    shutil.copy(file, system_files_backup_location)  # By Default, this will replace the File if it already exists


# BACKUPS TO LOCAL MEMORY CARD & GWSHARE

for dir in dirs_to_sync:
    with sqlite3.connect('/Drives/My Drive/My Backup/Database/SQLite/one_click_maintenance.db') as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS backup_data(file_name text NOT NULL,
                                                                modified_timestamp INT NOT NULL,
                                                                last_backup_status text NOT NULL);""")
        for root,dirs,files in os.walk(os.path.abspath(dir)):
            for file in files:
                source_file_path = os.path.join(root,file)
                source_file_mtime = int(os.path.getmtime(source_file_path))
                response = cursor.execute("SELECT EXISTS(SELECT 1 FROM backup_data WHERE file_name=?)", (source_file_path, )) # This will return value 1 if file_name found
                file_found = int(response.fetchone()[0])
                if file_found == 1:
                    fetched_record = cursor.execute("SELECT * FROM backup_data WHERE file_name=?", [source_file_path, ]).fetchall()  # This will return output in List of Tuples
                    for tuple in fetched_record:
                        recorded_timestamp = tuple[1]
                        if recorded_timestamp < source_file_mtime:
                            files_to_copy.append(source_file_path)
                else:
                    cursor.execute("INSERT INTO backup_data VALUES(?, ?, ?);", (source_file_path, 0, 'NA'))
                    files_to_copy.append(source_file_path)

# Files which needs to be Synced

        for source_file in files_to_copy:
            source_file_mtime = int(os.path.getmtime(source_file))
            gwshare_target_file = path(source_file, 'Drives', 'gwshare')
            mmc_target_file = path(source_file, '/Drives/', '/media/ramesh/MMC_DATA/')
            #gwshare_target_parent_folder = parent_folder(gwshare_target_file)
            mmc_target_parent_folder = parent_folder(mmc_target_file)
            try:
                #time.sleep(1)
                #print("Copying: ", source_file, " --> ", gwshare_target_file)
                #shutil.copyfile(source_file, gwshare_target_file)
                print("Copying: ", source_file, " --> ", mmc_target_file)
                shutil.copyfile(source_file, mmc_target_file)
            except FileNotFoundError:
                cursor.execute("UPDATE backup_data SET modified_timestamp=?, last_backup_status=? where file_name=?;", (0, 'NA', source_file))
            except PermissionError:
                cursor.execute("UPDATE backup_data SET modified_timestamp=?, last_backup_status=? where file_name=?;", (0, 'NA', source_file))
            if os.path.isfile(gwshare_target_file):
                cursor.execute("UPDATE backup_data SET modified_timestamp=?, last_backup_status=? where file_name=?;", (source_file_mtime, 'Done', source_file))
            else:
                cursor.execute("UPDATE backup_data SET modified_timestamp=?, last_backup_status=? where file_name=?;", (0, 'NA', source_file))
            db.commit()


# Changing Permissions

os.system("sudo chown -R ramesh:syncusers /Drives/*")
os.system("sudo chmod 775 -R /Drives/*")


# DIRECTORIES REVERSE SYNC

for dirs in dirs_to_sync_reverse:
    print("Syncing " + dirs[1] + " --> " + dirs[0])
    sync(dirs[1], dirs[0], 'sync')  


# Unmounting Filesystems

os.system("sudo umount -l /gwshare/")
os.system("sudo umount -l /media/ramesh/MMC_DATA")