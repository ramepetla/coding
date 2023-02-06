#!/usr/bin/python3.8
# The following script capture the details of Videos such as Title, Resoultion, Duration and Provides total duration fo the videos.
import cv2, math, os
dir = os.path.abspath(os.getcwd())
files = os.listdir(os.curdir)
videos = [['Title', 'Resolution', 'Duration']] # The next for loop will insert values "Title, Resolutions, Duration" in to this List
total_vid_sec = 0 

# --------------- Capturing details from Individual Videos
for f in files:
    vid = cv2.VideoCapture(f)
    fps = vid.get(cv2.CAP_PROP_FPS)  # Number of Frames Per Second of a Video 
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) # Total Number of Frames in the Video File
    frames_seconds = frame_count/fps
    total_vid_sec = total_vid_sec+frames_seconds
    minutes = str(int(frames_seconds/60))
    seconds = str(int(frames_seconds%60))
    duration = (minutes + 'm ' + seconds + 's')
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    height_in_num = math.trunc(height)
    width_in_num = math.trunc(width)
    Resolution = ''.join(map(str, [width_in_num, ' X ', height_in_num]))
    videos.append([f, Resolution, duration])
    vid.release()

# ----------------- Calculation for Total Duration of the Videos:

total_hours = 'to_cal_in_below'
total_minutes = 'to_cal_in_below'
total_seconds = 'to_cal_in_below'
if total_vid_sec <= 3600:
    total_hours = 'O'
    total_minutes = str(int(total_vid_sec/60))
    total_seconds = str(int(total_vid_sec%60))
else:
    total_hours = str(int(int(total_vid_sec/60)/60))
    total_minutes = str(int(total_vid_sec/60)%60)
    total_seconds = str(int(total_vid_sec%60))
total_duration = ''.join(map(str, [total_hours, ' hrs ', total_minutes, ' min ', total_seconds, ' sec']))

#  ------------------ Output Display in Tabular Form


dash = '-' * 115
for i in range(len(videos)):
    if i == 0:
        print(dash)
        print('{:<80s}{:>20s}{:>15s}' .format(videos[i][0], videos[i][1], videos[i][2]))
        print(dash)
    else:
        print('{:<80s}{:>20s}{:>15s}' .format(videos[i][0], videos[i][1], videos[i][2]))
print(dash)
print('{:<80s}{:>28s}' .format('Total Videos: ' + str(len(videos)-1), 'Total Duration: ' + total_duration ))
print(dash)


'''
------------ PENDING
Compare Video Titles with Text Doc
Unable to Retrieve Files from Sub-Folder. Getting an error, if folders contains sub-folders


'''

# Master Filename = "009.video_metadata.py"
# Path = /Drives/My Drive/My Backup/My Present Projects/My Work/Coding/Python