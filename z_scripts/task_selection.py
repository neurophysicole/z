def task_selection(archive_task_list, task_path, task_list, proj_path, proj_name):
    # import command line packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Pythong interpreter doesn't like it, but it works

    # total time on the project
    # -------------------------
    proj_time_file  = open('%s/time_on_task.txt' %task_path, 'r')
    proj_time       = int(proj_time_file.read())
    proj_time_h     = proj_time / 3600
    proj_time_m     = (proj_time - (proj_time_h * 3600)) / 60

    print('====================\n%s: %i Hours & %i Minutes\n====================\n' %(proj_name.upper(), proj_time_h, proj_time_m))


    # ================
    # Select the Task
    # ================
    task_check_loop = True
    while task_check_loop:
        # list tasks in the archive folder
        print('\nCompleted Tasks:')
        for task in archive_task_list:

            # total time spent
            task_time_file  = open('%s/archive/%s/time_on_task.txt' %(task_path, task), 'r')
            task_time       = int(task_time_file.read())
            task_time_file.close()

            # calculations - it is listed in seconds
            task_time_h     = task_time / 3600
            task_time_m     = (task_time - (task_time_h * 3600)) / 60

            # list it
            print('-x- %s\t\tH %i\tM %i' %(task, task_time_h, task_time_m))

        # list the active tasks
        print('\nTasks:')
        for task in task_list:

            # total time spent
            task_time_file  = open('%s/%s/time_on_task.txt' %(task_path, task), 'r')
            task_time       = int(task_time_file.read())
            task_time_file.close()

            # calculations - it is listed in seconds
            task_time_h     = task_time / 3600
            task_time_m     = (task_time - (task_time_h * 3600)) / 60

            # list it
            print('(%s) %s\t\tH %i\tM %i' %((task_list.index(task) + 1), task, task_time_h, task_time_m))

        task_input_loop = True
        while task_input_loop:
            try:
                task = int(raw_input('\nTask?\nTo return to project selection, enter \'0\', otherwise, enter a number:  '))
            except ValueError:
                continue
            else:
                task_input_loop = False

        if task == 0:
            task_name = 'new_jobber'
            task_check_loop = False
            task_input_loop = False
            break

        elif task <= len(task_list):
            task_name = task_list[(task - 1)]
        
            # confirm the task
            task_confirm_loop = True
            while task_confirm_loop:
                task_confirm = raw_input('\n%s? (y/n):  ' %task_name)

                if (task_confirm == '') or (task_confirm == 'y'):
                    task_check_loop     = False
                    task_confirm_loop   = False

                elif task_confirm == 'n': #input incorrect task
                    task_check_loop = False

                else: #wtf
                    print('\nThat don\'t make no sense. Try again.\n')

        else: #create new task
            new_task = True
            while new_task:
                task_name = raw_input('\nNew Task (Name):  ')

                confirm_task = True
                while confirm_task:
                    # confirm the task name
                    task_loop_confirm = raw_input('\n%s? (y/n)' %task_name)
                    
                    if (task_loop_confirm == '') or (task_loop_confirm == 'y'):
                        # check to see if actually a task that was previously archived
                        if os.path.isdir('%s/archive/%s' %(task_path, task_name)): #exists in archive folder
                            os.system('mv -v -f %s/archive/%s %s' %(task_path, task_name, task_path))

                            # abort loops
                            new_task        = False
                            confirm_task    = False
                            task_check_loop = False

                        else: #is a brand new task
                            os.system('mkdir %s/%s' %(task_path, task_name)) #create new task directory
                            # create a new timing file for the task
                            task_timing_file = open('%s/%s/time_on_task.txt' %(task_path, task_name), 'w')
                            task_timing_file.write('0')
                            task_timing_file.close()

                            # abort loops
                            new_task        = False
                            confirm_task    = False
                            task_check_loop = False

                    elif task_loop_confirm == 'n': #input wrong task name
                        confirm_task    = False

                    else: #wtf
                        print('\nThat don\'t make no sense. Try again.\n')
    
    return task_name