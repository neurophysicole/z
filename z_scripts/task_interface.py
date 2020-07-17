def task_interface(proj_name, task_name, proj_path, cur_branch_name, thymer):
    # import date/time packages
    import datetime
    from dateutil.relativedelta import relativedelta
    from datetime import datetime, date

    # import command line packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Python interpreter doesn't like it, but it works

    # import interface packages
    import PySimpleGUI as sg
    from PySimpleGUI import SetOptions

    # task timer - start
    task_start = datetime.now()
    
    # thymer scripts
    open_thymer  = 'open -a Thyme'
    start_thymer = 'osascript -e \'tell app "Thyme" to start\''
    stop_thymer  = 'osascript -e \'tell app "Thyme" to stop\''
    close_thymer = 'osascript -e \'quit app "Thyme"\''

    # startup Thyme (operates in the top bar)
    if thymer: #if Thyme isn't already running
        os.system(close_thymer)
        os.system(open_thymer)
        os.system(start_thymer)

    # date/time parameters
    date = datetime.today().strftime('%m-%d-%Y')
    time = datetime.today().strftime('%-H:%M')

    # get timing
    # ----------
    # open main file
    proj_timing_file    = open('%s/log.txt' %(proj_path), 'r')
    proj_time           = proj_timing_file.read().splitlines()

    # get proj time
    proj_time_s = 0
    for line in proj_time:
        logtime      = line.split() #separate out the lines
        logtime_proj = logtime[3] #get the project name
        if logtime_proj == proj_name:
            proj_time_s = proj_time_s + int(logtime[-1]) #add the seconds

    # apply the project time
    proj_time_h     = proj_time_s / 3600 #calc hours
    proj_time_m     = (proj_time_s - (proj_time_h * 3600)) / 60 #calc mins
    proj_time_total = 'Hours %i: Minutes %i' %(proj_time_h, proj_time_m) #put it together

    # open proj log file
    task_timing_file    = open('%s/%s/log.txt' %(proj_path, proj_name), 'r')
    task_time           = task_timing_file.read().splitlines()

    # get task time
    task_time_s = 0
    for line in task_time:
        logtime      = line.split() #separate out the lines
        logtime_task = logtime[-2] #get the task name
        if logtime_task == task_name:
            task_time_s = task_time_s + int(logtime[-1]) #add the seconds

    # apply the task time
    task_time_h     = task_time_s / 3600 #calc hours
    task_time_m     = (task_time_s - (task_time_h * 3600)) / 60 #calc mins 
    task_time_total = 'Hours %i: Minutes %i' %(task_time_h, task_time_m) #put it together

    # ---------------
    # window sections
    SetOptions(background_color = 'black', element_background_color = 'black', text_color = 'white', text_element_background_color = 'black', element_text_color = 'white')

    # info
    proj_header             = [sg.Text('%s' %proj_name), sg.Text('%s' %proj_time_total)]
    proj_complete_button    = [sg.CloseButton('Project Complete')]
    task_header             = [sg.Text('%s' %task_name), sg.Text('%s' %task_time_total)]
    task_complete_button    = [sg.CloseButton('Task Complete')]

    # status
    design_status   = False
    dev_status      = False
    data_status     = False
    analysis_status = False
    writing_status  = False
    pub_status      = False

    if proj_status == 'Design':
        design_status = True
    elif proj_status == 'Dev':
        dev_status = True
    elif proj_status == 'Data':
        data_status = True
    elif proj_status == 'Analysis':
        analysis_status = True
    elif proj_status == 'Writing':
        writing_status = True
    elif proj_status == 'Pub':
        pub_status = True
    else: #wtf
        print('\nThere is something wrong with determining the project status.\n')

    project_status          = [
        sg.Radio('Design', "status", key = 'design_status_key', default = design_status, size = (10, 1)), sg.Radio('Dev', "status", key = 'dev_status_key', default = dev_status, size = (10,1)), sg.Radio('Data', "status", key = 'data_status_key', default = data_status, size = (10, 1)), sg.Radio('Analysis', "status", key = 'analysis_status_key', default = analysis_status, size = (10, 1)), sg.Radio('Writing', "status", key = 'writing_status_key', default = writing_status, size = (10, 1)), sg.Radio('Pub', "status", key = 'pub_status_key', default = pub_status, size = (10, 1))
        ]

    # list subtasks
    subtasks                = [ sg.Text('To-Do\'s'), sg.InputText('NA', key = 'subtask_txt') sg.Listbox(values = (subtask_list), key = 'subtask_lst', size = (30, 3)) ]

    # text entry boxes
    text_entry_details      = [
        sg.Text('Details'), sg.Multiline(size = (100, 8), key = 'details', autoscroll = True, default_text = '----------\n')
        ]
    text_entry_notes        = [
        sg.Text('Notes'), sg.Multiline(size = (100, 8), key = 'notes', autoscroll = True, default_text = '----------\n')
        ]
    dunzo_button            = sg.CloseButton('Dunzo')

    # ------
    # window
    z_window = sg.Window(str('%s: %s' %(date, time)), resizable = True, disable_close = True, finalize = True)
    z_layout = [[sg.Frame(layout = [proj_header, proj_complete_button], title = 'Project', relief = sg.RELIEF_SUNKEN), project_status],[sg.Frame(layout = [task_header, task_complete_button], title = 'Task', relief = sg.RELIEF_SUNKEN), subtasks],[text_entry_details],[text_entry_notes],[dunzo_button]]


    # ==========
    # Responses
    # ==========
    # setup responses
    z_event, z_values = z_window.Layout(z_layout).Read()

    # notes
    task_details    = z_values['details']
    task_notes      = z_values['notes']

    # to-dos
    if z_values['subtask_txt'] == 'NA':
        todo = z_values['subtask_lst']
    elif z_values['subtask_txt'] != 'NA':
        todo = z_values['subtask_txt']
        open('%s/%s/%s/%s_notes.txt' %(proj_path, proj_name, task_name, todo), 'w+') #create new todo file
    else: #wtf
        print('Error determining the subtask')

    # status
    design_status   = z_values['design_status_key']
    dev_status      = z_values['dev_status_key']
    data_status     = z_values['data_status_key']
    analysis_status = z_values['analysis_status_key']
    writing_status  = z_values['writing_status_key']

    project_status  = [ desgin_status, dev_status, data_status, analysis_status, writing_status ]

    # timing calculations
    # -------------------
    # task timer - end
    task_end    = datetime.now()
    time_x      = relativedelta(task_end, task_start)

    # calculations
    # convert it all to seconds
    time_h = '{h}'.format(h = time_x.hours)
    time_m = '{m}'.format(m = time_x.minutes)
    time_s = '{s}'.format(s = time_x.seconds)

    time_h = int(time_h)*3600
    time_m = int(time_m)*60

    # add them all up
    time_s = int(time_s) + time_h + time_m

    # add them to the project and task timings
    # project timing
    proj_time = str(proj_time_s + time_s)
    proj_timing_file.close()

    # task timing
    task_time = str(task_time_s + time_s)
    task_timing_file.close()

    # shutdown Thymer
    if thymer:
        os.system(stop_thymer)
        os.system(close_thymer)

    return z_event, todo, task_start, task_end, task_details, task_notes, time_s, proj_time, project_status