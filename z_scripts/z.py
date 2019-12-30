#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# Folder Structure
# Z -> Settings ~ [Segment]
#   Settings -> _settings
#   [Segment] -> _log

#   [Segment] -> [Project Folder] (i.e., ARC)
#       [Project folder] -> Active
#           Active -> [Task folder] (i.e., task_script)
#               [Task folder] -> [Task file] (i.e., 19_12_26_2320)
#       [Project folder] -> Archive
#           Archive -> {SAME AS ACTIVE}

# Capabilities 
# change basic settings
# update projects and tasks
# search projects and tasks
# present project/task statistics


# ================
# Import Packages
# ================
# date/time packages
import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta

# command line packages
import os
import sys
reload(sys) #to help with seemingly random'ascii' encoding error
sys.setdefaultencoding('utf8') # ^^ <--Python interpreter doesn't like it, but it works

# interface packages
import PySimpleGUI27 as sg
from PySimpleGUI27 import SetOptions

# other necessary packages
import filecmp

# import custom modules
import loadup
import settings
import cloud_update
import jobber
import task_selection
import print_notes
import task_interface
import logit

# ------
# Runit
date    = datetime.today().strftime('%y-%m-%d')
logfile = 'log.txt'

# loadup
loadup.loadup()

# load settings
backup, main_dir, backup_dir, cur_segment_name = settings.settings()

# -------
# Loopit
exe_loop = True
while exe_loop:
    # check the cloud
    if backup:
        cloud_update.cloud_update(main_dir, backup_dir, cur_segment_name, logfile) #main dir, backup dir, segment, logfile name
    else: #no cloud access
        print('\nNot Connected to the Internet.\n')


    # ==================
    # Determine To-Do's
    # ==================
    # projects
    proj_path   = '%s/%s' %(main_dir, cur_segment_name)
    proj_list   = next(os.walk(proj_path))[1]

    # list projects
    print('\nProjects:')
    for projects in proj_list:
        print('(%s) %s' %((proj_list.index(projects) + 1), projects))
    

    # ===========
    # Select Job
    # ===========
    # run job selection module
    proj_name = jobber.jobber(proj_list, proj_path, main_dir)
    
    if proj_name == 'SEARCH':
        break

    # ==========
    # Task Loop
    # ==========
    task_loop = True
    while task_loop:
        # run task selection module
        archive_task_list, task_path, task_name, task_list = task_selection.task_selection(proj_path, proj_name)


        # ===========
        # List Notes
        # ===========
        # run notes module
        print_notes.print_notes(archive_task_list, proj_path, proj_name, task_path, task_name, task_list)

        # ===============
        # Task Interface
        # ===============
        # run task interface module
        # do work!
        z_event, time, task_end, notes, time_s, proj_time = task_interface.task_interface(proj_name, task_name, proj_path)


        # ==========
        # Follow-up
        # ==========
        # in some instances, do a follow-up to determine if should keep working or shut it down
        follow_up_loop = True
        while follow_up_loop:
            # move completed project/task to archive folder
            if z_event == 'Project Complete':
                # move project to archive folder
                os.system('mv -v -f %s/%s %s/archive' %(proj_path, proj_name, main_dir))
            elif z_event == 'Task Complete':
                # move task to archive folder
                os.system('mv -v -f %s/%s %s/archive' %(task_path, task_name, task_path))

            # working on a new task?  
            follow_up = raw_input('\nKeep working? (y/n):  ')
            if (follow_up == '') or (follow_up == 'y'): #want to keep working
                follow_up_what_loop = True
                while follow_up_what_loop:
                    if z_event == 'Project Complete': #switch project
                        task_loop           = False
                        follow_up_loop      = False
                        follow_up_what_loop = False
                    else: #what to do?
                        follow_up_what = raw_input('Same project? (y/n):  ')
                        if (follow_up_what == '') or (follow_up_what == 'y'): #don't switch projects
                            follow_up_loop      = False
                            follow_up_what_loop = False

                        elif follow_up_what == 'n': #switch project
                            task_loop           = False
                            follow_up_loop      = False
                            follow_up_what_loop = False

                        else: #wtf
                            print('\nWait. That don\'t make no sense. Try again.\n')

            elif follow_up == 'n': #done with the sesh
                exe_loop        = False
                task_loop       = False
                follow_up_loop  = False
            else: #wtf
                print('\nWait. That don\'t make no sense. Try again.\n')


        # ==============
        # Log Responses
        # ==============
        # run logit module
        logit.logit(proj_path, proj_name, task_path, task_name, time, task_end, notes, time_s, proj_time, z_event, main_dir)

    # ---------------
    # check the cloud
    if backup:
        cloud_update.cloud_update(main_dir, backup_dir, cur_segment_name, logfile)
    else: #no cloud access
        print('\nNot able to backup because not connected to the Cloud.\n')

exit()