#!/usr/bin/python

import time
import os 
import glob 
import subprocess
import signal
import logging
import datetime

#Global variables; Adjustable parameters

main_folder = "pictures"
rootpath = "/home/pi/" + main_folder #place all folders and files will reside under

#Sets /home/pi/ as root

#Pull the current date from the calender, also the name of the folder under pictures

date_name = datetime.date.today() #pulls the current date and assigns it to variable date in YYYY-MM-DD format

date_name = date_name.strftime("%d-%m-%Y") #reformats the date to be DD-MM-YYYY 
date_folder = rootpath + "/" + date_name 

############session folder name is shared between scripts so that pictures will be placed into them
#session_folder_name = "sesh" #The name of the folder under date_name that will increment everytime the script is run
#session_folder = time.strftime("%H:%M:%S", time.localtime()) #displays 24 clock HH:MM:SS
#session_folder = date_folder + "/" + session_folder #need to condense this section

session_name = date_name + "%03d_" #Makes each session folder name read ###_DD-MM-YYYY
session_folder = date_folder + "/" + session_name #Location of the session folders

#picture_naming_scheme = "" #Determines the way pictures are named under session_folder_name
#division_cutoff = 10000 #Determines the heirarchy of picture folder divisions inside the session folder

digits = 3  #number of total digits to be used - fx. in front of session name
#glob_copy_path = ''

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

################# Functions ######################################################

#Check to see if 'pictures' folder exists in the rootpath
#Create the 'pictures' folder if it does not exist
#Check to see if today's date folder exists under 'pictures
#Create the date folder if it does not exist

def check_if_path_exists(root_path, pathway):  #takes pathway, checks list in that folder
	if not os.path.isdir(root_path):        #checks if root folder under /home/pi/ exists
		os.system('mkdir ' + root_path)
	if not os.path.isdir(pathway):		# checks if folder on system exists
		os.system('mkdir ' + pathway)	# creates folder if not there
	#if not os.path.isdir(pathway + "/001_" + date_name):
		
	else:
		return  			# if folders exist just exit function

def make_next_folder(path, digits):
	if os.listdir(path) == []:
		os.system('mkdir ' + path + "/" + date_name + "_" + "1".zfill(digits)) #create first session folder within the date folder if no folder exists
		session_name = date_name + "_" + "1".zfill(digits) #make session name DD-MM-YYYY_###
		return
	highest_item = str(sorted(os.listdir(path), reverse=False)[-1])
		# getting list of files/folders in path, sorting reverse order, taking highest)
	
	highest_item = highest_item[-digits:] #look at the highest session number, most recent. Add one and create new recent session folder
	next_num = int(highest_item) + 1
	session_name = date_name + "_" + str(next_num).zfill(digits)
	os.system('mkdir ' + path + "/" + session_name) 
		# makes  new folder by  passing 
		# shell command as string, folder name is ###_DD-MM-YYYY
	return
def get_session_name():
	if os.listdir(date_folder) == []:
		session_name = date_name + "_" + "1".zfill(digits) #used by another script to see the most recent session folder
	else:
		highest_item = str(sorted(os.listdir(date_folder), reverse=False)[-1])
		# getting list of files/folders in path, sorting reverse order, taking highest)
	
		highest_item = highest_item[-3:]
		next_num = int(highest_item) + 1
		session_name = date_name + "_" + str(next_num).zfill(digits)
	return session_name
#used by another script to retrieve the session folder location
def get_session_folder():
	session_name = get_session_name()
	session_folder = date_folder + "/" + session_name
	return session_folder



#Inside the date folder, create a new session folder that is incrementally greater than the latest session number
#Session folder name = date + 'ses' + session#


#Place pictures inside the session folder
#pictureName = session folder name + '%0000d.jpg'


##################Functions above, code below #####################

if __name__ == "__main__":
	check_if_path_exists(rootpath, date_folder) #check pictures folder and date folder make them if they are not there
	
	#make_next_folder(date_folder)
	#os.system('mkdir ' + date_folder + "/" + session_folder)
	#os.system('mkdir ' + session_folder)
	
	make_next_folder(date_folder, digits)


	
