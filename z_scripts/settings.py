def settings():
    # import command line packages
    import os

    # import date/time packages
    import datetime
    from datetime import datetime, date, timedelta

    # determine the paths
    laptop_path = '/Users/zcole/Documents/file_drawer/dev/z'
    imac_path   = '/Users/zjcole/Documents/file_drawer/dev/z'

    # set the path to use
    if os.path.isdir(laptop_path):
        main_dir        = laptop_path
        backup_dir      = '/Users/zcole/Box/file_drawer/z'
    elif os.path.isdir(imac_path):
        main_dir        = imac_path
        backup_dir      = '/Users/zjcole/Box/file_drawer/z'
    else: #impossible
        print('\nERROR:The path needs to be updated in the settings module.\n')
    
    # open the settings file
    settings_file = '%s/settings.txt' %(main_dir)
    settings_file = open(settings_file, 'r')
    settings_list = settings_file.read().splitlines()
     
    # date
    date        = datetime.today().date()
    date_format = '%m.%d.%Y'

    # ======================
    # Get Branch Variables
    # ======================

    for line in range(1, len(settings_list)):
        # current branch
        # find the start
        if settings_list[line] == 'CURRENT BRANCH START':
            cur_branch_start    = settings_list[(line + 1)]
            cur_branch_start    = datetime.strptime(cur_branch_start, date_format).date()

        # find the end
        elif settings_list[line] == 'CURRENT BRANCH END':
            cur_branch_end      = settings_list[(line + 1)]
            cur_branch_end      = datetime.strptime(cur_branch_end, date_format).date()

        # get the branch name
        elif settings_list[line] == 'CURRENT BRANCH NAME':
            cur_branch_name    = settings_list[(line + 1)]

        # next branch
        # get the branch name
        elif settings_list[line] == 'NEXT BRANCH START':
            next_branch_start   = settings_list[(line + 1)]
            next_branch_start   = datetime.strptime(next_branch_start, date_format).date()

        # find the end
        elif settings_list[line] == 'NEXT BRANCH END':
            next_branch_end     = settings_list[(line + 1)]
            next_branch_end     = datetime.strptime(next_branch_end, date_format).date()

        # get the branch name
        elif settings_list[line] == 'NEXT BRANCH NAME':
            next_branch_name    = settings_list[(line + 1)]

        elif settings_list[line] == 'DUPLICATE ID':
            duplicate_id        = settings_list[(line + 1)]

    # close settings file
    settings_file.close()

    # ========================
    # Confirm Current Branch
    # ========================

    if not cur_branch_start <= date <= cur_branch_end: #date is not within the boundaries of the current branch
        # update current and next branch
        confirm_renew_loop = True
        while confirm_renew_loop:
            confirm_renew = raw_input('\nRenewing the current branch.\n\nCONFIRM that this should be carried out (y/n): ')
            if confirm_renew == '':
                # need to update the current branch
                cur_branch_start   = next_branch_start
                cur_branch_end     = next_branch_end
                old_branch_name    = cur_branch_name
                cur_branch_name    = next_branch_name

                # need to update the next branch
                next_branch_start  = cur_branch_end + timedelta(days = 1) #just add one day
                next_branch_end    = raw_input('\nInput the date that the next branch should end (e.g., \'19-12-26\'):\n')
                next_branch_name   = raw_input('\nCome up with a name for the next branch (e.g., \'20_Fall\'):\n')

                print('\nOkay, the current branch is set to %s.\nIf for some reason, this is inaccurate, you will need to update the settings (during job selection -- coming up), or just manually update the settings in the \'settings.txt\' file.\n' %cur_branch_name)

                confirm_renew_loop = False

                # ======================
                # Establish New Branch
                # ======================
                # make new branch dir and move everything over there..
                # make new branch directory
                print('\nSetting up %s directory.\n' %cur_branch_name)

                os.system('mkdir %s/%s' %(main_dir, cur_branch_name))

                # make new log file
                newlog = open('%s/%s/log.txt' %(main_dir, cur_branch_name), 'w+')
                newlog.close()

                # move everything over
                # list projects in old branch directory
                old_branch_list = next(os.walk('%s/%s' %(main_dir, old_branch_name)))[1]

                # move all project dirs form old branch to new branch
                for seg_proj in old_branch_list:
                    os.system('mv -v -f %s/%s/%s %s/%s' %(main_dir, old_branch_name, seg_proj, main_dir, cur_branch_name))

                
                # =====================
                # Update Settings File
                # =====================
                # update the settings list
                for line in range(1, len(settings_list)):
                    # current branch
                    # find the start
                    if settings_list[line] == 'CURRENT BRANCH START':
                        settings_list[(line + 1)] = cur_branch_start

                    # find the end
                    elif settings_list[line] == 'CURRENT BRANCH END':
                        settings_list[(line + 1)] = cur_branch_end

                    # get the branch name
                    elif settings_list[line] == 'CURRENT BRANCH NAME':
                        settings_list[(line + 1)] = cur_branch_name

                    # next branch
                    # get the branch name
                    elif settings_list[line] == 'NEXT BRANCH START':
                        settings_list[(line + 1)] = next_branch_start

                    # find the end
                    elif settings_list[line] == 'NEXT BRANCH END':
                        settings_list[(line + 1)] = next_branch_end

                    # get the branch name
                    elif settings_list[line] == 'NEXT BRANCH NAME':
                        settings_list[(line + 1)] = next_branch_name

                # open the settings file
                settings_file = '%s/settings.txt' %(main_dir)
                with open(settings_file, 'w') as settings_file:
                    for line in settings_list:
                        settings_file.write('%s\n' %line)


            elif confirm_renew == 'n': #renewal not accepted
                print('\n!Aborting renewal. Current branch: %s! If this isn\'t right, you might have to restart and update it correctly; or just go into the \'settings.txt\' file and update the branch information manually.' %cur_branch_name)

                confirm_renew_loop = False


    # =================
    # check for backup
    # =================
    # if not connected to the internet 
    backup_check = str('%s/dev-git/z_scripts' %backup_dir)
    if os.path.isdir(backup_check):
        backup = True
    else:
        backup = False

    return backup, main_dir, backup_dir, cur_branch_name, duplicate_id