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
local_folder = '/Users/zcole/Documents/file_drawer/dev/'
local_file   = 'zptz_local.xlsx'

try:
    cloud_folder = '/Users/zcole/Box/file_drawer/'
except IOError:
    print('\n* ***** *\nNOT CONNECTED TO BOX\n\nThis will not be backed up....yet\n* ***** *\n')
    backup  = False
else:
    cloud_folder = '/Users/zcole/Box/file_drawer/'
    backup  = True
    
local_file = '%s%s' %(local_folder, local_file)

wb_local = load_workbook(local_file)
ws_local = wb_local.active

# add headers
ws_local['A1'].value = 'Date'
ws_local['B1'].value = 'Time'
ws_local['C1'].value = 'Project'
ws_local['D1'].value = 'Project Status'
ws_local['E1'].value = 'Task'
ws_local['F1'].value = 'Task Status'
ws_local['G1'].value = 'Task Time (secs)'
ws_local['H1'].value = 'Notes'

wb_local.save(local_file)
wb_local.close()

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
    cloud_file   = 'zptz_cloud.xlsx'
    cloud_file  = '%s%s' %(cloud_folder, cloud_file)
    wb_cloud = load_workbook(cloud_file)
    ws_cloud = wb_cloud.active

    #input headers
    ws_cloud['A1'].value = 'Date'
    ws_cloud['B1'].value = 'Time'
    ws_cloud['C1'].value = 'Project'
    ws_cloud['D1'].value = 'Project Status'
    ws_cloud['E1'].value = 'Task'
    ws_cloud['F1'].value = 'Task Status'
    ws_cloud['G1'].value = 'Task Time (secs)'
    ws_cloud['H1'].value = 'Notes'

    # saveit
    wb_cloud.save(cloud_file)
    wb_cloud.close()

    # reactivate files
    wb_local
    ws_local
    wb_cloud
    ws_cloud

    #run initial backup
    print('\n-----\nChecking the cloud to make sure we are up to date. . . ')

    mrow = str(int(ws_local.max_row) + 1) 
    zmrow = range(2, int(mrow))
    mrow_cloud = str(int(ws_cloud.max_row) + 1)
    cloud_rows = range(2, int(mrow_cloud))

    # if date and time are missing from backup folder, initiate backup
    # HEADS UP: It feels backwards bc have to list items in backup, and compare them to the working file, but it is correct.

    #list all dates/times/notes in local doc
    al_list = []
    bl_list = []
    cl_list = []
    dl_list = []
    el_list = []
    fl_list = []
    gl_list = []
    hl_list = []
    
    for lrow in zmrow:
        al_list.append(ws_local['A%s' %lrow].value)
        bl_list.append(ws_local['B%s' %lrow].value)
        cl_list.append(ws_local['C%s' %lrow].value)
        dl_list.append(ws_local['D%s' %lrow].value)
        el_list.append(ws_local['E%s' %lrow].value)
        fl_list.append(ws_local['F%s' %lrow].value)
        gl_list.append(ws_local['G%s' %lrow].value)
        hl_list.append(ws_local['H%s' %lrow].value)

    local_list = [al_list, bl_list, cl_list, dl_list, el_list, fl_list, gl_list, hl_list]

    local_file_stuff = []
    for local_row in range(0, len(al_list)):
        local_row_list = []
        for local_columns in local_list:
            local_row_list.append(local_columns[local_row])
        local_thing = '%s%s%s%s%s%s%s%s' %(local_row_list[0], local_row_list[1], local_row_list[2], local_row_list[3], local_row_list[4], local_row_list[5], local_row_list[6], local_row_list[7])
        local_file_stuff.append(local_thing)

    # list all dates/times/notes in cloud doc
    ac_list = []
    bc_list = []
    cc_list = []
    dc_list = []
    ec_list = []
    fc_list = []
    gc_list = []
    hc_list = []

    for crow in cloud_rows:
        ac_list.append(ws_cloud['A%s' %crow].value)
        bc_list.append(ws_cloud['B%s' %crow].value)
        cc_list.append(ws_cloud['C%s' %crow].value)
        dc_list.append(ws_cloud['D%s' %crow].value)
        ec_list.append(ws_cloud['E%s' %crow].value)
        fc_list.append(ws_cloud['F%s' %crow].value)
        gc_list.append(ws_cloud['G%s' %crow].value)
        hc_list.append(ws_cloud['H%s' %crow].value)

    cloud_list = [ac_list, bc_list, cc_list, dc_list, ec_list, fc_list, gc_list, hc_list]

    cloud_file_stuff = []
    for cloud_row in range(0, len(ac_list)):
        cloud_row_list = []
        for cloud_columns in cloud_list:
            cloud_row_list.append(cloud_columns[cloud_row])
        cloud_thing = '%s%s%s%s%s%s%s%s' %(cloud_row_list[0], cloud_row_list[1], cloud_row_list[2], cloud_row_list[3], cloud_row_list[4], cloud_row_list[5], cloud_row_list[6], cloud_row_list[7])
        cloud_file_stuff.append(cloud_thing)

    for cloud_stuff in range(1, len(cloud_file_stuff)):
        if cloud_file_stuff[cloud_stuff] not in local_file_stuff:

            cloud_stuff += 2
            str(cloud_stuff)

            # activate for loop
            wb_local
            ws_local
            wb_cloud
            ws_cloud
            
            mrow = str(int(ws_local.max_row) + 1) 

            # log data
            ws_local['A%s' %mrow].value = ws_cloud['A%s' %cloud_stuff].value #date
            ws_local['B%s' %mrow].value = ws_cloud['B%s' %cloud_stuff].value #time
            ws_local['C%s' %mrow].value = ws_cloud['C%s' %cloud_stuff].value #proj
            ws_local['D%s' %mrow].value = ws_cloud['D%s' %cloud_stuff].value #proj_status
            ws_local['E%s' %mrow].value = ws_cloud['E%s' %cloud_stuff].value #task
            ws_local['F%s' %mrow].value = ws_cloud['F%s' %cloud_stuff].value #task_status
            ws_local['G%s' %mrow].value = ws_cloud['G%s' %cloud_stuff].value #times
            ws_local['H%s' %mrow].value = ws_cloud['H%s' %cloud_stuff].value #notes
                
            # save logged data
            wb_local.save(local_file)
            wb_local.close()
            wb_cloud.close()

        else:
            #reset
            wb_cloud.close()
            wb_local.close()
    #reset
    wb_cloud.close()

    print('\n-----\nThe system is up to date!\n')

else:
    print('\n-----\n Not connected to the cloud....\n')
    

# window
SetOptions(background_color = 'black', element_background_color = 'black',
           text_color = 'white', text_element_background_color = 'black',
           element_text_color = 'white', input_elements_background_color = 'black',
           input_text_color = 'white')

# runit
exe_loop = None
ploop = None
while exe_loop == None:

    wb_local #opening up new wb at beginning to account for newtask loop
    ws_local

    mrow = str(int(ws_local.max_row) + 1) 
    zmrow = range(2, int(mrow))

    #list projects
    project_list = []
    for zrow in zmrow:
        if ws_local['D%s' %zrow].value == 'oo':
            if ws_local['C%s' %zrow].value not in project_list:
                project_list.append(ws_local['C%s' %zrow].value)  

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
                                if ws_local['C%s' %zrow].value == proj:
                                    ws_local['D%s' %zrow].value = 'oo'
                                    wb_local.save(local_file)

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
        if ws_local['C%s' %zrow].value == proj:
            projnote_cell = ws_local['H%s' %zrow].value
            proj_task_cell = ws_local['E%s' %zrow].value
            proj_datetime_cell = str('%s %s' %(ws_local['A%s' %zrow].value, ws_local['B%s' %zrow].value))
            proj_task_list.append(proj_task_cell)
            proj_datetime_list.append(proj_datetime_cell)
            projnote_list.append(projnote_cell)

    project_notes = []
    if len(proj_task_list) > 0:
        print('\n-------------------------\n-------------------------\n    START %s NOTES\n-------------------------\n-------------------------' %proj.upper())
        # get all the notes written out
        for projn in range(0, len(proj_datetime_list)):
            project_note = '\n->%s /-/ %s\n%s' %(proj_task_list[projn], proj_datetime_list[projn], projnote_list[projn])
            if project_note not in project_notes:
                project_notes.append(project_note)
                print(project_note)
        print('\n-------------------------\n-------------------------\n    END %s NOTES\n-------------------------\n-------------------------\n' %proj.upper())

    # list tasks
    task_list = []
    for zrow in zmrow:
        if ws_local['C%s' %zrow].value == proj:
            if ws_local['F%s' %zrow].value == 'oo':
                if ws_local['E%s' %zrow].value not in task_list:
                    task_list.append(ws_local['E%s' %zrow].value)

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
                            if ws_local['E%s' %zrow].value == task:
                                if ws_local['C%s' %zrow].value == proj:
                                    if ws_local['D%s' %zrow].value == 'oo':
                                        ws_local['F%s' %zrow].value = 'oo'
                                        wb_local.save(local_file)

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
        if ws_local['C%s' %zrow].value == proj:
            if ws_local['E%s' %zrow].value == task:
                tasknote_cell = ws_local['H%s' %zrow].value
                task_datetime_cell = str('%s %s' %(ws_local['A%s' %zrow].value, ws_local['B%s' %zrow].value))
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
        if ws_local['C%s' %zrow].value == proj:
            ps = ws_local['G%s' %zrow].value
            if ps != None:
                proj_s += int(ps)

            if ws_local['E%s' %zrow].value == task:
                ts = ws_local['G%s' %zrow].value
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
            if ws_local['C%s' %zrow].value == proj:
                ws_local['D%s' %zrow].value = proj_status
                ws_local['F%s' %zrow].value = proj_status
    
    if p_values['taskip'] == True:
        task_status = 'oo'
    else:
        task_status = 'xx'
        for zrow in zmrow:
            if ws_local['E%s' %zrow].value == task:
                ws_local['F%s' %zrow].value = task_status

    notes = p_values['notes']

    # log local
    mrow = str(int(ws_local.max_row) + 1) 

    ws_local['A%s' %mrow].value = date
    ws_local['B%s' %mrow].value = time
    ws_local['C%s' %mrow].value = proj
    ws_local['D%s' %mrow].value = proj_status
    ws_local['E%s' %mrow].value = task
    ws_local['F%s' %mrow].value = task_status
    ws_local['G%s' %mrow].value = times
    ws_local['H%s' %mrow].value = notes

    #close it out
    wb_local.save(local_file)
    wb_local.close()

    # back it all up to the cloud by adding the missing input logs
    # this whole thing might seem a little weird, but if we are backing up, the backup file will actually be the working documents file
    if backup:
        print('\n-----\nEvaporating to the cloud. . . ')

        # if date and time are missing from backup folder, initiate backup
        # HEADS UP: It feels backwards bc have to list items in backup, and compare them to the working file, but it is correct.
        wb_local
        ws_local
        wb_cloud
        ws_cloud

        mrow = str(int(ws_local.max_row) + 1)
        zmrow = range(2, int(mrow))
        cloud_rows = range(2, int(mrow_cloud))

        #list all dates/times/notes in local doc
        al_list = []
        bl_list = []
        cl_list = []
        dl_list = []
        el_list = []
        fl_list = []
        gl_list = []
        hl_list = []
        
        for lrow in zmrow:
            al_list.append(ws_local['A%s' %lrow].value)
            bl_list.append(ws_local['B%s' %lrow].value)
            cl_list.append(ws_local['C%s' %lrow].value)
            dl_list.append(ws_local['D%s' %lrow].value)
            el_list.append(ws_local['E%s' %lrow].value)
            fl_list.append(ws_local['F%s' %lrow].value)
            gl_list.append(ws_local['G%s' %lrow].value)
            hl_list.append(ws_local['H%s' %lrow].value)

        local_list = [al_list, bl_list, cl_list, dl_list, el_list, fl_list, gl_list, hl_list]

        local_file_stuff = []
        for local_row in range(0, len(al_list)):
            local_row_list = []
            for local_columns in local_list:
                local_row_list.append(local_columns[local_row])
            local_thing = '%s%s%s%s%s%s%s%s' %(local_row_list[0], local_row_list[1], local_row_list[2], local_row_list[3], local_row_list[4], local_row_list[5], local_row_list[6], local_row_list[7])
            local_file_stuff.append(local_thing)

        # list all dates/times/notes in cloud doc
        ac_list = []
        bc_list = []
        cc_list = []
        dc_list = []
        ec_list = []
        fc_list = []
        gc_list = []
        hc_list = []

        for crow in cloud_rows:
            ac_list.append(ws_cloud['A%s' %crow].value)
            bc_list.append(ws_cloud['B%s' %crow].value)
            cc_list.append(ws_cloud['C%s' %crow].value)
            dc_list.append(ws_cloud['D%s' %crow].value)
            ec_list.append(ws_cloud['E%s' %crow].value)
            fc_list.append(ws_cloud['F%s' %crow].value)
            gc_list.append(ws_cloud['G%s' %crow].value)
            hc_list.append(ws_cloud['H%s' %crow].value)

        cloud_list = [ac_list, bc_list, cc_list, dc_list, ec_list, fc_list, gc_list, hc_list]

        cloud_file_stuff = []
        for cloud_row in range(0, len(ac_list)):
            cloud_row_list = []
            for cloud_columns in cloud_list:
                cloud_row_list.append(cloud_columns[cloud_row])
            cloud_thing = '%s%s%s%s%s%s%s%s' %(cloud_row_list[0], cloud_row_list[1], cloud_row_list[2], cloud_row_list[3], cloud_row_list[4], cloud_row_list[5], cloud_row_list[6], cloud_row_list[7])
            cloud_file_stuff.append(cloud_thing)

        for local_stuff in range(0, len(local_file_stuff)):
            if local_file_stuff[local_stuff] not in cloud_file_stuff:
                
                local_stuff += 2

                str(local_stuff)

                # activate for loop
                wb_local
                ws_local
                wb_cloud
                ws_cloud
                
                mrow_cloud = str(int(ws_cloud.max_row) + 1)

                # log data
                ws_cloud['A%s' %mrow_cloud].value = ws_local['A%s' %local_stuff].value #date
                ws_cloud['B%s' %mrow_cloud].value = ws_local['B%s' %local_stuff].value #time
                ws_cloud['C%s' %mrow_cloud].value = ws_local['C%s' %local_stuff].value #proj
                ws_cloud['D%s' %mrow_cloud].value = ws_local['D%s' %local_stuff].value #proj_status
                ws_cloud['E%s' %mrow_cloud].value = ws_local['E%s' %local_stuff].value #task
                ws_cloud['F%s' %mrow_cloud].value = ws_local['F%s' %local_stuff].value #task_status
                ws_cloud['G%s' %mrow_cloud].value = ws_local['G%s' %local_stuff].value #times
                ws_cloud['H%s' %mrow_cloud].value = ws_local['H%s' %local_stuff].value #notes
                    
                # save logged data
                wb_cloud.save(cloud_file)
                wb_cloud.close()
                wb_local.close()
            else:
                #reset
                wb_cloud.close()
                wb_local.close()

        print('\n-----\nThe system is successfully backed up!\n')

    else:
        #re-establish max row
        mrow = str(int(ws_local.max_row) + 1) 

        # log everything
        ws_local['A%s' %mrow].value = date
        ws_local['B%s' %mrow].value = time
        ws_local['C%s' %mrow].value = proj
        ws_local['D%s' %mrow].value = proj_status
        ws_local['E%s' %mrow].value = task
        ws_local['F%s' %mrow].value = task_status
        ws_local['G%s' %mrow].value = times
        ws_local['H%s' %mrow].value = notes

        #save logged data, close it down
        wb_local.save(local_file)
        wb_local.close()
        
        print('\n-----\nCould not backup to Box... will do next time (if connected).\n')

    # loop action
    if p_event == 'Dunzo':
        exe_loop = 1
    elif p_event == 'Switch Project':
        continue
    elif p_event == 'Switch Task':
        ploop = 1
        continue

# logout
exit()