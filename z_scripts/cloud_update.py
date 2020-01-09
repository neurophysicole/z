def cloud_update(main_dir, backup_dir, cur_branch_name, logfile):
    # import packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Python interpreter doesn't like it, but it works

    # import time package
    import time

    # check for projects, then check for tasks within each project
    print('Checking the local and cloud files for asymmetries..')
    time.sleep(.1)


    # ==============
    # Project Check
    # ==============
    # establish project paths
    local_proj_path = '%s/%s' %(main_dir, cur_branch_name)
    cloud_proj_path = '%s/%s' %(backup_dir, cur_branch_name)
    
    # make sure the current branch is in the cloud file system
    if os.path.isdir(cloud_proj_path):
        print('Checking %s' %cur_branch_name)
        time.sleep(.1)
    else: #there is no branch dir in the cloud file system
        print('\nGrowing the new %s branch in the cloud.\n' %cur_branch_name)
        time.sleep(.1)

        # copy the branch up to the cloud
        os.system('cp -a -v %s %s' %(local_proj_path, backup_dir))

    # make sure the current branch is in the local file system
    if os.path.isdir(local_proj_path):
        print('Ya, what he said..')
        time.sleep(.1)
    else: #there is not branch dir in the local file system
        print('\nGrowing the new %s local branch.\n' %cur_branch_name)
        time.sleep(.1)

        # copy the branch down to the local file system
        os.system('cp -a -v %s %s' %(cloud_proj_path, main_dir))

    # create project lists
    local_proj_list = next(os.walk(local_proj_path))[1]
    cloud_proj_list = next(os.walk(cloud_proj_path))[1]

    # project archive check
    # ---------------------
    # if project is archived on Cloud, need to archive locally, so there aren't duplicates
    # if the project is archived locally, should be updated on the Cloud
    # create archive list
    local_archive_proj_path = '%s/archive' %main_dir
    cloud_archive_proj_path = '%s/archive' %backup_dir

    local_archive_proj_list = next(os.walk(local_archive_proj_path))[1]
    cloud_archive_proj_list = next(os.walk(cloud_archive_proj_path))[1]

    # check local first
    for proj in local_archive_proj_list:
        if proj not in cloud_archive_proj_list:
            print('\nEvaporating archived project ** %s ** to the cloud archive list.\n' %proj)
            time.sleep(.1)

            os.system('cp -a -v %s/%s %s' %(local_archive_proj_path, proj, cloud_archive_proj_path)) #copy the proj

            # update the project directory
            if os.path.isdir('%s/%s' %(cloud_proj_path, proj)):
                os.system('rm -r -v -f %s/%s' %(cloud_proj_path, proj))

            # update the project list
            if proj in cloud_proj_list:
                cloud_proj_list.remove(proj)

    # now check cloud
    for proj in cloud_archive_proj_list:
        if proj not in local_archive_proj_list:
            print('\nPrecipitating archived project ** %s ** from the cloud archive list.\n' %proj)
            time.sleep(.1)

            os.system('cp -a -v %s/%s %s' %(cloud_archive_proj_path, proj, local_archive_proj_path)) #copy the proj

            # update the project directory
            if os.path.isdir('%s/%s' %(local_proj_path, proj)):
                os.system('rm -r -v -f %s/%s' %(local_proj_path, proj))

            # update the project list
            if proj in local_proj_list:
                local_proj_list.remove(proj)


    # project log sheet check
    # -----------------------
    # master
    # check that the local and cloud log sheets are all up to date
    local_master_log        = '%s/%s' %(local_proj_path, logfile)
    cloud_master_log        = '%s/%s' %(cloud_proj_path, logfile)

    # set files
    local_master_log_file   = open(local_master_log, 'r')
    cloud_master_log_file   = open(cloud_master_log, 'r')

    local_master_log_list   = local_master_log_file.read().splitlines()
    cloud_master_log_list   = cloud_master_log_file.read().splitlines()

    # master
    # not doing project level because will need to iterate through and check all projects in case updates were made on a different computer
    cloud_appended = False #for updating
    local_appended = False #for updating

    # check and update cloud master log list
    for line in local_master_log_list:
        if line not in cloud_master_log_list:
            cloud_master_log_list.append(line)
            cloud_appended = True
    
    # check and update local master log list
    for line in cloud_master_log_list:
        if line not in local_master_log_list:
            local_master_log_list.append(line)
            local_appended = True 
    
    # update local log file
    if local_appended:
        local_master_log_file.close()
        with open(local_master_log, 'w') as local_master_log_file:
            for line in local_master_log_list:
                local_master_log_file.write('%s\n' %line)

    # update cloud log file
    if cloud_appended:
        cloud_master_log_file.close()
        with open(cloud_master_log, 'w') as cloud_master_log_file:
            for line in cloud_master_log_list:
                cloud_master_log_file.write('%s\n' %line)

    # close out files
    local_master_log_file.close()
    cloud_master_log_file.close()

    
    # ===============
    # Run the update
    # ===============
    # project update with task update nested within
    # copy projects to cloud
    # ----------------------
    for proj in local_proj_list:
        if proj not in cloud_proj_list:
            print('\nEvaporating ** %s ** project file to the cloud.\n' %proj)
            time.sleep(.1)

            os.system('cp -a -v %s/%s %s' %(local_proj_path, proj, cloud_proj_path))
        else: #project is already there
            print('\nProject ** %s ** is up to date in the cloud.\n' %proj)
            time.sleep(.1)


            # log update
            # ----------
            # project log
            local_proj_log  = '%s/%s/%s' %(local_proj_path, proj, logfile)
            cloud_proj_log  = '%s/%s/%s' %(cloud_proj_path, proj, logfile)

            local_proj_log_file     = open(local_proj_log, 'r')
            cloud_proj_log_file     = open(cloud_proj_log, 'r')

            local_proj_log_list     = local_proj_log_file.read().splitlines()
            cloud_proj_log_list     = cloud_proj_log_file.read().splitlines()

            # compare log files, update if necessary
            # update cloud list
            local_appended = False # for updating
            cloud_appended = False # for updating

            for line in local_proj_log_list:
                if line not in cloud_proj_log_list:
                    cloud_proj_log_list.append(line)
                    cloud_appended = True
            
            # update local list
            for line in cloud_proj_log_list:
                if line not in local_proj_log_list:
                    local_proj_log_list.append(line)
                    local_appended = True
            
            # if local list was changed
            if local_appended:
                local_proj_log_file.close()
                with open(local_proj_log, 'w') as local_proj_log_file:
                    for line in local_proj_log_list:
                        local_proj_log_file.write('%s\n' %line)
            
            # if cloud list was changed
            if cloud_appended:
                cloud_proj_log_file.close()
                with open(cloud_proj_log, 'w') as cloud_proj_log_file:
                    for line in cloud_proj_log_list:
                        cloud_proj_log_file.write('%s\n' %line)


            # task update
            # -----------
            # task lists
            local_task_path = '%s/%s' %(local_proj_path, proj)
            cloud_task_path = '%s/%s' %(cloud_proj_path, proj)

            local_task_list = next(os.walk(local_task_path))[1]
            cloud_task_list = next(os.walk(cloud_task_path))[1]

            # remove archive from task list
            local_task_list.remove('archive')
            cloud_task_list.remove('archive')


            # task archive check
            # ------------------
            # if task is archived on Cloud, need to archive locally, so there aren't duplicates
            # if the task is archived locally, should be updated on the Cloud
            # create archive list
            local_archive_task_path = '%s/archive' %local_task_path
            cloud_archive_task_path = '%s/archive' %cloud_task_path

            local_archive_task_list = next(os.walk(local_archive_task_path))[1]
            cloud_archive_task_list = next(os.walk(cloud_archive_task_path))[1]

            # check local first
            for task in local_archive_task_list:
                if task not in cloud_archive_task_list:
                    print('\nEvaporating task ** %s ** archived in the %s project to the cloud.\n' %(task, proj))
                    time.sleep(.1)

                    os.system('cp -a -v %s/%s %s' %(local_archive_task_path, task, cloud_archive_task_path)) #copy the task

                    # update the project directory
                    if os.path.isdir('%s/%s' %(cloud_task_path, task)):
                        os.system('rm -r -v -f %s/%s' %(cloud_task_path, task))

                    # update the project list
                    if task in cloud_task_list:
                        cloud_task_list.remove(task)

            # now check cloud
            for task in cloud_archive_task_list:
                if task not in local_archive_task_list:
                    print('\nPrecipitating task ** %s ** from the cloud archive list for the %s project.\n' %(task, proj))
                    time.sleep(.1)

                    os.system('cp -a -v %s/%s %s' %(cloud_archive_task_path, task, local_archive_task_path)) #copy the task

                    # update the task directory
                    if os.path.isdir('%s/%s' %(local_task_path, task)):
                        os.system('rm -r -v -f %s/%s' %(local_task_path, task))

                    # update the task list
                    if task in local_task_list:
                        local_task_list.remove(task)

            # task update
            # -----------
            # compare task lists and copy over necessary items
            for task in local_task_list:
                if task not in cloud_task_list:
                    print('Project: %s.\nEvaporating ** %s ** task file to the cloud.\n' %(proj, task))
                    time.sleep(.1)

                    # throw it up
                    os.system('rm -r -v -f %s/%s' %(cloud_task_path, task))
                    os.system('cp -a -v %s/%s %s' %(local_task_path, task, cloud_task_path))


                    # update time on task -- project
                    # ------------------------------
                    # if adding new task, need to update project time on task
                    # open the files
                    cloud_time_on_task = open('%s/time_on_task.txt' %(cloud_task_path), 'r')
                    local_task_time = open('%s/%s/time_on_task.txt' %(local_task_path, task), 'r')

                    # get the values
                    cloud_time_on_task_value    = int(cloud_time_on_task.read())
                    local_task_time_value       = int(local_task_time.read())

                    cloud_time_on_task_value = cloud_time_on_task_value + local_task_time_value
                    cloud_time_on_task.close()
                    cloud_time_on_task = open('%s/time_on_task.txt' %(cloud_task_path), 'w') #just tired of battling it...
                    cloud_time_on_task.write(str(cloud_time_on_task_value))

                    # close out files
                    cloud_time_on_task.close()
                    local_task_time.close()

                else: #the task is already there

                    # note update
                    # -----------
                    # note list
                    local_note_path = '%s/%s' %(local_task_path, task)
                    cloud_note_path = '%s/%s' %(cloud_task_path, task)

                    local_note_list = os.listdir(local_note_path)
                    cloud_note_list = os.listdir(cloud_note_path)

                    # compare and update notes as necessary
                    for note in local_note_list:
                        if note not in cloud_note_list:
                            print('Project: %s. Task: %s.\nEvaporating ** %s ** note file to the cloud.\n' %(proj, task, note))
                            time.sleep(.1)

                            # throw it up
                            os.system('cp -v %s/%s %s' %(local_note_path, note, cloud_note_path))


                            # update time on task -- task
                            # ---------------------------
                            # if add a new note, need to update time on task for task and project
                            # get original time on task
                            old_cloud_time_on_task = open('%s/time_on_task.txt' %(cloud_note_path), 'r')
                            old_cloud_time_on_task_value = int(old_cloud_time_on_task.read())
                            old_cloud_time_on_task.close()

                            # delete old task time, copy over new task time 
                            os.system('rm -v -f %s/time_on_task.txt' %(cloud_note_path))
                            os.system('cp %s/time_on_task.txt %s' %(local_note_path, cloud_note_path))

                            # get new time on task
                            cloud_time_on_task              = open('%s/time_on_task.txt' %(cloud_note_path), 'r')
                            cloud_time_on_task_proj         = open('%s/time_on_task.txt' %(cloud_task_path), 'r')

                            cloud_time_on_task_value        = int(cloud_time_on_task.read())
                            cloud_time_on_task_proj_value   = int(cloud_time_on_task_proj.read())

                            # get the amount of time to add to project
                            proj_task_time_add              = cloud_time_on_task_value - old_cloud_time_on_task_value
                            cloud_time_on_task_proj_value   = cloud_time_on_task_proj_value + proj_task_time_add

                            # update project time
                            cloud_time_on_task_proj.close()
                            cloud_time_on_task_proj         = open('%s/time_on_task.txt' %(cloud_task_path), 'w')
                            cloud_time_on_task_proj.write(str(cloud_time_on_task_proj_value))

                            # close files
                            cloud_time_on_task.close()
                            cloud_time_on_task_proj.close()


    # copy projects from cloud
    # ------------------------
    # NOTE: Log files already updated to-and-from the cloud (above)
    for proj in cloud_proj_list:
        if proj not in local_proj_list:
            print('Precipitating ** %s ** project files from the cloud.' %proj)
            time.sleep(.1)

            os.system('cp -a -v %s/%s %s' %(cloud_proj_path, proj, local_proj_path))
        else: #project is already updated
    

            # task update
            # -----------
            # task lists
            local_task_path = '%s/%s' %(local_proj_path, proj)
            cloud_task_path = '%s/%s' %(cloud_proj_path, proj)

            local_task_list = next(os.walk(local_task_path))[1]
            cloud_task_list = next(os.walk(cloud_task_path))[1]

            # check and update tasks as necessary
            for task in cloud_task_list:
                if task not in local_task_list:
                    print('Project: %s.\nPrecipitating ** %s ** task file from the cloud.\n' %(proj, task))
                    time.sleep(.1)

                    # make the drop
                    os.system('cp -a -v %s/%s %s' %(cloud_task_path, task, local_task_path))


                    # update time on task -- project
                    # ------------------------------
                    # if adding new task, need to update project time on task
                    # open the files
                    local_time_on_task = open('%s/%s/time_on_task.txt' %(local_proj_path, proj), 'r')
                    cloud_task_time = open('%s/%s/%s/time_on_task.txt' %(cloud_proj_path, proj, task), 'r')

                    # get the values
                    local_time_on_task_value    = int(local_time_on_task.read())
                    cloud_task_time_value       = int(cloud_task_time.read())

                    local_time_on_task_value = local_time_on_task_value + cloud_task_time_value
                    local_time_on_task.close()
                    local_time_on_task = open('%s/%s/time_on_task.txt' %(local_proj_path, proj), 'w') #just tired of battling it...
                    local_time_on_task.write(str(local_time_on_task_value))

                    # close out files
                    local_time_on_task.close()
                    cloud_task_time.close()

                else: #the task is already there


                    # note update
                    # -----------
                    # note list
                    local_note_path = '%s/%s' %(local_task_path, task)
                    cloud_note_path = '%s/%s' %(cloud_task_path, task)

                    local_note_list = os.listdir(local_note_path)
                    cloud_note_list = os.listdir(cloud_note_path)

                    # compare and update notes as necessary
                    for note in cloud_note_list:
                        if note not in local_note_list:
                            print('Project: %s. Task: %s.\nPrecipitating ** %s ** note file from the cloud.\n' %(proj, task, note))
                            time.sleep(.1)

                            # make the drop
                            os.system('cp -v %s/%s %s' %(cloud_note_path, note, local_note_path))


                            # update time on task -- task
                            # ---------------------------
                            # if add a new note, need to update time on task for task and project
                            # get original time on task
                            old_local_time_on_task = open('%s/time_on_task.txt' %(local_note_path), 'r')
                            old_local_time_on_task_value = int(old_local_time_on_task.read())
                            old_local_time_on_task.close()

                            # delete old task time, copy over new task time 
                            os.system('rm -v -f %s/time_on_task.txt' %(local_note_path))
                            os.system('cp %s/time_on_task.txt %s' %(cloud_note_path, local_note_path))

                            # get new time on task
                            local_time_on_task              = open('%s/time_on_task.txt' %(local_note_path), 'r')
                            local_time_on_task_proj         = open('%s/time_on_task.txt' %(local_task_path), 'r')

                            local_time_on_task_value        = int(local_time_on_task.read())
                            local_time_on_task_proj_value   = int(local_time_on_task_proj.read())

                            # get the amount of time to add to project
                            proj_task_time_add              = local_time_on_task_value - old_local_time_on_task_value
                            local_time_on_task_proj_value   = local_time_on_task_proj_value + proj_task_time_add

                            # update project time
                            local_time_on_task_proj.close()
                            local_time_on_task_proj         = open('%s/time_on_task.txt' %(local_task_path), 'w')
                            local_time_on_task_proj.write(str(local_time_on_task_proj_value))

                            # close files
                            local_time_on_task.close()
                            local_time_on_task_proj.close()