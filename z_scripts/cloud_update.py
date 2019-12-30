def cloud_update(main_dir, backup_dir, segment, logfile):
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
    local_proj_path = '%s/%s' %(main_dir, segment)
    cloud_proj_path = '%s/%s' %(backup_dir, segment)
    
    local_proj_list = next(os.walk(local_proj_path))[1]
    if os.path.isdir(cloud_proj_path):
        print('Ckecing %s' %segment)
    else: #there is no segment dir in the cloud
        print('\nGrowing the new %s branch in the cloud.\n' %segment)
        os.system('mkdir %s/%s' %(backup_dir, segment))
        cloud_segment_log = open('%s/%s/log.txt' %(backup_dir, segment), 'w')
        cloud_segment_log.close()

    cloud_proj_list = next(os.walk(cloud_proj_path))[1]


    # compare lists
    proj_status     = set(local_proj_list) == set(cloud_proj_list)


    # ================
    # Log Sheet Check
    # ================
    # check that the local and cloud log sheets are all up to date
    local_logfile   = '%s/%s' %(main_dir, logfile)
    cloud_logfile   = '%s/%s' %(backup_dir, logfile)

    # set files
    local_log       = open(local_logfile, 'a+')
    local_log       = local_log.read()
    cloud_log       = open(cloud_logfile, 'a+')
    cloud_log       = cloud_log.read()

    # update to the cloud
    # -------------------
    # create a local list
    if set(local_log) == set(cloud_log):
        print('\nThe log files are up to date.\n')

    else: #the logfiles are different
        # logit
        for line in local_log:
            if line not in cloud_log:
                cloud_log.write(line)
        for line in cloud_log:
            if line not in local_log:
                local_log.write(line)

    # close the files
    # local_log.close()
    # cloud_log.close()

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
                os.system('cp -a -v %s/%s/%s %s/%s' %(main_dir, segment, proj, backup_dir, segment))
            else: #project is already updated
                print('\nProject ** %s ** is up to date in the cloud.\n' %proj)

            # task lists
            local_task_path = '%s/%s/%s' %(main_dir, segment, proj)
            cloud_task_path = '%s/%s/%s' %(backup_dir, segment, proj)

            local_task_list = next(os.walk(local_task_path))[1]
            cloud_task_list = next(os.walk(cloud_task_path))[1]

            # compare lists
            task_status = set(local_task_list) == set(cloud_task_list)


            # log update
            # ----------
            local_proj_log  = '%s/%s/%s/%s' %(main_dir, segment, proj, logfile)
            cloud_proj_log  = '%s/%s/%s/%s' %(backup_dir, segment, proj, logfile)

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

            # local_proj_log.close()
            # cloud_proj_log.close()

            # task update
            # -----------
            if task_status:
                print('\nLocal and Cloud task file structures are the same.\n')

            else: #something needs to be udpated in the tasks
                for task in local_task_list:
                    if task not in cloud_task_list:
                        print('Project: %s.\nEvaporating ** %s ** task file to the cloud.\n' %(proj, task))
                        os.system('cp -a -v %s/%s/%s/%s %s/%s/%s' %(main_dir, segment, proj, task, backup_dir, segment, proj))
                    else: #the task is already updated
                        print('\nTask ** %s ** in Project ** %s ** is up to date in the cloud.\n' %(task, proj))
        

                    # note list
                    local_note_path = '%s/%s/%s/%s' %(main_dir, segment, proj, task)
                    cloud_note_path = '%s/%s/%s/%s' %(backup_dir, segment, proj, task)

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
                                os.system('cp -a -v %s/%s/%s/%s/%s %s/%s/%s/%s' %(main_dir, segment, proj, task, note, backup_dir, segment, proj, note))
                            else: # the note is already updated
                                print('\nNote ** %s ** in Task ** %s ** in Project ** %s ** is up to date in the cloud.\n' %(note, task, proj))


        # copy projects from cloud
        # ------------------------
        for proj in cloud_proj_list:
            if proj not in local_proj_list:
                print('Precipitating ** %s ** project files from the cloud.' %proj)
                os.system('cp -a -v %s/%s/%s %s/%s' %(backup_dir, segment, proj, main_dir, proj))
            else: #project is already updated
                print('\nProject ** %s ** is up to date on the computer.\n' %proj)
            
            # task lists
            local_task_path = '%s/%s/%s' %(main_dir, segment, proj)
            cloud_task_path = '%s/%s/%s' %(backup_dir, segment, proj)

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
                        os.system('cp -a -v %s/%s/%s/%s %s/%s/%s' %(backup_dir, segment, proj, task, main_dir, segment, proj))

                    else: #the task is already updated
                        print('\nTask ** %s ** in Project ** %s ** is up to date on the computer.\n' %(task, proj))

                    # note list
                    local_note_path = '%s/%s/%s/%s' %(main_dir, segment, proj, task)
                    cloud_note_path = '%s/%s/%s/%s' %(backup_dir, segment, proj, task)

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
                                os.system('cp -a -v %s/%s/%s/%s/%s %s/%s/%s/%s' %(backup_dir, segment, proj, task, note, main_dir, segment, proj, note))
                            else: # the note is already updated
                                print('\nNote ** %s ** in Task ** %s ** in Project ** %s ** is up to date in the cloud.\n' %(note, task, proj))