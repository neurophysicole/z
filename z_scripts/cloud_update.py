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

    # compare lists
    proj_status     = set(local_proj_list) == set(cloud_proj_list)


    # ================
    # Log Sheet Check
    # ================
    # master
    # check that the local and cloud log sheets are all up to date
    local_master_logfile   = '%s/%s' %(local_proj_path, logfile)
    cloud_master_logfile   = '%s/%s' %(cloud_proj_path, logfile)

    # set files
    local_master_log = open(local_master_logfile, 'a+')
    local_master_log = local_master_log.read()
    cloud_master_log = open(cloud_master_logfile, 'a+')
    cloud_master_log = cloud_master_log.read()

    # project
    # check that the local and cloud log sheets are all up to date
    local_proj_logfile   = '%s/%s' %(local_proj_path, logfile)
    cloud_proj_logfile   = '%s/%s' %(cloud_proj_path, logfile)

    # set files
    local_proj_log = open(local_proj_logfile, 'a+')
    local_proj_log = local_proj_log.read()
    cloud_proj_log = open(cloud_proj_logfile, 'a+')
    cloud_proj_log = cloud_proj_log.read()


    # update to the cloud
    # -------------------
    # master
    # not doing project level because will need to iterate through and check all projects in case updates were made on a different computer
    # create a local list
    if set(local_master_log) == set(cloud_master_log):
        print('\nThe log files are up to date.\n')

    else: #the logfiles are different
        # logit
        for line in local_master_log:
            if line not in cloud_master_log:
                cloud_master_log.write(line)
        for line in cloud_master_log:
            if line not in local_master_log:
                local_master_log.write(line)

    # ===============
    # Run the update
    # ===============
    # project update with task update nested within
    if proj_status:
        print('\nLocal and Cloud project file structures are the same.\n')

    else: #something needs updated in the projects   

        # copy projects to cloud
        # ----------------------
        for proj in local_proj_list:
            if proj not in cloud_proj_list:
                print('\nEvaporating ** %s ** project file to the cloud.\n' %proj)
                os.system('cp -a -v %s/%s %s' %(local_proj_path, proj, cloud_proj_path))
            else: #project is already updated
                print('\nProject ** %s ** is up to date in the cloud.\n' %proj)

            # task lists
            local_task_path = '%s/%s' %(local_proj_path, proj)
            cloud_task_path = '%s/%s' %(cloud_proj_path, proj)

            local_task_list = next(os.walk(local_task_path))[1]
            cloud_task_list = next(os.walk(cloud_task_path))[1]

            # compare lists
            task_status = set(local_task_list) == set(cloud_task_list)


            # log update
            # ----------
            # project log
            local_proj_log  = '%s/%s/%s' %(local_proj_path, proj, logfile)
            cloud_proj_log  = '%s/%s/%s' %(cloud_proj_path, proj, logfile)

            local_proj_log  = open(local_proj_log, 'a+')
            local_proj_log  = local_proj_log.read()
            cloud_proj_log  = open(cloud_proj_log, 'a+')
            cloud_proj_log  = cloud_proj_log.read()

            if set(local_proj_log) == set(cloud_proj_log):
                print('\nProject log files up to date locally and on the cloud.\n')
            else: #cloud log needs updated
                # logit
                for line in local_proj_log:
                    if line not in cloud_proj_log:
                        cloud_proj_log.write(line)
                for line in cloud_proj_log:
                    if line not in local_proj_log:
                        local_proj_log.write(line)


            # task update
            # -----------
            if task_status:
                print('\nLocal and Cloud task file structures are the same.\n')

            else: #something needs to be udpated in the tasks
                for task in local_task_list:
                    if task not in cloud_task_list:
                        print('Project: %s.\nEvaporating ** %s ** task file to the cloud.\n' %(proj, task))
                        os.system('cp -a -v %s/%s/%s %s/%s' %(local_proj_path, proj, task, cloud_proj_path, proj))
                    else: #the task is already updated
                        print('\nTask ** %s ** in Project ** %s ** is up to date in the cloud.\n' %(task, proj))
        

                    # note list
                    local_note_path = '%s/%s/%s' %(local_proj_path, proj, task)
                    cloud_note_path = '%s/%s/%s' %(cloud_proj_path, proj, task)

                    local_note_list = next(os.walk(local_note_path))[1]
                    cloud_note_list = next(os.walk(cloud_note_path))[1]

                    # compare lists
                    note_status = set(local_note_list) == set(cloud_note_list)


                    # note update
                    # -----------
                    if note_status:
                        print('/nLocal and Cloud note file structures are the same.\n')

                    else: #something needs to be updated in the notes
                        for note in local_note_list:
                            if note not in cloud_note_list:
                                print('Project: %s. Task: %s.\nEvaporating ** %s ** note file to the cloud.\n' %(proj, task, note))
                                os.system('cp -a -v %s/%s/%s/%s %s/%s/%s' %(local_proj_path, proj, task, note, cloud_proj_path, proj, note))
                            else: # the note is already updated
                                print('\nNote ** %s ** in Task ** %s ** in Project ** %s ** is up to date in the cloud.\n' %(note, task, proj))


        # copy projects from cloud
        # ------------------------
        for proj in cloud_proj_list:
            if proj not in local_proj_list:
                print('Precipitating ** %s ** project files from the cloud.' %proj)
                os.system('cp -a -v %s/%s %s' %(cloud_proj_path, proj, local_proj_path))
            else: #project is already updated
                print('\nProject ** %s ** is up to date on the computer.\n' %proj)
            
            # task lists
            local_task_path = '%s/%s' %(local_proj_path, proj)
            cloud_task_path = '%s/%s' %(cloud_proj_path, proj)

            local_task_list = next(os.walk(local_task_path))[1]
            cloud_task_list = next(os.walk(cloud_task_path))[1]

            # compare lists
            task_status = set(local_task_list) == set(cloud_task_list)


            # task update
            # -----------
            if task_status:
                print('\nLocal and Cloud task file structures are the same.\n')

            else: #something needs to be updated in the tasks
                for task in cloud_task_list:
                    if task not in local_task_list:
                        print('Project: %s.\nPrecipitating ** %s ** task file from the cloud.\n' %(proj, task))
                        os.system('cp -a -v %s/%s %s' %(cloud_task_path, task, local_task_path))

                    else: #the task is already updated
                        print('\nTask ** %s ** in Project ** %s ** is up to date on the computer.\n' %(task, proj))

                    # note list
                    local_note_path = '%s/%s' %(local_task_path, task)
                    cloud_note_path = '%s/%s' %(cloud_task_path, task)

                    local_note_list = next(os.walk(local_note_path))[2]
                    cloud_note_list = next(os.walk(cloud_note_path))[2]

                    # compare lists
                    note_status = set(local_note_list) == set(cloud_note_list)


                    # note update
                    # -----------
                    if note_status:
                        print('/nLocal and Cloud note file structures are the same.\n')

                    else: #something needs to be updated in the notes
                        for note in cloud_note_list:
                            if note not in local_note_list:
                                print('Project: %s. Task: %s.\nPrecipitating ** %s ** note file from the cloud.\n' %(proj, task, note))
                                os.system('cp -a -v %s/%s/%s %s/%s' %(cloud_task_path, task, note, local_task_path, note))
                            else: # the note is already updated
                                print('\nNote ** %s ** in Task ** %s ** in Project ** %s ** is up to date in the cloud.\n' %(note, task, proj))