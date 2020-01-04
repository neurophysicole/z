def cloud_update(main_dir, backup_dir, cur_branch_name, logfile):
    # import packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Python interpreter doesn't like it, but it works

    # check for projects, then check for tasks within each project
    print('Checking the local and cloud files for asymmetries..')


    # ==============
    # Project Check
    # ==============
    # see if the project list file is the same locally and on the cloud

    # create lists
    local_proj_path = '%s/%s' %(main_dir, cur_branch_name)
    cloud_proj_path = '%s/%s' %(backup_dir, cur_branch_name)
    
    local_proj_list = next(os.walk(local_proj_path))[1]
    if os.path.isdir(cloud_proj_path):
        print('Checking %s' %cur_branch_name)
    else: #there is no branch dir in the cloud
        print('\nGrowing the new %s branch in the cloud.\n' %cur_branch_name)
        os.system('mkdir %s' %local_proj_path)
        cloud_branch_log = open('%s/%s' %(cloud_proj_path, logfile), 'w')
        cloud_branch_log.close()

    cloud_proj_list = next(os.walk(cloud_proj_path))[1]

    # ================
    # Log Sheet Check
    # ================
    # master
    # check that the local and cloud log sheets are all up to date
    local_master_logfile   = '%s/%s' %(local_proj_path, logfile)
    cloud_master_logfile   = '%s/%s' %(cloud_proj_path, logfile)

    # set files
    local_master_log        = open(local_master_logfile, 'a+')
    cloud_master_log        = open(cloud_master_logfile, 'a+')

    local_master_log_list   = local_master_log.read().splitlines()
    cloud_master_log_list   = cloud_master_log.read().splitlines()

    # master
    # not doing project level because will need to iterate through and check all projects in case updates were made on a different computer

    # local to cloud
    for line in local_master_log_list:
        if line not in cloud_master_log_list:
            cloud_master_log.write(line)
    
    # cloud to local
    for line in cloud_master_log_list:
        if line not in local_master_log_list:
            local_master_log.write(line)


    # ===============
    # Run the update
    # ===============
    # project update with task update nested within
    # copy projects to cloud
    # ----------------------
    for proj in local_proj_list:
        if proj not in cloud_proj_list:
            print('\nEvaporating ** %s ** project file to the cloud.\n' %proj)
            os.system('cp -a -v %s/%s %s' %(local_proj_path, proj, cloud_proj_path))
        else: #project is already there
            print('\nProject ** %s ** is up to date in the cloud.\n' %proj)


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
                        local_proj_log_file.write(line)
            
            # if cloud list was changed
            if cloud_appended:
                cloud_proj_log.close()
                with open(cloud_proj_log, 'w') as cloud_proj_log_file:
                    for line in cloud_proj_log_list:
                        cloud_proj_log_file.write(line)


            # task update
            # -----------
            # task lists
            local_task_path = '%s/%s' %(local_proj_path, proj)
            cloud_task_path = '%s/%s' %(cloud_proj_path, proj)

            local_task_list = next(os.walk(local_task_path))[1]
            cloud_task_list = next(os.walk(cloud_task_path))[1]

            # compare task lists and copy over necessary items
            for task in local_task_list:
                if task not in cloud_task_list:
                    print('Project: %s.\nEvaporating ** %s ** task file to the cloud.\n' %(proj, task))
                    os.system('cp -a -v %s/%s/%s %s/%s' %(local_proj_path, proj, task, cloud_proj_path, proj))


                    # update time on task -- project
                    # ------------------------------
                    # if adding new task, need to update project time on task
                    if proj != 'archive':
                        # open the files
                        cloud_time_on_task = open('%s/%s/time_on_task.txt' %(cloud_proj_path, proj), 'r')
                        local_task_time = open('%s/%s/%s/time_on_task.txt' %(local_proj_path, proj, task), 'r')

                        # get the values
                        cloud_time_on_task_value    = int(cloud_time_on_task.read())
                        local_task_time_value       = int(local_task_time.read())

                        cloud_time_on_task_value = cloud_time_on_task_value + local_task_time_value
                        cloud_time_on_task.close()
                        cloud_time_on_task = open('%s/%s/time_on_task.txt' %(cloud_proj_path, proj), 'w') #just tired of battling it...
                        cloud_time_on_task.write(str(cloud_time_on_task_value))

                        # close out files
                        cloud_time_on_task.close()
                        local_task_time.close()

                else: #the task is already there

                    # note update
                    # -----------
                    # note list
                    local_note_path = '%s/%s/%s' %(local_proj_path, proj, task)
                    cloud_note_path = '%s/%s/%s' %(cloud_proj_path, proj, task)

                    local_note_list = next(os.walk(local_note_path))[1]
                    cloud_note_list = next(os.walk(cloud_note_path))[1]

                    # compare and update notes as necessary
                    for note in local_note_list:
                        if note not in cloud_note_list:
                            print('Project: %s. Task: %s.\nEvaporating ** %s ** note file to the cloud.\n' %(proj, task, note))
                            os.system('cp -a -v %s/%s/%s/%s %s/%s/%s' %(local_proj_path, proj, task, note, cloud_proj_path, proj, note))


                            # update time on task -- task
                            # ---------------------------
                            # if add a new note, need to update time on task for task and project
                            if task != 'archive':
                                # get original time on task
                                old_cloud_time_on_task = open('%s/%s/%s/time_on_task.txt' %(cloud_proj_path, proj, task), 'r')
                                old_cloud_time_on_task_value = int(old_cloud_time_on_task.read())
                                old_cloud_time_on_task.close()

                                # delete old task time, copy over new task time 
                                os.system('rm -v -f %s/%s/%s/time_on_task.txt' %(cloud_proj_path, proj, task))
                                os.system('cp %s/%s/%s/time_on_task.txt %s/%s/%s' %(local_proj_path, proj, task, cloud_proj_path, proj, task))

                                # get new time on task
                                cloud_time_on_task              = open('%s/%s/%s/time_on_task.txt' %(cloud_proj_path, proj, task), 'r')
                                cloud_time_on_task_proj         = open('%s/%s/time_on_task.txt' %(cloud_proj_path, proj), 'r')

                                cloud_time_on_task_value        = int(cloud_time_on_task.read())
                                cloud_time_on_task_proj_value   = int(cloud_time_on_task_proj.read())

                                # get the amount of time to add to project
                                proj_task_time_add              = cloud_time_on_task_value - old_cloud_time_on_task_value
                                cloud_time_on_task_proj_value   = cloud_time_on_task_proj_value + proj_task_time_add

                                # update project time
                                cloud_time_on_task_proj.close()
                                cloud_time_on_task_proj         = open('%s/%s/time_on_task.txt' %(cloud_proj_path, proj), 'w')
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
                    os.system('cp -a -v %s/%s %s' %(cloud_task_path, task, local_task_path))


                    # update time on task -- project
                    # ------------------------------
                    # if adding new task, need to update project time on task
                    if proj != 'archive':
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
                            os.system('cp -a -v %s/%s/%s %s/%s' %(cloud_task_path, task, note, local_task_path, note))


                            # update time on task -- task
                            # ---------------------------
                            # if add a new note, need to update time on task for task and project
                            if task != 'archive':
                                # get original time on task
                                old_local_time_on_task = open('%s/%s/%s/time_on_task.txt' %(local_proj_path, proj, task), 'r')
                                old_local_time_on_task_value = int(old_local_time_on_task.read())
                                old_local_time_on_task.close()

                                # delete old task time, copy over new task time 
                                os.system('rm -v -f %s/%s/%s/time_on_task.txt' %(local_proj_path, proj, task))
                                os.system('cp %s/%s/%s/time_on_task.txt %s/%s/%s' %(cloud_proj_path, proj, task, local_proj_path, proj, task))

                                # get new time on task
                                local_time_on_task              = open('%s/%s/%s/time_on_task.txt' %(local_proj_path, proj, task), 'r')
                                local_time_on_task_proj         = open('%s/%s/time_on_task.txt' %(local_proj_path, proj), 'r')

                                local_time_on_task_value        = int(local_time_on_task.read())
                                local_time_on_task_proj_value   = int(local_time_on_task_proj.read())

                                # get the amount of time to add to project
                                proj_task_time_add              = local_time_on_task_value - old_local_time_on_task_value
                                local_time_on_task_proj_value   = local_time_on_task_proj_value + proj_task_time_add

                                # update project time
                                local_time_on_task_proj.close()
                                local_time_on_task_proj         = open('%s/%s/time_on_task.txt' %(local_proj_path, proj), 'w')
                                local_time_on_task_proj.write(str(local_time_on_task_proj_value))

                                # close files
                                local_time_on_task.close()
                                local_time_on_task_proj.close()