def task_interface(proj_name, task_name, proj_path, backup_dir, cur_branch_name, thymer):
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
    import PySimpleGUI27 as sg
    from PySimpleGUI27 import SetOptions

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
    SetOptions(background_color = 'black', element_background_color = 'black', text_color = 'white', text_element_background_color = 'black', element_text_color = 'white', input_elements_background_color = 'black', input_text_color = 'white')

    proj_header             = [sg.Text('%s' %proj_name), sg.Text('%s' %proj_time_total)]
    proj_complete_button    = [sg.CloseButton('Project Complete')]
    task_header             = [sg.Text('%s' %task_name), sg.Text('%s' %task_time_total)]
    task_complete_button    = [sg.CloseButton('Task Complete')]
    text_entry              = sg.Multiline(size = (100, 8), key = 'notes', autoscroll = True, default_text = '----------\n')
    dunzo_button            = sg.CloseButton('Dunzo')

    # window
    z_window = sg.Window(str('%s: %s' %(date, time)), resizable = True, disable_close = True, finalize = True)
    z_layout = [[sg.Frame(layout = [proj_header, proj_complete_button], title = 'Project', relief = sg.RELIEF_SUNKEN)],[sg.Frame(layout = [task_header, task_complete_button], title = 'Task', relief = sg.RELIEF_SUNKEN)],[text_entry],[dunzo_button]]


    # ==========
    # Responses
    # ==========
    # setup responses
    z_event, z_values = z_window.Layout(z_layout).Read()

    # assing task notes to variable
    notes = z_values['notes']

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
    os.system(stop_thymer)
    os.system(close_thymer)

    return z_event, task_start, task_end, notes, time_s, proj_time