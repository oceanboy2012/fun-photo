#!/usr/bin/python

import time
import os 
import glob 
import subprocess
import signal
import logging
import picamera


rootpath = '/home/pi/foto_dump/'
dirpath = '/home/pi/foto_dump/images/' #set working folder (directory)
temp_path = '/home/pi/foto_dump/temp/' #set temporary folder for each sessions 4 pictures
max_photos = 8
max_photos_per_session = 4
pics_per_group = 4
slideshow_duration = 8
glob_copy_path = ''

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

def check_if_path_exists(root_path, pathway, temporary_path, start_name):  #takes pathway, checks list in that folder
	if not os.path.isdir(root_path):        #checks if root folder under /home/pi/ exists
		os.system('mkdir ' + root_path)
	if not os.path.isdir(pathway):		# checks if folder on system exists
		os.system('mkdir ' + pathway)	# creates folder if not there
	if not os.path.isdir(temporary_path):   #checks if tmp folder exists in root working folder
		os.system('mkdir ' + temporary_path)
	
	pathway_list = os.listdir(pathway)	# gets content of pathway
	if not pathway_list:			# if no folders make first folder
		os.system('mkdir ' + pathway + start_name)
	else:
		return  			# if folders exist just exit function

def make_next_folder(path, root_name, digits):
	highest_item = sorted(os.listdir(path), reverse=False)[-1] 
		# getting list of files/folders in path, sorting reverse order, taking highest)
	num_in_highest = int(''.join(i for i in highest_item if i in "0123456789")) 
		# this grabs only the number out of variable highest_item, which is a folder
	    	# and  makes  num_in_highest  an integer
	next_num = str(num_in_highest + 1).zfill(digits) 
		# set next_num var to one number higher and with 3 digits including leading zeros
	os.system('mkdir ' + path + root_name + next_num) 
		# makes  new folder by  passing 
		# shell command as string, folder name is 'string' + next_num
	return


#####-FUNCTIONS TO CHANGE NUMBER ON PICTURE-#####

#this function counts the number of photos in the temp folder then moves them to 
#highest session folder if the number is greater than or equal to the max_photo_count variable set globally
	
def move_temp_photos(high_session_path, max_photo_count, temporary_path):
	temp_list = os.listdir(temporary_path)
	count = len(temp_list)  
	if count >= max_photo_count:
		for i in temp_list:
			os.system('mv ' + temporary_path + i + ' ' + high_session_path + i)
	return


#pass highest session path variable to session
# folder based on folder session pathway
#if there are no files(photos) in folder path, make photo 00001
# returning first photo path ( of session folder with added session0000?_00001.jpg)
# if there are files in highest session path
#gives us session0000?_0000highest

def change_photo_num(high_session_path, digits, temporary_path):    
                                               
	global glob_copy_path    
	if not os.listdir(temporary_path): 
		if not os.listdir(high_session_path):   
			glob_copy_path = temporary_path + 'session' + high_session_path[-6:-1] + '_00001.jpg' 
			return temporary_path + 'session' + high_session_path[-6:-1] + '_00001.jpg'   
		else:      
			highest_photo = sorted(os.listdir(high_session_path), reverse=False)[-1] 
			next_photo_num = str(int(highest_photo[-9:-4]) + 1).zfill(digits)   
			glob_copy_path = temporary_path + 'session' + high_session_path[-6:-1] + '_' + next_photo_num + '.jpg'
			return temporary_path + 'session' + high_session_path[-6:-1] + '_' + next_photo_num + '.jpg'
	else:            
		highest_photo = sorted(os.listdir(temporary_path), reverse=False)[-1] 
		next_photo_num = str(int(highest_photo[-9:-4]) + 1).zfill(digits)   
		glob_copy_path = temporary_path + 'session' + high_session_path[-6:-1] + '_' + next_photo_num + '.jpg'
		return temporary_path + 'session' + high_session_path[-6:-1] + '_' + next_photo_num + '.jpg'


###########-PHOTO MANIPULATION FUNCTIONS-############

def capture(name):
        name = str(name)
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            # Camera warm-up time
            time.sleep(2)
            camera.capture(temp_path + name + '.jpg')


def slideshow_photos(folder_path, total_time_seconds):

	time_between_photos = total_time_seconds/len(os.listdir(folder_path))
	    # look at using a try except else statement here to prevent division by zero or a string entry
		
#	os.system('xterm -e eog -s -f ' + folder_path)
	os.system('eog -f -s ' + folder_path)
#	time.sleep(5)
	
	
	return

# def reduce_files(path, start_num) # this uses ffmpeg to reduce all the files in passed folder and names them 


def copy_temp(path, number):  # copies all files in folder to 1...3.jpg 
	listed = os.listdir(path)
	for i in listed:
		os.system( 'cp ' + path + '/' + i + ' ' + path + '/'  + str(number) + '.jpg')
		number = number + 1


def delete_files(path):           #function to delete duplicate photos 1.jpg to 4.jpg 
	for i in range(1,5):           #goes through range from 1 to 4
		os.system('rm ' + path + str(i) + '.jpg')         #removes/deletes photos



###################_FUNCTIONS ABOVE_##################################



check_if_path_exists(rootpath, dirpath, temp_path, 'session00001')

folder_list =  os.listdir(dirpath)   # get global folder contents in list (folders & files)


  

sorted_list =  sorted(folder_list, reverse=False)  #sorts list from lowest to highest and alphabetical

highest = sorted_list[-1] # takes last item in list, which is highest since it was sorted 


### count number of files in highest numbered folder ###

high_path = dirpath + highest + '/'
highest_folder_file_count = len(os.listdir(high_path))

 
if highest_folder_file_count >= max_photos:
	make_next_folder(dirpath, 'session',5)
	folder_list =  os.listdir(dirpath)
	highest = sorted(folder_list, reverse=False)[-1]  #need to now rename highest(folder) as newly created folder,
			# so we can now have that as folder in which to put photos
	high_path = dirpath + highest + '/'

move_temp_photos(high_path, 1,temp_path) # safety check move any photos in the temp folder into highest session folder

temp_x = 1 # count variable for while loop, photo group

while temp_x <= pics_per_group:

	time.sleep(1)
	capture(temp_x) #take the pictures with Picamera funtion
	time.sleep(1)


	temp_x = temp_x + 1



copy_temp(temp_path,1) # takes a folder path and lists contents then copies each starting with 1.jpg ... up
time.sleep(2.6)
subprocess.Popen(['chromium-browser', '--kiosk','/home/pi/git/flasksimple_slideshow.html'], #open browser in subpross
	stdout=open('/dev/null', 'w'),
	stderr=open ('logfile.log', 'a'))



time.sleep(9)	

#slideshow_photos(temp_path, slideshow_duration)

#os.system( 'chromium-browser --kiosk /home/pi/photobooth/simple_slideshow.html') 


move_temp_photos(high_path, max_photos_per_session,temp_path)     #moves temp photos to permanent folder

delete_files(temp_path)          #function deletes duplicate photos 1.jpg to 4.jpg using temp_path folder
