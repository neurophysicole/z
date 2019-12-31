def task_selection(archive_task_list, task_path, task_name, task_list, proj_path, proj_name):
    # import command line packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Pythong interpreter doesn't like it, but it works

    # select the task
    # ---------------
    task_check_loop = True
    while task_check_loop:
        # list tasks in the archive folder
        print('\nCompleted Tasks:')
        for tasks in archive_task_list:
            print('-x- %s' %(tasks))

        # list the active tasks
        print('\nTasks:')
        for tasks in task_list:
            print('(%s) %s' %((task_list.index(tasks) + 1), tasks))

        task_input_loop = True
        while task_input_loop:
            try:
                task = int(raw_input('\nTask? (Number):  '))
            except ValueError:
                continue
            else:
                task_input_loop = False

        if (task) <= len(task_list):
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