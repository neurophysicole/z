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
    folder   = '/Users/zcole/Documents/dev/file_drawer/'
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

mrow = str(int(ws.max_row) + 1)

# window
SetOptions(background_color = 'black', element_background_color = 'black',
           text_color = 'white', text_element_background_color = 'black',
           element_text_color = 'white', input_elements_background_color = 'black',
           input_text_color = 'white')

# runit
exe_loop = None
while exe_loop == None:

    # projects
    project_list = []

    for row in ws.iter_rows():
        for cell in row:
            if ws['D' + str(cell.row)].value == 'oo':
                if ws['C' + str(cell.row)].value not in project_list:
                    project_list.append(ws['C' + str(cell.row)].value)

    ploop = None
    while ploop == None:
        # project
        print('\nProjects:')
        for project in project_list:
            print('(%s) %s' %(project_list.index(project), project))

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



        tloop = None
        while tloop == None:
            # tasks
            task_list = []
            for row in ws.iter_rows():
                for cell in row:
                    if ws['C' + str(cell.row)].value == proj:
                        if ws['F' + str(cell.row)].value == 'oo':
                            if ws['E' + str(cell.row)].value not in task_list:
                                task_list.append(ws['E' + str(cell.row)].value)

            print('Tasks:')
            for tasks in task_list:
                print('(%s) %s' %(task_list.index(tasks), tasks))

            # task
            task_loop = 'n'
            while task_loop == 'n':
                try:
                    task = int(raw_input('\nWhat task? (Number): '))
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

            # project notes
            pnote_list = []
            for row in ws.iter_rows():
                for cell in row:
                    if ws['C' + str(cell.row)].value == proj:
                        if ws['H' + str(cell.row)].value not in pnote_list:
                            pnote_list.append(ws['H' + str(cell.row)].value)

            if len(pnote_list) > 0:
                print('\nProject Notes:\n')
                for pnote in pnote_list:
                    print(pnote)
                print('\n-------------------------\n-------------------------\n    END PROJECT NOTES\n-------------------------\n-------------------------')
                    
            # task notes
            note_list = []
            for row in ws.iter_rows():
                for cell in row:
                    if ws['C' + str(cell.row)].value == proj:
                        if ws['E' + str(cell.row)].value == task:
                            if ws['H' + str(cell.row)].value not in note_list:
                                note_list.append(ws['H' + str(cell.row)].value)

            if len(note_list) > 0:
                print('\nTask Notes:\n')
                for note in note_list:
                    print(note)

            # timing calculations
            proj_s = 0
            proj_time = 0
            proj_hours = 0
            proj_mins = 0
            task_s = 0
            task_time = 0
            task_mins = 0
            task_hours = 0
            for row in ws.iter_rows():
                for cell in row:
                    if ws['C' + str(cell.row)].value == proj:
                        if cell.row > 1:
                            ps = ws['G' + str(cell.row)].value
                            if ps != None:
                                proj_s += int(ps)/9
                            else:
                                proj_s += 0

                    # if ws['C' + str(cell.row)].value == proj:
                        if ws['E' + str(cell.row)].value == task:
                            if cell.row > 1:
                                ts = ws['G' + str(cell.row)].value
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
                for row in ws.iter_rows():
                    for cell in row:
                        if ws['C' + str(cell.row)].value == proj:
                            ws['D' + str(cell.row)].value = proj_status
                            ws['F' + str(cell.row)].value = proj_status
            
            if p_values['taskip'] == True:
                task_status = 'oo'
            else:
                task_status = 'xx'
                for row in ws.iter_rows():
                    for cell in row:
                        if ws['E' + str(cell.row)].value == task:
                            ws['F' + str(cell.row)].value = task_status

            notes = p_values['notes']
            
            # log everything
            ws['A' + str(mrow)].value = date
            ws['B' + str(mrow)].value = time
            ws['C' + str(mrow)].value = proj
            ws['D' + str(mrow)].value = proj_status
            ws['E' + str(mrow)].value = task
            ws['F' + str(mrow)].value = task_status
            ws['G' + str(mrow)].value = times
            ws['H' + str(mrow)].value = notes

            wb.save(filename)

            # loop action
            if p_event == 'Switch Task':
                continue
            if p_event == 'Switch Project':
                tloop = 1
            if p_event == 'Dunzo':
                exe_loop = 1
                ploop = 1
                tloop = 1

# logout
wb.save(filename)

exit()