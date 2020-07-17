def logit(proj_path, proj_name, task_path, task_name, todo, task_start, task_end, task_details, task_notes, time_s, z_event, main_dir, logfile, project_status):
    # import date/time packages
    import datetime
    from datetime import datetime, date
    
    # import os packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Python interpreter doesn't like it, but it works
    
    # get the date (year first)
    date        = datetime.today().strftime('%Y-%m-%d')
    task_start  = task_start.strftime('%-H%M')
    task_end    = task_end.strftime('%-H%M')
    
    # log task notes
    task_header      = '%s: %s, %s-%s' %(todo, date, task_start, task_end)

    # if close task, need to save the current notes to the archive folder
    if z_event == 'Project Complete':
        task_note_dir   = '%s/archive/%s/archive/%s' %(main_dir, proj_name, task_name)
        task_log_dir    = '%s/archive/%s' %(main_dir, proj_name)
        print('Moving %s project to the archive.' %proj_name)
        os.system('mv -v -f %s/%s %s/archive' %(main_dir, proj_name, main_dir))
    elif z_event == 'Task Complete':
        task_note_dir   = '%s/archive/%s' %(task_path, task_name)
        task_log_dir    = '%s' %(task_path)
        print('Moving %s task to the %s archive folder.' %(task_name, proj_name))
        os.system('mv -v -f %s/%s %s/archive' %(task_path, task_name, task_path))
    else: # no archiving
        task_note_dir   = '%s/%s' %(task_path, task_name)
        task_log_dir    = '%s' %task_path

    # setup log
    log = '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(date, task_start, task_end, proj_name, task_name, todo, time_s)

    # log details in file
    task_dets_file = '%s/dets.txt' %(task_log_dir)
    task_dets_file = open(task_dets_file, 'a+')
    task_dets_file.write(task_header)
    task_dets_file.write(log)
    task_dets_file.write(task_details)

    # log notes in file
    task_note_file = '%s/%s_notes.txt' %(task_note_dir, todo)
    task_note_file = open(task_note_file, 'a+')
    task_note_file.write(task_header)
    task_note_file.write(log)
    task_note_file.write(task_notes)
    task_note_file.close()

    # update task log
    task_log_fname  = '%s/%s' %(task_note_dir, logfile)
    task_log_file   = open(task_log_fname, 'a+')
    task_log_file.write(log)
    task_log_file.close()

    # update project log
    proj_log_fname  = '%s/%s' %(task_log_dir, logfile)
    proj_log_file   = open(proj_log_fname, 'a+')
    proj_log_file.write(log)
    proj_log_file.close()
    
    # update master log
    master_log_fname    = '%s/%s' %(proj_path, logfile)
    master_log_file     = open(master_log_fname, 'a+')
    master_log_file.write(log)
    proj_log_file.close()

    # update project status
    project_status_list = [ 'Design', 'Dev', 'Data', 'Analysis', 'Writing' ]
    for i in project_status:
        if project_status[i] == True:
            project_status = project_status_list[i]
        else:
            print('\nThere is an error determining project status.\n')
    
    project_status_fname    = '%s/%s' %(proj_path, status_file)
    project_status_file     = open(project_status_fname, 'w')
    project_status_file.write(project_status)
    project_status_file.close()