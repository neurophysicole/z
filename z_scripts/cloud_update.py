def cloud_update

    # import packages
    import os
    import sys
    reload(sys) #to help with seemingly random'ascii' encoding error
    sys.setdefaultencoding('utf8') # ^^ <--Python interpreter doesn't like it, but it works

    # import datetime packages
    import datetime
    from datetime import datetime, date

    # import time package
    import time

    # check for projects, then check for tasks within each project
    print('Checking the local and cloud files for asymmetries..')
    time.sleep(.1)

    # ========================
    # Update Master Log Sheet
    # ========================
    # ------
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

    local_archive_proj_path = '%s/archive' %main_dir
    cloud_archive_proj_path = '%s/archive' %backup_dir

    local_archive_proj_list = next(os.walk(local_archive_proj_path))[1]
    cloud_archive_proj_list = next(os.walk(cloud_archive_proj_path))[1]

    # get local master logfile information
    local_master_log = '%s/log.txt' %(local_proj_path) #find it
    read_local_master_log = open(local_master_log, 'r') #open it
    local_master_log_list = read_local_master_log.read().splitlines() #read it in

    # get cloud master logfile information
    cloud_master_log = '%s/log.txt' %(cloud_proj_path) #find it
    read_cloud_master_log = open(cloud_master_log, 'r') #open it
    cloud_master_log_list - read_cloud_master_log.read().splitlines() #read it in
    
    print('Updating projects..')
    time.sleep(.1)

    # =========================
    # Check Local Project List
    # =========================
    for proj in local_proj_list:

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


        # local project info
        local_task_path = '%s/%s' %(local_proj_path, proj)
        local_task_list = next(os.walk(local_task_path))[1]
        local_task_list.remove('archive')

        # get local active logfile info
        local_task_log = '%s/log.txt' %(local_task_path) #find it
        read_local_task_log = open(local_task_log, 'r') #open it
        local_task_log_list = read_local_task_log.read().splitlines() #read it in

        # figure out final log date/time
        last_line_local_task_list = local_task_log_list[-1] #find most recent
        last_line_local_task_list_split = last_line_local_task_list.split() #find date/time
        local_task_date = last_line_local_task_list_split[0] #pull out date
        local_task_time = int(last_line_local_task_list_split[2]) #pull out time

        # get local archive info
        local_archive_task_path = '%s/%s/archive' %(local_proj_path, proj)
        local_archive_task_list = next(os.walk(local_archive_task_path))[1]

        # ---------------
        # cloud proj info
        cloud_task_path = '%s/%s' %(cloud_proj_path, proj)
        cloud_task_list = next(os.walk(cloud_task_path))[1]
        cloud_task_list.remove('archive')

        # get logfile info
        cloud_task_log = '%s/log.txt' %(cloud_task_list_path) #find it
        read_cloud_task_log = open(cloud_task_log, 'r') #open it
        cloud_task_log_list = read_cloud_task_log.read().splitlines() #read it in

        # figure out final log date/time
        last_line_cloud_task_list = cloud_task_log_list[-1] #find most recent
        last_line_cloud_task_list_split = last_line_cloud_task_list.split() #find date/time
        cloud_task_date = last_line_cloud_task_list_split[0] #pull out date
        cloud_task_time = int(last_line_cloud_task_list_split[2]) #pull out time

        # get cloud archive info
        cloud_archive_task_path = '%s/archive' %(cloud_task_path)
        cloud_archive_task_list = next(os.walk(cloud_archive_task_path))[1]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # update each of the four proj locations (archive local, archive cloud, active local, archive local)
        # within each proj location, update the four task locations (archive local, archive cloud, active local, active cloud)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # --------------------------------------------------
        # check if proj is in the cloud active projects list
        if proj in cloud_proj_list: 

            # ----------------------------------------
            # if proj exists, check local active tasks
            for task in local_task_list:

                # get file info
                local_note_path = '%s/%s' %(local_task_path, task)
                local_note_list = next(os.walk(local_note_path))[1]
                local_archive_note_path = '%s/archive/%s' %(local_task_path, task)
                cloud_note_path = '%s/%s' %(cloud_task_path, task)

                # --------------
                # check for task
                if os.path.isdir(cloud_note_path):

                    # ---------------------------
                    # if task exists, check notes
                    for note in local_note_list:
                        cloud_note = '%s/%s' %(cloud_note_path, note)
                        local_note = '%s/%s' %(local_note_path, note)
                        if not os.path.isfile(cloud_note):
                            os.system('cp -v %s %s' %(local_note, cloud_note_path))
                    
                    print('Evaporating %s-%s task updates to the cloud.' %(proj, task))
                    os.system('rm -r -v -f %s' %local_note_path)
                    os.system('cp -a -v %s %s' %(cloud_note_path, local_task_path))
                    time.sleep(.1)

                else: #no task dir in cloud
                    # ---------------------------------------
                    # check the archived tasks within project
                    cloud_archive_note_path = '%s/%s' %(cloud_archive_task_path, task)
                    if os.path.isdir(cloud_archive_note_path):

                        # determine which is more up to date
                        cloud_archive_note_list = next(os.walk(cloud_archive_note_path))[2]

                        if local_task_date == cloud_task_date: #if dates are the same, need to compare log times
                            if local_task_time > cloud_task_time: #local most recent
                                evaporate_to_cloud = True
                            elif local_task_time < cloud_task_time: #cloud most recent
                                precipitate_from_cloud = True

                        if (local_task_date > cloud_task_date) or evaporate_to_cloud: #local is most recent
                            # precipitate notes to local, then evaporate local to cloud
                            for note in cloud_archive_note_list:
                                cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                                local_note = '%s/%s' %(local_note_path, note)
                                # check archive for non-overlapping stuff
                                if not os.path.isfile(local_note):
                                    # precipitate down from cloud
                                    os.system('cp -v %s %s' %(cloud_archive_note, local_note_path))

                            print('Evaporating %s-%s task updates to the cloud.' %(proj, task))
                            os.system('cp -a -v %s %s' %(local_note_path, cloud_task_path))
                            os.system('rm -r -v -f %s' %cloud_archive_note_path)
                            cloud_archive_task_list.remove(task) #move to active tasks in cloud -- already updated, so no need to update the cloud active projects list
                            time.sleep(.1)

                        elif (local_task_date < cloud_task_date) or precipitate_from_cloud: #cloud is most recent
                            # evaporate to cloud, then precipitate back to local
                            for note in local_note_list:
                                cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                                local_note = '%s/%s' %(local_note_path, note)
                                if not os.path.isfile(cloud_archive_note):
                                    os.system('cp -v %s %s' %(local_note, cloud_archive_note_path))
                            
                            print('Precipitating %s-%s task updates from the cloud.' %(proj, task))
                            os.system('cp -a -v %s %s' %(cloud_archive_note_path, local_archive_task_path)) #moved to local archive
                            os.system('rm -r -v -f %s' %local_note_path) #this is defunct
                            local_task_list.remove(task) #no longer in local task list
                            time.sleep(.1)

                    else: #task doesn't exist
                        print('Evaporating %s-%s to the cloud.' %(proj, task))
                        os.system('cp -a -v %s %s' %(local_note_path, cloud_task_path))
                        time.sleep(.1)

            # --------------------------
            # check local archived tasks
            for task in local_archive_task_list:

                # get archive task info
                local_archive_note_path = '%s/%s' %(local_archive_task_path, task)
                local_archive_note_list = next(os.walk(local_archive_note_path))[2]
                cloud_archive_note_path = '%s/%s' %(cloud_archive_task_path, task)
                cloud_archive_note_list = next(os.walk(cloud_archive_note_path))[2]

                # -----------------------
                # check the cloud archive
                if os.path.isdir(cloud_archive_note_path):

                    # if task is in archive, check that notes are up to date
                    for note in local_archive_note_list:
                        # evaporate to cloud, then precipitate back down
                        cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                        local_archive_note = '%s/%s' %(local_archive_note_path, note)
                        if not os.path.isfile(cloud_archive_note_path):
                            os.system('cp -v %s %s' %(local_archive_note, cloud_archive_note_path))
                        
                    print('Precipitating archived task information for %s-%s from the cloud.' %(proj, task))
                    os.system('rm -r -v -f %s' %local_archive_note_path) #remove it so there are no issues copying
                    os.system('cp -a -v %s %s' %(cloud_archive_note_path, local_archive_task_path))
                            
                else: #no task dir in cloud archived tasks
                    # --------------------------------------------------
                    # check active tasks within the project on the cloud
                    cloud_note_path = '%s/%s' %(cloud_task_path, task)
                    if os.path.isdir(cloud_note_path):

                        # determine which is more up to date
                        if local_task_date == cloud_task_date:
                            if local_task_time > cloud_task_time:
                                evaporate_to_cloud = True
                            elif local_task_time < cloud_task_time:
                                precipitate_from_cloud = True

                        if (local_task_date > cloud_task_date) or evaporate_to_cloud: #local more up to date
                            for note in cloud_note_list:
                                # precipitate from cloud, then evaporate back up
                                local_archive_note = '%s/%s' %(local_archive_note_path, note)
                                cloud_note = '%s/%s' %(cloud_note_path, note)
                                # check archive for non-overlapping stuff
                                if not os.path.isfile(local_archive_note):
                                    # precipitate down from cloud
                                    os.system('cp -v %s %s' %(cloud_note, local_archive_note_path))

                            print('Evaporating archived task information for %s-%s to the archived task folder in the cloud.' %(proj, task))
                            os.system('cp -a -v %s %s' %(local_archive_note_path, cloud_archive_task_path))
                            os.system('rm -r -v -f %s' %cloud_note_path) #moving to archive
                            cloud_task_list.remove(task)
                            time.sleep(.1)
                            
                        elif (local_task_date < cloud_task_date) or precipitate_from_cloud: #cloud more up to date
                            for note in local_archive_note_list:
                                # evaporate to cloud, then precipitate back down
                                cloud_archive_note = '%s/%s' %(cloud_note_path, note)
                                local_archive_note = '%s/%s' %(local_archive_note_path, note)
                                if not os.path.isfile(cloud_archive_note):
                                    # evaporate to cloud
                                    os.system('cp -v %s %s' %(local_archive_note, cloud_note_path))
                                
                            print('Precipitating %s-%s task info from cloud, and moving to active tasks.' %(proj, task))
                            os.system('cp -a -v %s %s' %(cloud_note_path, local_task_path))
                            os.system('rm -r -v -f %s' %local_archive_note_path)
                            local_archive_task_list.remove(task)
                            time.sleep(.1)

                    else: #task doesn't exist
                        print('Evaporating %s-%s (archived) to the cloud archive.' %(proj, task))
                        os.system('cp -a -v %s %s' %(local_archive_note_path, cloud_archive_task_path))                        

            # -------------------------------
            # check active tasks in the cloud
            for task in cloud_task_list:
                # get task info
                cloud_note_path = '%s/%s' %(cloud_task_path, task)
                cloud_note_list = next(os.walk(cloud_note_path))[1]
                cloud_archive_note_path = '%s/archive/%s' %(cloud_task_path, task)
                local_note_path = '%s/%s' %(local_task_path, task)
                local_archive_note_path = '%s/%s' %(local_archive_task_path, task)

                # --------------------------
                # check active tasks (local)
                if os.path.isdir(local_note_path):

                    # if task exists locally, check the notes
                    local_note_list = next(os.walk(local_note_path))[2]                
                    for note in local_note_list:
                        # evaporate to the cloud, then precipitate back down
                        local_note = '%s/%s' %(local_note_path, note)
                        cloud_note = '%s/%s' %(cloud_note_path, note)
                        if not os.path.isfile(cloud_note):
                            # evaporate to the cloud
                            os.system('cp -v %s %s' %(local_note_path, cloud_note_path))

                    print('Precipitating %s-%s down from the cloud.' %(proj, task))
                    os.system('cp -a -v %s %s' %(cloud_note_path, local_task_path))

                else: #no task dir in cloud
                    # ----------------------------
                    # check archived tasks (local)
                    if os.path.isdir(local_archive_note_path):

                        # determine which is more up to date
                        if local_task_date == cloud_task_date:
                            if local_task_time > cloud_task_time:
                                evaporate_to_cloud = True
                            elif local_task_time < cloud_task_time:
                                precipitate_from_cloud = True

                        if (local_task_date > cloud_task_date) or evaporate_to_cloud: #local more up to date
                            for note in cloud_note_list:
                                # precipitate down from cloud, then evaporate back up
                                local_archive_note = '%s/%s' %(local_archive_note_path, note)
                                cloud_note = '%s/%s' %(cloud_note_path, note)
                                # check archive for non-overlapping stuff
                                if not os.path.isfile(local_archive_note):
                                    # precipitate down from cloud
                                    os.system('cp -v %s %s' %(cloud_note, local_archive_note_path))

                            print('Evaporating %s task to the cloud %s archive.' %(proj, task))
                            os.system('cp -a -v %s %s' %(local_archive_note_path, cloud_archive_task_path))
                            os.system('rm -r -v -f %s' %cloud_note_path)
                            cloud_task_list.remove(task)
                            time.sleep(.1)

                        elif (local_task_date < cloud_task_date) or precipitate_from_cloud: #cloud more up to date
                            for note in local_archive_note_list:
                                # evaporate up to cloud then precipitate back down
                                cloud_note = '%s/%s' %(cloud_note_path, note)
                                local_archive_note = '%s/%s' %(local_archive_note_path, note)
                                # check archive for new stuff
                                if not os.path.isfile(cloud_note):
                                    os.system('cp -v %s %s' %(local_archive_note, cloud_note_path))
                                
                            print('Precipitating %s-%s task info from the cloud and moving from archived to active tasks.' (proj, task))
                            os.system('cp -a -v %s %s' %(cloud_note_path, local_task_path))
                            os.system('rm -r -v -f %s' %local_archive_note_path)
                            local_archive_task_list.remove(task)
                            time.sleep(.1)

                    else: #task doesn't exist
                        print('Precipitating %s-%s from the cloud.' %(proj, task))
                        os.system('cp -a -v %s %s' %(cloud_note_path, local_task_path))
                        time.sleep(.1)

            # --------------------------
            # check cloud archived tasks
            for task in cloud_archive_task_list:
                # get task info
                local_archive_note_path = '%s/%s' %(local_archive_task_path, task)
                local_archive_note_list = next(os.walk(local_archive_note_path))[2]
                cloud_archive_note_path = '%s/%s' %(cloud_archive_task_path, task)
                cloud_archive_note_list = next(os.walk(cloud_archive_note_path))[2]

                # -------------------
                # check local archive
                if os.path.isdir(local_archive_note_path):

                    # if exists in local archive, update notes
                    for note in local_archive_note_list:
                        # evaporate to the cloud then precipitate back down
                        local_archive_note = '%s/%s' %(local_archive_note_path, note)
                        cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                        if not os.path.isfile(cloud_archive_note_path):
                            # evaporate to the cloud
                            os.system('cp -v %s/%s %s' %(local_archive_note, cloud_archive_note_path))
                        
                    print('Precipitating %s-%s down to the local archive.' %(proj, task))
                    os.system('cp -a -v %s %s' %(cloud_archive_note_path, local_archive_task_path))
                    time.sleep(.1)

                else: #no task dir in cloud
                # ------------------------
                # check local active tasks   

                    # local_note_path = '%s/%s' %(local_task_path, task)
                    if os.path.isdir(local_note_path):
                        # determine which is more up to date
                        if local_task_date == cloud_task_date:
                            if local_task_time > cloud_task_time:
                                evaporate_to_cloud = True
                            elif local_task_time < cloud_task_time:
                                precipitate_from_cloud = True

                        if (local_task_date > cloud_task_date) or evaporate_to_cloud: #local is more up to date
                            for note in cloud_note_list:
                                # precipitate up then evaporate back down
                                cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                                local_note = '%s/%s' %(local_note_path, note)
                                # check archive for non-overlapping stuff
                                if not os.path.isfile(local_note):
                                    # precipitate down from cloud
                                    os.system('cp -v %s %s' %(cloud_archive_note, local_note_path))

                            print('Evaporating %s-%s up to the cloud and removing from the cloud archive.' %(proj, task))
                            os.system('cp -a -v %s %s' %(local_note_path, cloud_task_path))
                            os.system('rm -r -v -f %s' %cloud_archive_note_path)
                            cloud_archive_task_list.remove(task)
                            time.sleep(.1)
                            
                        elif (local_task_date < cloud_task_date) or precipitate_from_cloud: #cloud is more up to date
                            for note in local_note_list:
                                # evaporate to cloud, then precipitate back down
                                cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                                local_note = '%s/%s' %(local_note_path, note)
                                if not os.path.isfile(local_note):
                                    os.system('cp -v %s %s' %(local_note, cloud_archive_note_path))

                            print('Precipitating %s-%s from the cloud to the archive.' %(proj, task))
                            os.system('cp -a -v %s %s' %(cloud_archive_note_path, local_archive_task_path))
                            os.system('rm -r -v -f %s' %local_note_path)
                            local_task_list.remove(task)
                            time.sleep(.1)

                    else: #task doesn't exist
                        print('Precipitating %s-%s from the cloud to the archive.' %(proj, task))
                        os.system('cp -a -v %s %s' %(cloud_archive_note_path, local_archive_task_path))         
                        time.sleep(.1)               

        else: #proj not in cloud list
            # check for project in the archive
            if proj in cloud_archive_proj_list:
                # need to see what project is more up to date
                if local_task_date == cloud_task_date:
                    if local_task_time > cloud_task_time:
                        evaporate_to_cloud = True
                    elif local_task_time < cloud_task_time:
                        precipitate_from_cloud = True
                    else: #wtf
                        print('ERROR: There is an issue in determining which %s project is most up to date.' %proj)
                if local_task_date > cloud_task_date: #local project is more up to date
                    evaporate_to_cloud = True
                elif local_task_date < cloud_task_date: #cloud project is more up to date
                    precipitate_from_cloud = True
                else: #wtf
                    print('ERROR: There is an issue in determining which %s project is most up to date.' %proj)

                if (local_task_date > cloud_task_date) or evaporate_to_cloud: #local project is more up to date
                    # precipitate from cloud, then evaporate
                    for task in cloud_archive_task_list:
                        local_note_path = '%s/%s' %(local_task_path, task)
                        local_note_list = next(os.walk(local_task))[2]
                        cloud_archive_note_path = '%s/archive/%s' %(cloud_task_path, task)
                        cloud_archive_note_list = next(os.walk(cloud_archive_note_path))[2]

                        if os.path.isdir(cloud_archive_note_path):
                            for note in cloud_archive_note_list:
                                # precipitate to cloud
                                cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                                local_note = '%s/%s' %(local_note_path, note)
                                if not os.path.isfile(local_note):
                                    os.system('cp -v %s %s' %(cloud_archive_note, local_note_path))

                                print('Evaporating %s-%s to the cloud and removing from the cloud archive list.' %(proj, task))
                                os.system('cp -v %s %s' %(local_note, cloud_note_path))
                                os.system('rm -r -v -f %s' %cloud_archive_task)
                                cloud_archive_note_list.remove(task)
                                time.sleep(.1)

                        else: #task doesn't exist
                            # search the archive tasks
                            local_archive_task = '%s/archive/%s' %(local_task_path, task)
                            local_archive_note_list = next(os.walk(local_archive_task))[2]
                            if os.path.isdir(local_archive_task): #it is in the archive
                                for note in local_archive_note_list:
                                    # precipitate to cloud, then evaporate
                                    local_archive_note = '%s/%s' %(local_archive_task, note)
                                    cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                                    if not os.path.isfile(cloud_archive_note):
                                        os.system('cp -v %s/%s %s' %(local_archive_note, cloud_archive_note_path))

                                print('Evaporate %s-%s from the cloud.' %(proj, task))
                                os.system('cp -v %s %s' %(local_archive_task, cloud_archive_note_path))
                                time.sleep(.1)

                            else: #not in the archive.. doesn't exist
                                print('Precipitating %s-%s from cloud archive to local archive.' %(proj, task))
                                os.system('cp -a -v %s/%s %s' %(cloud_archive_task, local_archive_path))
                                time.sleep(.1)

                elif (local_task_date < cloud_task_date) or precipitate_from_cloud:
                    # evaporate to cloud, then precipitate
                    for task in local_task_path:
                        local_note_path = '%s/%s' %(local_task_path, task)
                        local_note_list = next(os.walk(local_note_path))[2]
                        cloud_archive_note_path = '%s/archive/%s' %(cloud_task_path, task)
                        cloud_archive_note_list = next(os.walk(cloud_archive_note_path))[2]

                        if os.path.isdir(local_note_path): 
                            for note in local_note_list:
                                # evaporate from cloud
                                cloud_archive_note = '%s/%s' %(cloud_archive_note_path, note)
                                local_note = '%s/%s' %(local_note_path, note)
                                if not os.path.isfile(cloud_archive_note):
                                    os.system('cp -v %s %s' %(local_note, cloud_archive_path))
                            
                            print('Evaporating %s-%s to the cloud archive from the local active list.' %(proj, task))
                            os.system('cp -v %s %s' %(cloud_archive_note_path, local_archive_task_path))
                            os.system('rm -r -v -f %s' %local_note_path)
                            local_task_list.remove(task)
                            time.sleep(.1)

            else: #doesn't exist
                print('Evaporating project %s to the cloud.' %proj)
                os.system('cp -a -v %s %s' %(local_task_path, cloud_task_path))
                time.sleep(.1)

    # project in the cloud but not in the local list
    for proj in cloud_proj_list:
        if proj not in local_proj_list:
            print('Precipitating %s from the cloud.' %proj)
            os.system('cp -a -v %s/%s %s' %(cloud_proj_path, proj, local_proj_path))
            time.sleep(.1)
    
    # project in the local archive, but not the cloud archive
    for proj in local_archive_proj_list:
        if proj not in cloud_archive_proj_list:
            print('Evaporating %s to the cloud.' %proj)
            os.system('cp -a -v %s/%s %s' %(local_archive_proj_path, proj, cloud_archive_proj_path))
            time.sleep(.1)

    # project in the cloud archive, but not the local archive
    for proj in cloud_archive_proj_list:
        if proj not in local_archive_proj_list:
            print('Precipitating %s from the cloud archive list to the local archive list.' %proj)
            os.system('cp -a -v %s/%s %s' %(cloud_archive_proj_path, proj, local_archive_proj_path))
            time.sleep(.1)


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
