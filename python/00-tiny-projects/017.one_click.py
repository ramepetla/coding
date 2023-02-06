#!/usr/bin/env python3

'''
    AUTHOR: ramepetla@gmail.com
            R A M E S H P E T L A
            
     VERSION: 0.1

     This Script is tested on
              Pop!_OS 22.04 with Python 3.10.6

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
        1) Copies all Files and Folder from One Location to Another. This will create Duplicate Files in case
           of conflicts.

    KNOWN ISSUE 1: 
        If the Local Mount is Memory Card, then Format the Memory Card with ext4 and Populate entries in /etc/fstab e.g.,
        "/dev/mmcblk0p1  /media/ramesh/MMC_DATA ext4 defaults 0 0". Now change the Required Ownership with chown.
        Data Sync issues found with exFat Filesystem.
'''


'''
Tasks Include:

    Backup
    Reanme
    deletion
    moving data

Should scan the archives containing sample code (python, devops) under My_Work/Collections
to to_be_deleted/temp_code

all part of code should be in form of classes and functions    

'''
