#!/usr/bin/env python3

'''
    AUTHOR: ramepetla@gmail.com
            R A M E S H P E T L A
            
     VERSION: 0.1

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
        1) Copies Local Data to External HDD's on Demand.
        2) It won't delete any Files on External HDD if those files are not available in Local Direcotry

  KNOWN ISSUE 1: 
         
'''

from os.path import exists
import os, subprocess, time
from pickle import FALSE, TRUE
from socket import timeout
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from time import sleep
from datetime import date, datetime, time, sys
import logging


#+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~+~+~+~  HELP  +~+~++~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~ |

'''
sudo apt-get clean
sudo apt-get autoremove --purge
sudo apt-get autoremove

'''
#+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~+~+  USER INPUT  ~++~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~ |

backup_type = sys.argv[1]   # extdrv # intdrv

#+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~  GLOBAL VARIABLES  ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~ |

tmp_rsync_log = '/tmp/rsync.log'

log_file_location = '/Drives/My_Drive/My_Backup/Backups/Scripts/Logs/data_backup/'
log_file = log_file_location + 'data_backup_to_external_hdd_' + str(datetime.now().strftime("%Y-%m-%dT%H%M%S")) + '.log'
sys.stdout = open(log_file, 'w')

#+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+  DRIVE EXISTENCE  +~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~ |

# Mounting Filesystems (Internal Drives)

def internal_drives():

    is_it_mounted = os.system("df -h | grep gwshare")  # This is returning value 256, not sure WHY
    if is_it_mounted == 256:
        os.system("sudo mount -t cifs //192.168.1.1/G /gwshare/ -o 'rw,uid=1000,gid=1002,username=gwshare,password=SetSD23a3,vers=2.0'")

    is_it_mounted = os.system("df -h | grep MMC_DATA")  # This is returning value 256, not sure WHY
    if is_it_mounted == 256:
        os.system("sudo mount /dev/mmcblk0p1  /media/ramesh/MMC_DATA")
    
    is_it_mounted = os.system("df -h | grep gwshare")
    if is_it_mounted == 0:
        is_it_mounted = os.system("df -h | grep MMC_DATA")
        if is_it_mounted == 0:
            drives_existence = TRUE
        else:
            drives_existence = FALSE
    else:
        drives_existence = FALSE

    return drives_existence


# Availability Check (External Drives)

def external_drives():
   
    is_it_mounted = os.system("df -h | grep Passport")
    if is_it_mounted == 0:
        is_it_mounted = os.system("df -h | grep Movies")
        if is_it_mounted == 0:
            drives_existence = TRUE
        else:
            drives_existence = FALSE
    else:
        drives_existence = FALSE

    return drives_existence

#+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~  USER INPUT  +~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~ |

# Write JSON SCRIPT for INPUT

dirs_to_sync_ext =  { 
                    '/Drives/My_Drive/Rapid/': ['/Drives/My_Drive/My_Backup/Backups/Rapid/', ],
                    '/Drives/My_Drive/My_Backup/': ['/media/ramesh/Movies/Backups/Drives_Backup/My_Drive/My_Backup/',
                                                    '/media/ramesh/My Passport/Backups/Drives_Backup/My_Drive/My_Backup/' ],
                    '/Drives/My_Drive/Workspace/': ['/media/ramesh/Movies/Backups/Drives_Backup/My_Drive/Workspace/',
                                                    '/media/ramesh/My Passport/Backups/Drives_Backup/My_Drive/Workspace/' ],
                }

dirs_to_sync_int = {}

rsync_errors = [ 'error', 'permission', 'denied', 'failed']

dir_contents_to_deleted = [ ]

#+~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~  FUNCTIONS  ~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~ |

# To Get Timestamp

def get_timestamp():
    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    return current_timestamp


# RSYNC Job

def sync_dirs(dirs_to_sync):
    for key, values in dirs_to_sync.items():

        os.remove(tmp_rsync_log) if os.path.exists(tmp_rsync_log) else None

        for value in values:
            cmd = "rsync -azh --stats --log-file={}".format(tmp_rsync_log) + ' ' + "'{}'".format(key) + ' ' +"'{}'".format(value) + ' > ' + tmp_rsync_log
            subprocess.run(['{}'.format(cmd)], shell=True)
    
        rsync_log_file = open(tmp_rsync_log, "r")
        data = rsync_log_file.read()

        number_of_errors = 0
        
        for error in rsync_errors:
            if error in data:
                number_of_errors += 1
        
        number_of_errors = 5  # Remove this Line if Folder Contents Needs to Be Deleted. Once Script is STABLE

        if key in dir_contents_to_deleted and number_of_errors == 0 and backup_type == "extdrv": 
            print(get_timestamp(), "Proceeding with Deletion of Data in folder", key)
        else:
            print(get_timestamp(), "Total {} Error(s) found while Copying".format(number_of_errors), key)

        print(get_timestamp(), "Detailed RSYNC Log Messages")


        with open(tmp_rsync_log, 'r') as log_file:
            file_contents = log_file.read()
            print(file_contents)
        log_file.close()


#+~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~  EXECUTION  ~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~+~+~+~ | 

if backup_type == "extdrv":
    print("BACKUP TYPE IS ", backup_type)
    returned_value = external_drives()
    if returned_value == TRUE:
        sync_dirs(dirs_to_sync_ext)
    else:
        print(get_timestamp(), "The External Drives are not moutned")
else:
    returned_value = internal_drives()
    if returned_value == TRUE:
        sync_dirs(dirs_to_sync_int)
    else:
        print(get_timestamp(), "The Internal Drives are not mounted")



'''
Following should take backup to /Drives/My_Drive/My_backup/Backups

/home/ramesh/.vmware

/home/ramesh/.bash_aliases

/home/ramesh/.config/gtk-3.0

'''


