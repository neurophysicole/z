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

# file parameters
try:
    folder   = '/Users/zcole/Box/file_drawer/'
except IOError:
    print('\n* ***** *\nNOT CONNECTED TO BOX\n* ***** *\n')
    folder   = '/Users/zcole/Documents/file_drawer/dev/'
else:
    folder   = '/Users/zcole/Box/file_drawer/'
    
filename     =  str(folder + 'zptz.xlsx')

# thymer scripts
open_thymer  = 'open -a Thyme'
start_thymer = 'osascript -e \'tell app "Thyme" to start\''
stop_thymer  = 'osascript -e \'tell app "Thyme" to stop\''
close_thymer = 'osascript -e \'quit app "Thyme"\''

# date/time parameters
date = datetime.today().strftime('%m/%d/%Y')
time = datetime.today().strftime('%-H:%M')

# activate project wb
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

    mrow = str(int(ws.max_row) + 1) 
    zmrow = range(2, int(mrow) - 1)

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
                        if projyn == '':
                            proj = raw_input('Project Name: ')
                            project_list.append(proj)
                            pjn_loop = 1

                            #if a 'completed' project is being re-activated
                            for zrow in zmrow:
                                if ws['C%s' %zrow].value == proj:
                                    ws['D%s' %zrow].value = 'oo'

                        elif projyn == 'n':
                            continue
                        else:
                            pjn_loop = None

            pl_loop = None
            while pl_loop == None:
                proj_l = raw_input('%s? (y/n): ' %proj)
                if proj_l == '':
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
                    if taskyn == '':
                        task = raw_input('Task Name: ')
                        task_list.append(task)
                        tyn_loop = 1
                    elif taskyn == 'n':
                        continue
                    else:
                        tyn_loop = None
        
        tl_loop = None
        while tl_loop == None:
            task_l = raw_input('%s? (y/n): ' %task)
            if task_l == '':
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
            if zrow > 1:
                ps = ws['G%s' %zrow].value
                if ps != None:
                    proj_s += int(ps)/9
                else:
                    proj_s += 0

                if ws['E%s' %zrow].value == task:
                    if zrow > 1:
                        ts = ws['G%s' %zrow].value
                        if ts != None:
                            task_s += int(ts)/9
                        else:
                            task_s += 0
    
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

    # log everything
    ws['A%s' %mrow].value = date
    ws['B%s' %mrow].value = time
    ws['C%s' %mrow].value = proj
    ws['D%s' %mrow].value = proj_status
    ws['E%s' %mrow].value = task
    ws['F%s' %mrow].value = task_status
    ws['G%s' %mrow].value = times
    ws['H%s' %mrow].value = notes

    wb.save(filename)
    wb.close()

    # loop action
    if p_event != 'Switch Project':
        ploop = 1
    else:
        ploop = None

    if (p_event != 'Switch Task') or (p_event == 'Dunzo'):
        exe_loop = 1

# logout
exit()