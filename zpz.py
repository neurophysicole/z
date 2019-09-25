#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
from pyexcel_xlsx import save_data
import pyexcel as pe
import xlrd
import xlwt
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from openpyxl import worksheet
import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
import os
import sys
from collections import OrderedDict
import pandas as pd
from pandas import read_excel
from pyexcel._compact import OrderedDict
import xlsxwriter
import PySimpleGUI27 as sg
from PySimpleGUI27 import SetOptions

## Run this script in terminal `python 'name'.py`
## Everything is setup for Python version 2.7
## If using different version of python, may need to update packages/commands

## This script will open up an excel file, write the headers, and read the file
## First, will return the projects which are active
## --Choose by entering the corresponding number
## Will be followed by confirmation (pretty much everything is)
## --To confirm, enter 'y', or just hit 'Return'
## Once a project is selected (or input), all of the project notes will be listed in the terminal window
## Next, will return the tasks which are active
## -- task selection is same process as project selection
## NOTE: If type in a project or task name that is not active, this will re-activate the project/task
## Once a task is selected (or added), all of the task notes will be listed in the terminal window
## Also, a window will popup where project and task status can be updated, and notes can be added
## When the window pops up, a timer will also start in the top bar (if the application 'Thyme' is installed)
## If want to switch project or task, just click those selections when done
## If you intended to change the project or task status, be sure to do that first!!
## If you are done with the session, click Dunzo

## No matter the selection, after the popup window is closed, if Box is connected, the system will automatically compare the documents and backup any new items to the backup file.
## NOTE: This does mean that if running on separate computers, the logfiles on each computer coudl end up being slightly different.. but the backup will always hold all of the information.

## After backing everything up, the loop will continue as specified, or will terminate and close everything out.


# file parameters
folder = '/Users/zcole/Documents/file_drawer/dev/'
filex  = 'zptz.xlsx'

try:
    backup_folder = '/Users/zcole/Box/file_drawer/'
except IOError:
    print('\n* ***** *\nNOT CONNECTED TO BOX\n\nThis will not be backed up....yet\n* ***** *\n')
    backup  = False
else:
    backup_folder = '/Users/zcole/Box/file_drawer/'
    backup  = True
    
filename     = '%s%s' %(folder, filex)

# thymer scripts
open_thymer  = 'open -a Thyme'
start_thymer = 'osascript -e \'tell app "Thyme" to start\''
stop_thymer  = 'osascript -e \'tell app "Thyme" to stop\''
close_thymer = 'osascript -e \'quit app "Thyme"\''

# date/time parameters
date = datetime.today().strftime('%m/%d/%Y')
time = datetime.today().strftime('%-H:%M')

# activate project wb
# this may seem a little backwards, but an afterthought led me here, and this is where we are now....
if backup:
    backup_file  = '%s%s' %(backup_folder, filex)
    wb = load_workbook(backup_file)
    wb_backup = load_workbook(filename)
    ws_backup = wb_backup.active
    ws = wb.active

    #run initial backup
    print('\n-----\nChecking the cloud to make sure we are up to date. . . ')

    mrow = str(int(ws.max_row) + 1) 
    zmrow = range(2, int(mrow))
    backup_mrow = str(int(ws_backup.max_row) + 1)
    backup_rows = range(2, int(backup_mrow))

    # add headers
    ws_backup['A1'].value = 'Date'
    ws_backup['B1'].value = 'Time'
    ws_backup['C1'].value = 'Project'
    ws_backup['D1'].value = 'Project Status'
    ws_backup['E1'].value = 'Task'
    ws_backup['F1'].value = 'Task Status'
    ws_backup['G1'].value = 'Task Time (secs)'
    ws_backup['H1'].value = 'Notes'

    # if date and time are missing from backup folder, initiate backup
    # HEADS UP: It feels backwards bc have to list items in backup, and compare them to the working file, but it is correct.

    #list all dates and times
    d_list = []
    t_list = []
    n_list = []
    for dtnrow in zmrow:
        d_list.append(ws['A%s' %dtnrow].value)
        t_list.append(ws['B%s' %dtnrow].value)
        n_list.append(ws['H%s' %dtnrow].value)

    # get the rows to that need to be backed up
    backup_row_list = []
    for brow in backup_rows:
        backup_date = ws_backup['A%s' %brow].value
        backup_time = ws_backup['B%s' %brow].value
        backup_note = ws_backup['H%s' %brow].value
        if backup_date not in d_list:
            backup_row_list.append('%s' %brow)
        else: #if the date is in both lists
            dindex_list = [] #it is possible to have multiple postings on same date
            for backup_date in d_list:
                d_list_index = d_list.index(backup_date)
                dindex_list.append(d_list_index)
            if backup_time not in t_list:
                backup_row_list.append('%s' %brow)
            else:
                tmatch_list = []
                tindex_list = []
                for indeces in dindex_list:
                    tmatch = t_list[indeces]
                    tmatch_list.append(tmatch)
                    tindex = tmatch_list.index(indeces)
                    tindex_list.append(tindex)
                if backup_time not in tmatch_list:
                    backup_row_list.append('%s' %brow)
                else: #it is highly unlikely, but I suppose it may be possible that multiple postings could have the same date & time (quick note was made that took under a minute?). Either way, this can't hurt, right?
                    nmatch_list = []
                    for tindeces in t_list:
                        nmatch = n_list[tindeces]
                        nmatch_list.append(nmatch)
                    if backup_note not in nmatch_list:
                        backup_row_list.append('%s' %brow)

    #log backup
    for backup_row in backup_row_list:
        
        # activate for loop
        wb
        ws
        mrow

        # log data
        ws['A%s' %mrow].value = ws_backup['A%s' %backup_row].value #date
        ws['B%s' %mrow].value = ws_backup['B%s' %backup_row].value #time
        ws['C%s' %mrow].value = ws_backup['C%s' %backup_row].value #proj
        ws['D%s' %mrow].value = ws_backup['D%s' %backup_row].value #proj_status
        ws['E%s' %mrow].value = ws_backup['E%s' %backup_row].value #task
        ws['F%s' %mrow].value = ws_backup['F%s' %backup_row].value #task_status
        ws['G%s' %mrow].value = ws_backup['G%s' %backup_row].value #times
        ws['H%s' %mrow].value = ws_backup['H%s' %backup_row].value #notes
            
        # save logged data
        wb.save(backup_file)
        wb.close()

    #reset
    wb_backup.close()

    wb
    ws
    wb_backup
    ws_backup

    print('\n-----\nThe system is up to date!\n')

else:
    wb = load_workbook(filename)
    ws = wb.active

# add headers
ws['A1'].value = 'Date'
ws['B1'].value = 'Time'
ws['C1'].value = 'Project'
ws['D1'].value = 'Project Status'
ws['E1'].value = 'Task'
ws['F1'].value = 'Task Status'
ws['G1'].value = 'Task Time (secs)'
ws['H1'].value = 'Notes'

wb.save(filename)

# window
SetOptions(background_color = 'black', element_background_color = 'black',
           text_color = 'white', text_element_background_color = 'black',
           element_text_color = 'white', input_elements_background_color = 'black',
           input_text_color = 'white')

# runit
exe_loop = None
ploop = None
while exe_loop == None:

    wb #opening up new wb at beginning to account for newtask loop
    ws

    mrow  = str(int(ws.max_row) + 1) 
    zmrow = range(2, int(mrow))

    #list projects
    project_list = []
    for zrow in zmrow:
        if ws['D%s' %zrow].value == 'oo':
            if ws['C%s' %zrow].value not in project_list:
                project_list.append(ws['C%s' %zrow].value)  

    if ploop == None:
        print('\nProjects:')
        for project in project_list:
            print('(%s) %s' %(project_list.index(project), project))

        # determing project
        proj_loop = None
        while proj_loop == None:
            try:
                proj = int(raw_input('What do you want to work on? (Number): '))
            except ValueError:
                continue
            else:
                if 0 <= proj <= (len(project_list) - 1): 
                    proj = project_list[proj]
                else:
                    pjn_loop = None
                    while pjn_loop == None:
                        projyn = raw_input('New project? (y/n): ')
                        if (projyn == '') or (projyn == 'y'):
                            proj = raw_input('Project Name: ')
                            project_list.append(proj)
                            pjn_loop = 1

                            #if a 'completed' project is being re-activated
                            for zrow in zmrow:
                                if ws['C%s' %zrow].value == proj:
                                    ws['D%s' %zrow].value = 'oo'
                                    wb.save(filename)

                        elif projyn == 'n':
                            continue
                        else:
                            pjn_loop = None

            pl_loop = None
            while pl_loop == None:
                proj_l = raw_input('%s? (y/n): ' %proj)
                if (proj_l == '') or (proj_l == 'y'):
                    proj_loop = 1
                    pl_loop = 1
                elif proj_l == 'n':
                    pl_loop = 1
                else:
                    pl_loop = None

    else:
        ploop = None

    # project notes
    proj_task_list = []
    proj_datetime_list = []
    projnote_list = []
    for zrow in zmrow:
        if ws['C%s' %zrow].value == proj:
            projnote_cell = ws['H%s' %zrow].value
            proj_task_cell = ws['E%s' %zrow].value
            proj_datetime_cell = str('%s %s' %(ws['A%s' %zrow].value, ws['B%s' %zrow].value))
            proj_task_list.append(proj_task_cell)
            proj_datetime_list.append(proj_datetime_cell)
            projnote_list.append(projnote_cell)

    project_notes = []
    if len(proj_task_list) > 0:
        print('\n-------------------------\n-------------------------\n    START %s NOTES\n-------------------------\n-------------------------' %proj.upper())
        # get all the notes written out
        for projn in range(0, len(proj_datetime_list)):
            project_note = str('\n->%s /-/ %s\n%s' %(proj_task_list[projn], proj_datetime_list[projn], projnote_list[projn]))
            if project_note not in project_notes:
                project_notes.append(project_note)
                print(project_note)
        print('\n-------------------------\n-------------------------\n    END %s NOTES\n-------------------------\n-------------------------\n' %proj.upper())

    # list tasks
    task_list = []
    for zrow in zmrow:
        if ws['C%s' %zrow].value == proj:
            if ws['F%s' %zrow].value == 'oo':
                if ws['E%s' %zrow].value not in task_list:
                    task_list.append(ws['E%s' %zrow].value)

    print('Tasks:')
    for tasks in task_list:
        print('(%s) %s' %(task_list.index(tasks), tasks))

    # task
    task_loop = 'n'
    while task_loop == 'n':
        try:
            task = int(raw_input('\nTask: #'))
        except ValueError:
            continue
        else:
            if 0 <= task <= (len(task_list) - 1):
                task = task_list[task]
            else:
                tyn_loop = None
                while tyn_loop == None:  
                    taskyn = raw_input('New task? (y/n): ')
                    if (taskyn == '') or (taskyn == 'y'):
                        task = raw_input('Task Name: ')
                        task_list.append(task)
                        tyn_loop = 1

                        #if a 'completed' task is being re-activated
                        for zrow in zmrow:
                            if ws['E%s' %zrow].value == task:
                                if ws['C%s' %zrow].value == proj:
                                    if ws['D%s' %zrow].value == 'oo':
                                        ws['F%s' %zrow].value = 'oo'
                                        wb.save(filename)

                    elif taskyn == 'n':
                        continue
                    else:
                        tyn_loop = None
        
        tl_loop = None
        while tl_loop == None:
            task_l = raw_input('%s? (y/n): ' %task)
            if (task_l == '') or (task_l == 'y'):
                task_loop = 1
                tl_loop = 1
            elif task_l == 'n':
                tl_loop = 1
                continue
            else:
                tl_loop = None
            
    # task notes
    tasknote_list = []
    task_datetime_list = []
    for zrow in zmrow:
        if ws['C%s' %zrow].value == proj:
            if ws['E%s' %zrow].value == task:
                tasknote_cell = ws['H%s' %zrow].value
                task_datetime_cell = str('%s %s' %(ws['A%s' %zrow].value, ws['B%s' %zrow].value))
                tasknote_list.append(tasknote_cell)
                task_datetime_list.append(task_datetime_cell)

    task_notes = []
    if len(tasknote_list) > 0:
        print('\n->%s\n' %task.upper())
        # get all the notes written out
        for taskn in range(0, len(task_datetime_list)):
            task_note = str('\n%s\n%s\n\n' %(task_datetime_list[taskn], tasknote_list[taskn]))
            if task_note not in task_notes:
                task_notes.append(task_note)
                print(task_note)

    # timing calculations
    proj_s = 0
    proj_time = 0
    proj_hours = 0
    proj_mins = 0
    task_s = 0
    task_time = 0
    task_mins = 0
    task_hours = 0
    for zrow in zmrow:
        if ws['C%s' %zrow].value == proj:
            ps = ws['G%s' %zrow].value
            if ps != None:
                proj_s += int(ps)

            if ws['E%s' %zrow].value == task:
                ts = ws['G%s' %zrow].value
                if ts != None:
                    task_s += int(ts)
    
    if proj_s > 0:
        proj_hours = proj_s/3600
        proj_mins = (proj_s%3600)/60

        proj_time = '{h}h {m}m'.format(h = proj_hours, m = proj_mins)

    if task_s > 0:
        task_hours = task_s/3600
        task_mins = (task_s%3600)/60
        task_time = '{h}h {m}m'.format(h = task_hours, m = task_mins)

    # task timer
    task_start = datetime.now()
    
    os.system(close_thymer)
    os.system(open_thymer)
    os.system(start_thymer)

    # window
    p_window = sg.Window(str('%s: %s' %(date, time)))
    p_layout = [[sg.Frame(layout = [[sg.Text('%s' %proj), sg.Text('%s' %proj_time)], [sg.Radio('In Progress', "projp", key = 'projip', default = True), sg.Radio('Completed', "projp")]], title = 'Project', relief = sg.RELIEF_SUNKEN)], [sg.Frame(layout = [[sg.Text('%s' %task), sg.Text('%s' %task_time)], [sg.Radio('In Progress', "taskp", key = 'taskip', default = True), sg.Radio('Completed', "taskp")]], title = 'Task', relief = sg.RELIEF_SUNKEN)], [sg.Multiline(size = (50,5), key = 'notes', autoscroll = True, default_text = '----------\n')], [sg.CloseButton('Switch Project'), sg.CloseButton('Switch Task'), sg.CloseButton('Dunzo')]]

    p_event, p_values = p_window.Layout(p_layout).Read()

    # task timer
    task_end = datetime.now()
    timex    = relativedelta(task_end, task_start)

    # time calculations
    timeh = '{h}'.format(h = timex.hours)
    timem = '{m}'.format(m = timex.minutes)
    times = '{s}'.format(s = timex.seconds)

    timeh = int(timeh)*3600
    timem = int(timem)*60

    times = int(times)+timeh+timem

    os.system(stop_thymer)
    os.system(close_thymer)

    # input values
    if p_values['projip'] == True:
        proj_status = 'oo'
    else:
        proj_status = 'xx'
        for zrow in zmrow:
            if ws['C%s' %zrow].value == proj:
                ws['D%s' %zrow].value = proj_status
                ws['F%s' %zrow].value = proj_status
    
    if p_values['taskip'] == True:
        task_status = 'oo'
    else:
        task_status = 'xx'
        for zrow in zmrow:
            if ws['E%s' %zrow].value == task:
                ws['F%s' %zrow].value = task_status

    notes = p_values['notes']

    # back it all up to the cloud by adding the missing input logs
    # this whole thing might seem a little weird, but if we are backing up, the backup file will actually be the working documents file
    if backup:
        print('\n-----\nEvaporating to the cloud. . . ')

        # activate local file
        wb_backup
        ws_backup

        backup_mrow = str(int(ws_backup.max_row) + 1)
        backup_rows = range(2, int(backup_mrow))

        # add headers
        ws_backup['A1'].value = 'Date'
        ws_backup['B1'].value = 'Time'
        ws_backup['C1'].value = 'Project'
        ws_backup['D1'].value = 'Project Status'
        ws_backup['E1'].value = 'Task'
        ws_backup['F1'].value = 'Task Status'
        ws_backup['G1'].value = 'Task Time (secs)'
        ws_backup['H1'].value = 'Notes'

        # log data
        ws_backup['A%s' %backup_mrow].value = date
        ws_backup['B%s' %backup_mrow].value = time
        ws_backup['C%s' %backup_mrow].value = proj
        ws_backup['D%s' %backup_mrow].value = proj_status
        ws_backup['E%s' %backup_mrow].value = task
        ws_backup['F%s' %backup_mrow].value = task_status
        ws_backup['G%s' %backup_mrow].value = times
        ws_backup['H%s' %backup_mrow].value = notes

        # save what is logged
        wb_backup.save(backup_file)
        wb_backup.close()

        # if date and time are missing from backup folder, initiate backup
        # HEADS UP: It feels backwards bc have to list items in backup, and compare them to the working file, but it is correct.
        wb_backup
        ws_backup

        #list all dates and times
        d_list = []
        t_list = []
        n_list = []
        for dtnrow in zmrow:
            d_list.append(ws['A%s' %dtnrow].value)
            t_list.append(ws['B%s' %dtnrow].value)
            n_list.append(ws['H%s' %dtnrow].value)

        # get the rows to that need to be backed up
        backup_row_list = []
        for brow in backup_rows:
            backup_date = ws_backup['A%s' %brow].value
            backup_time = ws_backup['B%s' %brow].value
            backup_note = ws_backup['H%s' %brow].value
            if backup_date not in d_list:
                backup_row_list.append('%s' %brow)
            else: #if the date is in both lists
                dindex_list = [] #it is possible to have multiple postings on same date
                for backup_date in d_list:
                    d_list_index = d_list.index(backup_date)
                    dindex_list.append(d_list_index)
                if backup_time not in t_list:
                    backup_row_list.append('%s' %brow)
                else:
                    tmatch_list = []
                    tindex_list = []
                    for indeces in dindex_list:
                        tmatch = t_list[indeces]
                        tmatch_list.append(tmatch)
                        tindex = tmatch_list.index(indeces)
                        tindex_list.append(tindex)
                    if backup_time not in tmatch_list:
                        backup_row_list.append('%s' %brow)
                    else: #it is highly unlikely, but I suppose it may be possible that multiple postings could have the same date & time (quick note was made that took under a minute?). Either way, this can't hurt, right?
                        nmatch_list = []
                        for tindeces in t_list:
                            nmatch = n_list[tindeces]
                            nmatch_list.append(nmatch)
                        if backup_note not in nmatch_list:
                            backup_row_list.append('%s' %brow)

        #log backup
        for backup_row in backup_row_list:
            
            # activate for loop
            wb
            ws
            mrow

            # log data
            ws['A%s' %mrow].value = ws_backup['A%s' %backup_row].value #date
            ws['B%s' %mrow].value = ws_backup['B%s' %backup_row].value #time
            ws['C%s' %mrow].value = ws_backup['C%s' %backup_row].value #proj
            ws['D%s' %mrow].value = ws_backup['D%s' %backup_row].value #proj_status
            ws['E%s' %mrow].value = ws_backup['E%s' %backup_row].value #task
            ws['F%s' %mrow].value = ws_backup['F%s' %backup_row].value #task_status
            ws['G%s' %mrow].value = ws_backup['G%s' %backup_row].value #times
            ws['H%s' %mrow].value = ws_backup['H%s' %backup_row].value #notes
                
            # save logged data
            wb.save(backup_file)
            wb.close()

        #close it down
        wb_backup.close()

        print('\n-----\nThe system is successfully backed up!\n')

    else:
        #re-establish max row
        mrow

        # log everything
        ws['A%s' %mrow].value = date
        ws['B%s' %mrow].value = time
        ws['C%s' %mrow].value = proj
        ws['D%s' %mrow].value = proj_status
        ws['E%s' %mrow].value = task
        ws['F%s' %mrow].value = task_status
        ws['G%s' %mrow].value = times
        ws['H%s' %mrow].value = notes

        #save logged data, close it down
        wb.save(filename)
        wb.close()
        
        print('\n-----\nCould not backup to Box... will do next time (if connected).\n')

    # loop action
    if p_event != 'Switch Project':
        ploop = 1
    else:
        ploop = None

    if (p_event != 'Switch Task') or (p_event == 'Dunzo'):
        exe_loop = 1

# logout
exit()