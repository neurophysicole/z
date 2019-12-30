def logit(proj_path, proj_name, task_path, task_name, time, task_end, notes, time_s, proj_time, z_event, main_dir):
    # import date/time packages
    import datetime
    from datetime import datetime, date, timedelta
    
    # import command line packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Python interpreter doesn't like it, but it works

    # get the date (year first)
    date = datetime.today().strftime('%Y-%m-%d')

    # log task notes
    task_fname      = '%s_%s' %(date, time_s)

    # if close task, need to save the current notes to the archive folder
    if z_event == 'Project Complete':
        task_note_dir   = '%s/archive/%s/%s' %(main_dir, proj_name, task_name)
        task_log_dir    = '%s/archive/%s' %(main_dir, proj_name)
    elif z_event == 'Task Complete':
        task_note_dir   = '%s/archive/%s' %(task_path, task_name)
        task_log_dir    = '%s' %(task_path)
    else: # no archiving
        task_note_dir   = '%s/%s' %(task_path, task_name)
        task_log_dir    = '%s' %task_path

    task_note_file = '%s/%s.txt' %(task_note_dir, task_fname)
    task_note_file = open(task_note_file, 'w')
    task_note_file.write(notes)
    task_note_file.close()

    log = '%s\t%s\t%s\t%s\n' %(task_fname, proj_name, task_name, time_s)

    # update project log
    proj_log_fname  = '%s/log.txt' %(task_log_dir)
    proj_log_file   = open(proj_log_fname, 'a+')
    proj_log_file.write(log)
    proj_log_file.close()
    
    #update master log
    master_log_fname    = '%s/log.txt' %proj_path
    master_log_file     = open(master_log_fname, 'a+')
    master_log_file.write(log)
    proj_log_file.close()