#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# Folder Structure
# Z -> Settings ~ [branch]
#   Settings -> _settings
#   [branch] -> _log

#   [branch] -> [Project Folder] (i.e., ARC)
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
from print_notes import print_proj_notes
import task_selection
from print_notes import print_task_notes
import task_interface
import logit

# ------
# Runit
date    = datetime.today().strftime('%y-%m-%d')
logfile = 'log.txt'

# loadup
loadup.loadup()

# load settings
backup, main_dir, backup_dir, cur_branch_name = settings.settings()

# -------
# Loopit
exe_loop = True
while exe_loop:
    # check the cloud
    if backup:
        cloud_update.cloud_update(main_dir, backup_dir, cur_branch_name, logfile) #main dir, backup dir, branch, logfile name
    else: #no cloud access
        print('\nNot Connected to the Internet.\n')


    # ==================
    # Determine To-Do's
    # ==================
    # projects
    proj_path   = '%s/%s' %(main_dir, cur_branch_name)
    proj_list   = next(os.walk(proj_path))[1]

    job_loop = True
    while job_loop:
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
            #do something else?
            keep_working_loop = True
            while keep_working_loop:
                keep_working = raw_input('\nOK, is there something else that you would like to work on? (y/n): ')
                
                if (keep_working == 'y') or (keep_working == ''):
                    keep_working_loop = False
                elif keep_working == 'n':
                    exit()
                else: #wtf
                    print('\nThat don\'t make no sense! Try again.\n')
            #if going to do something else, need to restart back at the beginning of the loop
            if (keep_working == 'y') or (keep_working == ''):
                continue
            
        # ==========
        # Task Loop
        # ==========
        task_loop = True
        while task_loop:
            # print all project notes
            task_path, task_list, archive_task_list = print_proj_notes(proj_path, proj_name)

            # run task selection module
            task_name = task_selection.task_selection(archive_task_list, task_path, task_list, proj_path, proj_name)

            # determine if we need to go back to switch projects (searching through)
            if task_name == 'new_jobber':
                task_loop = False
                continue
            else:
                job_loop = False

            # ===========
            # List Notes
            # ===========
            # run notes module
            print_task_notes(task_path, task_name)

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
            logit.logit(proj_path, proj_name, task_path, task_name, time, notes, time_s, z_event, main_dir, logfile)

    # ---------------
    # check the cloud
    if backup:
        cloud_update.cloud_update(main_dir, backup_dir, cur_branch_name, logfile)
    else: #no cloud access
        print('\nNot able to backup because not connected to the Cloud.\n')

exit()