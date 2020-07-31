# excuse the grossness.. wrote this while pretty exhausted.
# loop exit orders could use a check over (not sure if order matters when attempting to exit multiple loops).

# import packages
import os
import time

# import settings
import settings

# import data presentation packages
from tabulate import tabulate
import pandas as pd

print('This is going to be kinda gross. Need to clean up later. But it works!')

# status filename
status_file = 'status.txt'
due = str('') #I know this is a dumb place but it will work..

# dirs
main_dir = os.path.dirname(os.path.abspath('%s/..' %__file__)) #main directory

# open the settings file
settings_file = '%s/settings.txt' %(main_dir)
settings_file = open(settings_file, 'r')
settings_list = settings_file.read().splitlines()

for line in range(1, len(settings_list)):
    # current branch
    # get the branch name
    if settings_list[line] == 'CURRENT BRANCH NAME':
        cur_branch_name    = settings_list[(line + 1)]

# close settings file
settings_file.close()

# get projects
proj_path   = '%s/%s' %(main_dir, cur_branch_name)

try:
    proj_list   = next(os.walk(proj_path))[1]
except StopIteration:
    proj_list   = []
else:
    proj_list   = next(os.walk(proj_path))[1]

proj_list.sort()

loopit = True
while loopit:
    # status
    status_header = '\nProject Status'
    print('\n%s\n~*~*~*~*~*~*~*~*~*~*~\n~*~*~*~*~*~*~*~*~*~*~\n\n' %status_header.upper())
    status_list = []
    for project in proj_list:
        project_status_fname = '%s/%s/%s' %(proj_path, project, status_file)

        proj_status_file = open(project_status_fname, 'r')
        proj_status = proj_status_file.read()

        # append lists
        status_list.append(proj_status)

        proj_status_file.close()
        
    status_df = pd.DataFrame({'Project': proj_list, 'Status': status_list})
    print(tabulate(status_df, headers = 'keys', tablefmt = 'psql', showindex = False))
    print('\n\n~*~*~*~*~*~*~*~*~*~*~')

    # print todos
    print('\n\nTODOS\n~*~*~*~*~*~*~*~*~*~*~\n~*~*~*~*~*~*~*~*~*~*~\n\n')
    todo_fname  = '%s/todos.txt' %proj_path
    todo_file   = open(todo_fname, 'r')
    todos       = todo_file.readlines()

    # make dataframe
    idx_list    = []
    projdf_list = []
    todo_list   = []
    ddate_list  = []
    note_list   = []

    todos.sort()
    for line in todos:
        idx = todos.index(line) + 1
        idx_list.append(idx)
        
        line = line.split('\t')
        projdf_list.append(line[0])

        # sometimes they are super long.. making multiple lines..
        todo_words = line[1].split()
        if len(todo_words) > 10:
            todo_words.insert(9, '\n')
        if len(todo_words) > 20:
            todo_words.insert(19, '\n')
        if len(todo_words) > 30:
            todo_words.insert(29, '\n')
        if len(todo_words) > 40:
            todo_words.insert(39, '\n')
        if len(todo_words) > 50:
            todo_words.insert(49, '\n')
        todo_words = ' '.join(todo_words)
        todo_list.append(todo_words)

        ddate_list.append(line[2])

        # making multiple lines again
        note_words = line[3].split()
        if len(note_words) > 10:
            note_words.insert(9, '\n')
        if len(note_words) > 20:
            note_words.insert(19, '\n')
        if len(note_words) > 30:
            note_words.insert(29, '\n')
        if len(note_words) > 40:
            note_words.insert(39, '\n')
        if len(note_words) > 50:
            note_words.insert(49, '\n')

        # add a note header
        note_header = str('<-----%i----->\n' %(idx))
        note_words.insert(0, note_header)
        note_words = ' '.join(note_words)
        note_list.append(note_words)

    todos_df = pd.DataFrame({'#': idx_list, 'Project': projdf_list, 'To-Dos': todo_list, 'Due Date': ddate_list, 'Notes': note_list})
    print(tabulate(todos_df, headers = 'keys', tablefmt = 'psql', showindex = False))
    
    print('\n\n~*~*~*~*~*~*~*~*~*~*~\n\n')

    todo_file.close()

    # update or check off
    uc_loop = True
    while uc_loop:
        update_check = input('Update the list (\'z\'), or check something off (\'x\')?  ')
        if update_check == 'z':
            proj_loop = True
            while proj_loop:
                proj_yn = input('Is this associated with a project? (y/n):  ')
                if (proj_yn == 'y') or (proj_yn == ''):
                    proj_yn_loop = True
                    while proj_yn_loop:
                        for proj in proj_list:
                            print('[%i] %s' %((proj_list.index(proj) + 1), proj))
                        which_proj = int(input('Input the number associated with the project:  ')) - 1
                        if which_proj > (len(proj_list)):
                            print('We\'re not on the same page.')
                            continue
                        confirm = True
                        while confirm:
                            make_proj = str('%s' %proj_list[which_proj])
                            this_proj = input('%s (y/n)?  ' %make_proj)
                            if (this_proj == 'y') or (this_proj == ''):

                                # set due date
                                due_date_loop = True
                                while due_date_loop:
                                    due_date = input('Is there a date by when this todo should be completed? (y/n):  ')
                                    if (due_date == '') or (due_date == 'y'):
                                        due_date_subloop = True
                                        while due_date_subloop:
                                            due         = input('Input the date (e.g., August 24, 2020, 1:00:00 PM):  ')
                                            due_confirm = input(str('%s? (y/n):  ' %due))
                                            if (due_confirm == '') or (due_confirm == 'y'):
                                                # abort loops
                                                due_date_subloop    = False
                                        allday_subloop = True
                                        while allday_subloop:
                                            allday      = input('All day event? (y/n):  ')
                                            if allday == '':
                                                allday_confirm = input(str('y (y/n)?  '))
                                            else:
                                                allday_confirm = input(str('%s? (y/n):  ' %allday))
                                            if ((allday == 'y') or (allday == '')) and ((allday_confirm == 'y') or (allday_confirm == '')):
                                                allday = str('true')
                                                allday_subloop = False
                                            elif (allday == 'n') and ((allday_confirm == 'y') or (allday_confirm == '')):
                                                allday = str('false')
                                                allday_subloop = False
                                            else: #wtf
                                                print('There is an issue with determining the allday nature of the event.')
                                        eventname_loop = True
                                        while eventname_loop:
                                            event_name   = input('Name the event:  ')
                                            eventname_confirm = input(str('%s? (y/n):  ' %event_name))
                                            if (eventname_confirm == 'y') or (eventname_confirm == ''):
                                                eventname_loop = False
                                            elif eventname_confirm == 'n':
                                                eventname_loop = True
                                            else: #wtf
                                                print('There is something wrong with determining the event name.') 
                                        # add to-do to calendar
                                        os.system(str('osascript -e \'tell application \"iCal\" to tell calendar \"To-Dos\" to make event with properties {start date: date \"%s\", allday event: %s, summary: \"%s\"}\'' %(due, allday, event_name)))
                                        due_date_loop       = False
                                        proj_yn_loop    = False
                                        confirm         = False
                                        proj_loop       = False
                                    elif due_date == 'n':
                                        due             = ''
                                        due_date_loop   = False
                                        proj_yn_loop    = False
                                        confirm         = False
                                        proj_loop       = False
                                        allday          = ''
                                        event_name      = ''
                                    else: #wtf
                                        print('\nThat don\'t make no sense. Try again.\n')


                                confirm = False
                                proj_yn_loop = False
                                proj_loop == False
                            elif this_proj == 'n':
                                confirm = False
                            else: #wtf
                                print('There is something wrong with trying to determine what project you want to add.')
                elif proj_yn == 'n':
                    make_proj = str('NA')


                    # set due date
                    due_date_loop = True
                    while due_date_loop:
                        due_date = input('Is there a date by when this todo should be completed? (y/n):  ')
                        if (due_date == '') or (due_date == 'y'):
                            due_date_subloop = True
                            while due_date_subloop:
                                due         = input('Input the date (e.g., August 24, 2020, 1:00:00 PM):  ')
                                due_confirm = input(str('%s? (y/n):  ' %due))
                                if (due_confirm == '') or (due_confirm == 'y'):
                                    # abort loops
                                    due_date_subloop    = False
                            allday_subloop = True
                            while allday_subloop:
                                allday      = input('All day event? (y/n):  ')
                                if allday == '':
                                    allday_confirm = input(str('y (y/n)?  '))
                                else:
                                    allday_confirm = input(str('%s (y/n)?  ' %allday))
                                if ((allday == 'y') or (allday == '')) and ((allday_confirm == 'y') or (allday_confirm == '')):
                                    allday = str('true')
                                    allday_subloop = False
                                elif (allday == 'n') and ((allday_confirm == 'y') or (allday_confirm == '')):
                                    allday = str('false')
                                    allday_subloop = False
                                else: #wtf
                                    print('There is an issue with determining the allday nature of the event.')
                            eventname_loop = True
                            while eventname_loop:
                                event_name   = input('Name the event:  ')
                                eventname_confirm = input(str('%s? (y/n):  '%event_name))
                                if (eventname_confirm == 'y') or (eventname_confirm == ''):
                                    eventname_loop = False
                                elif eventname_confirm == 'n':
                                    eventname_loop = True
                                else: #wtf
                                    print('There is something wrong with determining the event name.') 
                            # add to-do to calendar
                            os.system(str('osascript -e \'tell application \"iCal\" to tell calendar \"To-Dos\" to make event with properties {start date: date \"%s\", allday event: %s, summary: \"%s\"}\'' %(due, allday, event_name)))
                            due_date_loop       = False
                        elif due_date == 'n':
                            due             = ''
                            due_date_loop   = False
                            allday          = ''
                            event_name      = ''
                        else: #wtf
                            print('\nThat don\'t make no sense. Try again.\n')


                    proj_loop = False
                else: #wtf
                    print('Something is wrong! Try again.')

            in_todo_loop = True
            while in_todo_loop:
                in_todo = input('What is the todo?  ')
                in_todo_yn_loop = True
                while in_todo_yn_loop:
                    in_todo_yn = input('%s (y/n)?  ' %in_todo)
                    if (in_todo_yn == 'y') or (in_todo_yn == ''):
                        in_todo_yn_loop = False
                        in_todo_loop = False
                    elif in_todo_yn == 'n':
                        in_todo_yn_loop = False
                    else: #wtf
                        print('There was an issue with confirming the todo.')
            
            todo_notes  = input('Any notes?\n')
            if todos != []:
                log_todo    = str('%s\t%s\t%s\t%s\n' %(make_proj, in_todo, due, todo_notes))
            else:
                log_todo    = str('%s\t%s\t%s\t%s\n' %(make_proj, in_todo, due, todo_notes))

            update_confirm = True
            while update_confirm:
                u_conf = input('Log it (y/n)?  ')
                if (u_conf == 'y') or (u_conf == ''):
                    # logit
                    todo_file = open(todo_fname, 'a+')
                    todo_file.write(log_todo)
                    todo_file.close()
                    # close loop
                    update_confirm = False
                    uc_loop = False
                elif u_conf == 'n':
                    update_confirm == False
                else: #wtf
                    print('There was an issue confirming whether or not you wanted to log it.')
            
        elif update_check == 'x':
            check_loop = True
            while check_loop:
                check = int(input('Which todo would you like to check off (#)?  ')) - 1
                if check > (len(todos)):
                    print('There was something wrong with that input. Try again.')
                    continue
                check_confirm_loop = True
                while check_confirm_loop:
                    check_confirm = input('%s (y/n)?  ' %todos[check]) #not sure if that will work after the doc is closed...
                    if (check_confirm == 'y') or (check_confirm == ''):
                        # delete line
                        new_todos = []
                        todo_file = open(todo_fname, 'w')
                        todo_file.write('')
                        todo_file.close()
                        todo_file = open(todo_fname, 'a+')
                        for line in range(0, len(todos)):
                            if todos[check] != todos[line]:
                                if line > 0:
                                    if todos[(check - 1)] != todos[(line - 1)]:
                                        todo_file.write('%s' %todos[line])
                                else:
                                    todo_file.write('%s' %todos[line])                   
                        todo_file.close()

                        check_confirm_loop = False
                        check_loop = False
                        uc_loop = False
                    elif check_confirm == 'n':
                        check_confirm_loop = False
                    else: #wtf
                        print('There was something wrong with checking your confirmation.')
                            
        else: #wtf
            print('Not sure what you want..')

        # anything else?
        more_loop = True
        while more_loop:
            more = input('Would you like to do anything else (y/n)?'  )
            if (more == 'y') or (more == ''):
                y_confirm_loop = True
                while y_confirm_loop:
                    y_confirm = input('Sure it\'s a yes (y/n)?  ')
                    if (y_confirm == 'y') or (y_confirm == ''):
                        y_confirm_loop = False
                        more_loop = False
                    elif y_confirm == 'n':
                        y_confirm_loop = False
                    else: #wtf
                        print('Something wrong with confirming your response.')
            elif more == 'n':
                n_confirm_loop = True
                while n_confirm_loop:
                    n_confirm = input('Sure it\'s a no (y/n)?  ')
                    if (n_confirm == 'y') or (n_confirm == ''):
                        n_confirm_loop = False
                        more_loop = False
                        loopit = False
                    elif n_confirm == 'n':
                        n_confirm_loop = False
                    else: #wtf
                        print('There was a problem with confirming your response.')
            else: #wtf
                print('Something went wrong while attempting to confirm your response. Try again.')