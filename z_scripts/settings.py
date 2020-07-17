def settings():
    # import command line packages
    import os

    # import date/time packages
    import datetime
    from datetime import datetime, date, timedelta

    # set the directories
    home_dir = os.getcwd()
    main_dir = os.path.dirname(os.path.abspath('%s/..' %__file__)) #main directory

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
        # get the branch name
        if settings_list[line] == 'CURRENT BRANCH NAME':
            cur_branch_name    = settings_list[(line + 1)]

        # next branch
        # get the branch name
        elif settings_list[line] == 'NEXT BRANCH START':
            next_branch_start   = settings_list[(line + 1)]
            next_branch_start   = datetime.strptime(next_branch_start, date_format).date()

        # get the branch name
        elif settings_list[line] == 'NEXT BRANCH NAME':
            next_branch_name    = settings_list[(line + 1)]

    # close settings file
    settings_file.close()

    # ========================
    # Confirm Current Branch
    # ========================

    if not date <= next_branch_start: #date is not within the boundaries of the current branch
        # update current and next branch
        confirm_renew_loop = True
        while confirm_renew_loop:
            confirm_renew = input('\nRenewing the current branch.\n\nCONFIRM that this should be carried out (y/n): ')
            if confirm_renew == '':
                # need to update the current branch
                old_branch_name    = cur_branch_name
                cur_branch_name    = next_branch_name

                # need to update the next branch
                next_branch_name   = input('\nCome up with a name for the next branch (e.g., \'20_Fall\'):\n')
                next_branch_start  = input('\nInput the date that the next branch should start (e.g., \'19-12-26\'):\n')

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
                    # get the branch name
                    if settings_list[line] == 'CURRENT BRANCH NAME':
                        settings_list[(line + 1)] = cur_branch_name

                    # next branch
                    # get the branch name
                    elif settings_list[line] == 'NEXT BRANCH START':
                        settings_list[(line + 1)] = next_branch_start

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

    # ====================
    # Set Terminal Windows
    # ====================
    terminal        = int(input('What is the terminal ID? (e.g., \'1\')\nNote, it is always one more than what is actually listed in the Terminal window:  '))
    notes_terminal  = terminal + 1
    dets_terminal   = terminal + 2

    # open new terminal windows
    os.system('open -n -a Terminal')
    os.system('open -n -a Terminal')

    return main_dir, home_dir, cur_branch_name, notes_terminal, dets_terminal