def settings():
    # import command line packages
    import os

    # import date/time packages
    import datetime
    from datetime import datetime, date, timedelta

    # determine the paths
    laptop_path = '/Users/zcole/Documents/file_drawer/dev/z'
    imac_path   = '/Users/zjcole/Documents/z'

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

    # come up with number of lines in settings file
    # num_lines = sum(1 for line in open(settings_list))
     
    # date
    date = datetime.today().strftime('%m-%d-%Y')

    # ======================
    # Get Branch Variables
    # ======================

    for line in range(1, len(settings_list)):
        # current branch
        # find the start
        if settings_list[line] == 'CURRENT BRANCH START':
            cur_branch_start   = settings_list[(line + 1)]

        # find the end
        elif settings_list[line] == 'CURRENT BRANCH END':
            cur_branch_end     = settings_list[(line + 1)]

        # get the branch name
        elif settings_list[line] == 'CURRENT BRANCH NAME':
            cur_branch_name    = settings_list[(line + 1)]

        # next branch
        # get the branch name
        elif settings_list[line] == 'NEXT BRANCH START':
            next_branch_start  = settings_list[(line + 1)]

        # find the end
        elif settings_list[line] == 'NEXT BRANCH END':
            next_branch_end    = settings_list[(line + 1)]

        # get the branch name
        elif settings_list[line] == 'NEXT BRANCH NAME':
            next_branch_name   = settings_list[(line + 1)]


    # ========================
    # Confirm Current Branch
    # ========================

    if cur_branch_start <= date <= cur_branch_end:
        print('\nThe current branch is: %s.\n' %cur_branch_name)
    else: #date is not within the boundaries of the current branch
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

                #make new branch dir and move everything over there..
                # ======================
                # Establish New Branch
                # ======================
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

            elif confirm_renew == 'n': #renewal not accepted
                print('\n!Aborting renewal. Current branch: %s! If this isn\'t right, you might have to restart and update it correctly; or just go into the \'settings.txt\' file and update the branch information manually.' %cur_branch_name)

                confirm_renew_loop = False


    # =================
    # check for backup
    # =================
    # if not connected to the internet 
    if os.path.isdir(backup_dir):
        backup = True
    else:
        backup = False

    return backup, main_dir, backup_dir, cur_branch_name