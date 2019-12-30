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
    # Get Segment Variables
    # ======================

    for line in range(1, len(settings_list)):
        # current segment
        # find the start
        if settings_list[line] == 'CURRENT SEGMENT START':
            cur_segment_start   = settings_list[(line + 1)]

        # find the end
        elif settings_list[line] == 'CURRENT SEGMENT END':
            cur_segment_end     = settings_list[(line + 1)]

        # get the segment name
        elif settings_list[line] == 'CURRENT SEGMENT NAME':
            cur_segment_name    = settings_list[(line + 1)]

        # next segment
        # get the segment name
        elif settings_list[line] == 'NEXT SEGMENT START':
            next_segment_start  = settings_list[(line + 1)]

        # find the end
        elif settings_list[line] == 'NEXT SEGMENT END':
            next_segment_end    = settings_list[(line + 1)]

        # get the segment name
        elif settings_list[line] == 'NEXT SEGMENT NAME':
            next_segment_name   = settings_list[(line + 1)]


    # ========================
    # Confirm Current Segment
    # ========================

    if cur_segment_start <= date <= cur_segment_end:
        print('\nThe current segment is: %s.\n' %cur_segment_name)
    else: #date is not within the boundaries of the current segment
        # update current and next segment
        confirm_renew_loop = True
        while confirm_renew_loop:
            confirm_renew = raw_input('\nRenewing the current segment.\n\nCONFIRM that this should be carried out (y/n): ')
            if confirm_renew == '':
                # need to update the current segment
                cur_segment_start   = next_segment_start
                cur_segment_end     = next_segment_end
                old_segment_name    = cur_segment_name
                cur_segment_name    = next_segment_name

                # need to update the next segment
                next_segment_start  = cur_segment_end + timedelta(days = 1) #just add one day
                next_segment_end    = raw_input('\nInput the date that the next segment should end (e.g., \'19-12-26\'):\n')
                next_segment_name   = raw_input('\nCome up with a name for the next segment (e.g., \'20_Fall\'):\n')

                print('\nOkay, the current segment is set to %s.\nIf for some reason, this is inaccurate, you will need to update the settings (during job selection -- coming up), or just manually update the settings in the \'settings.txt\' file.\n' %cur_segment_name)

                confirm_renew_loop = False

                #make new segment dir and move everything over there..
                # ======================
                # Establish New Segment
                # ======================
                # make new segment directory
                print('\nSetting up %s directory.\n' %cur_segment_name)

                os.system('mkdir %s/%s' %(main_dir, cur_segment_name))

                # make new log file
                newlog = open('%s/%s/log.txt' %(main_dir, cur_segment_name), 'w+')
                newlog.close()

                # move everything over
                # list projects in old segment directory
                old_segment_list = next(os.walk('%s/%s' %(main_dir, old_segment_name)))[1]

                # move all project dirs form old segment to new segment
                for seg_proj in old_segment_list:
                    os.system('mv -v -f %s/%s/%s %s/%s' %(main_dir, old_segment_name, seg_proj, main_dir, cur_segment_name))

            elif confirm_renew == 'n': #renewal not accepted
                print('\n!Aborting renewal. Current segment: %s! If this isn\'t right, you might have to restart and update it correctly; or just go into the \'settings.txt\' file and update the segmeent information manually.' %cur_segment_name)

                confirm_renew_loop = False


    # =================
    # check for backup
    # =================
    # if not connected to the internet 
    if os.path.isdir(backup_dir):
        backup = True
    else:
        backup = False

    return backup, main_dir, backup_dir, cur_segment_name