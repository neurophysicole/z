def cleanup(backup, main_dir, backup_dir, cur_branch_name, duplicate_id):

    # import command line package
    import os

    # import timing package
    import time

    # clean out any duplicate Box files
    print('\nCleaning up the file drawers.')
    time.sleep(.1)

    # list the dirs
    if backup:
        check_dirs = [main_dir, backup_dir]
    else:
        check_dirs = [main_dir]

    # iterate through dirs
    for dir in check_dirs:
        
        # check the dir name
        if dir == main_dir:
            print('\nChecking the local directory.')
        elif dir == backup_dir:
            print('\nChecking the cloud directory.')
        time.sleep(.1)

        # get list of projects
        proj_dir    = '%s/%s' %(dir, cur_branch_name)
        proj_list   = next(os.walk(proj_dir))[1]

        # check main log file
        logfile = next(os.walk(proj_dir))[2]

        # iterate through logfiles (if there are multiple)
        for filex in range(0, len(logfile)):
            lfile = '%s/%s' %(main_dir, logfile[filex])
            if duplicate_id in lfile:
                print('\nLogfile duplicate found!')
                os.system('rm -v -f %s' %lfile)

        # iterate through projects
        for project in proj_list:
            print('..checking the %s project...' %project)

            # get task list
            task_dir    = '%s/%s' %(proj_dir, project)
            task_list   = next(os.walk(task_dir))[1]

            # iterate through tasks
            for task in task_list:

                # get the note list
                note_dir    = '%s/%s' %(task_dir, task)
                note_list   = next(os.walk(note_dir))[2]

                # iterate through notes
                for note in range(0, len(note_list)):
                    tasknote = '%s/%s' %(note_dir, note_list[note]) #get note
                    if duplicate_id in tasknote:
                        print('\nFound one!')
                        os.system('rm -v -f %s' %tasknote)

    # all done
    print('\n--All Clear!\n')
    time.sleep(.1)