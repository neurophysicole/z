def task_interface(proj_name, task_name, proj_path, backup_dir, cur_branch_name):
    # import date/time packages
    import datetime
    from dateutil.relativedelta import relativedelta
    from datetime import datetime, date

    # import command line packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Pythong interpreter doesn't like it, but it works

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

    #startup Thymer (operates in the top bar)
    os.system(close_thymer)
    os.system(open_thymer)
    os.system(start_thymer)

    # date/time parameters
    date = datetime.today().strftime('%m-%d-%Y')
    time = datetime.today().strftime('%-H:%M')

    # get timing
    # project
    proj_timing_file    = open('%s/%s/time_on_task.txt' %(proj_path, proj_name), 'r')
    proj_time           = int(proj_timing_file.read())
    proj_time_h         = proj_time / 3600
    proj_time_m         = (proj_time - (proj_time_h * 3600)) / 60

    proj_time_total     = 'Hours %i: Minutes %i' %(proj_time_h, proj_time_m)

    # task
    task_timing_file    = open('%s/%s/%s/time_on_task.txt' %(proj_path, proj_name, task_name), 'r')
    task_time           = int(task_timing_file.read())
    task_time_h         = task_time / 3600
    task_time_m         = (task_time - (task_time_h * 3600)) / 60

    task_time_total     = 'Hours %i: Minutes %i' %(task_time_h, task_time_m)

    # ---------------
    # window sections
    proj_header             = [sg.Text('%s' %proj_name), sg.Text('%s' %proj_time_total)]
    proj_complete_button    = [sg.CloseButton('Project Complete')]
    task_header             = [sg.Text('%s' %task_name), sg.Text('%s' %task_time_total)]
    task_complete_button    = [sg.CloseButton('Task Complete')]
    text_entry              = sg.Multiline(size = (100, 8), key = 'notes', autoscroll = True, default_text = '----------\n')
    dunzo_button            = sg.CloseButton('Dunzo')

    # window
    SetOptions(background_color = 'black', element_background_color = 'black', text_color = 'white', text_element_background_color = 'black', element_text_color = 'white', input_elements_background_color = 'black', input_text_color = 'white')

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
    proj_time = int(proj_time)
    proj_time = str(proj_time + time_s)
    proj_timing_file.close()

    # task timing
    task_time = int(task_time)
    task_time = str(task_time + time_s)
    task_timing_file.close()

    # save timings
    proj_timing_file = open('%s/%s/time_on_task.txt' %(proj_path, proj_name), 'w')
    proj_timing_file.write(proj_time)
    proj_timing_file.close()
    print('\nEvaporating time on task to the cloud.\n')
    os.system('cp -v %s/%s/time_on_task.txt %s/%s/%s' %(proj_path, proj_name, backup_dir, cur_branch_name, proj_name)) #need to backup timing...

    task_timing_file = open('%s/%s/%s/time_on_task.txt' %(proj_path, proj_name, task_name), 'w')
    task_timing_file.write(task_time)
    task_timing_file.close()
    print('\nEvaporating time on task to the cloud.\n')
    os.system('cp -v %s/%s/%s/time_on_task.txt %s/%s/%s/%s' %(proj_path, proj_name, task_name, backup_dir, cur_branch_name, proj_name, task_name)) # need to backup timing...

    # shutdown Thymer
    os.system(stop_thymer)
    os.system(close_thymer)

    return z_event, task_start, task_end, notes, time_s, proj_time