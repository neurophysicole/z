def print_proj_notes(proj_path, proj_name, notes_terminal):
    # printing all of the project notes before selecting the task could help inform of what needs to be worked on..
    
    # import command line packages
    import os

    # import time package
    import time

    # import dataframe packages
    import pandas as pd
    from tabulate import tabulate
    
    # get the task
    task_path = '%s/%s' %(proj_path, proj_name)
    task_list = next(os.walk(task_path))[1]
    task_list.remove('archive') #remove archive selection from task list
    # archive task list
    archive_task_path = '%s/archive' %task_path
    archive_task_list = next(os.walk(archive_task_path))[1]

    # list all proj notes
    # archive notes
    proj_header = str('\n\n===================\n===================\n\n%s NOTES - ARCHIVE\n\n===================\n===================\n\n' %proj_name.upper())
    os.system(str('echo \'%s\' > %s' %(proj_header, notes_terminal)))

    for archive_task in archive_task_list:
        # get the notes
        archive_note_dir    = '%s/archive/%s' %(task_path, archive_task)
        archive_note_list   = next(os.walk(archive_note_dir))[2]
        archive_note_list.remove('log.txt')
        archive_note_list.remove('dets.txt')
        archive_note_list   = sorted(archive_note_list)

        if '.DS_Store' in archive_note_list:
            os.system('rm -rf %s/.DS_Store' %archive_note_dir)
            archive_note_list.remove('.DS_Store')

        dets_file            = open('%s/dets.txt' %archive_note_dir, 'r')
        dets_file_contents   = dets_file.readlines()

        # task header
        task_header = str( '\n\n-------------------\n%s Task Notes - Archive\n-------------------\n\n' %archive_task )
        os.system(str('echo \'%s\' > %s' %(task_header, notes_terminal)))

        note_list = []
        dets_list = []
        date_list = []

        for archive_todo in archive_note_list:
            archive_note            = open('%s/%s' %(archive_note_dir, archive_todo), 'r')
            archive_note_contents   = archive_note.readlines()
            archive_todo            = os.path.splitext(archive_todo)[0][:-6]
            if len(archive_todo) == 0:
                continue

            for note_line in range(0, len(archive_note_contents)):
                this_note_line = archive_note_contents[note_line].split()
                if len(this_note_line) > 0:
                    if this_note_line[0][:-1] == archive_todo:
                        if len(this_note_line) > 0:
                            if this_note_line[0][:-1] == archive_todo:
                                note_find = True
                                note_find_line = note_line + 1
                                while note_find: #find end of note
                                    if note_find_line <= (len(archive_note_contents) - 1):
                                        if len(archive_note_contents[note_find_line].split()) > 0:
                                            if archive_note_contents[note_find_line].split()[0][:-1] == archive_todo:
                                                note_find = False
                                            else:
                                                note_find_line += 1
                                        else:
                                            note_find_line += 1
                                    else:
                                        note_find = False
                                    end_note = note_find_line - 1

                                note = ''
                                if note_line <= end_note:
                                    for note_line_contents in range((note_line + 2), end_note):
                                        note = note + '\n' + archive_note_contents[note_line_contents]

                        note = note.replace("'", "").replace('"', "")
                        note = note.split()

                        for note_word in range(0, len(note)):     

                            if len(note[note_word]) > 40:
                                old_word = note[note_word]
                                chunks = int(len(old_word) / 40)
                                new_word = ''
                                for i in range(1, chunks):
                                    bound_2 = i * 40
                                    bound_1 = bound_2 - 39
                                    segment = old_word[bound_1:bound_2]

                                    if i % 2 == 0:
                                        new_word = str('%s%s' %(new_word, segment))
                                    else:
                                        new_word = str('%s%s\n' %(new_word, segment))
                                
                                note[note_word] = new_word

                        if len(note) > 10:
                            old_list = note
                            chunks = int(len(old_list) / 10)
                            new_list = []
                            for k in range(1,chunks):
                                bound_2 = k * 10
                                bound_1 = bound_2 - 9
                                segment = old_list[bound_1:bound_2]
                                segment.append('\n')
                                segment = ' '.join(segment)
                                new_list.append(segment)

                            note = ' '.join(new_list)

                        else:
                            note = ' '.join(note)

                        if len(note) == 0:
                            note = ' '

                        note_list.append(note)

            for dets_line in range(0, len(dets_file_contents)):
                this_dets_line = dets_file_contents[dets_line].split()
                if len(this_dets_line) > 0:
                    if this_dets_line[0][:-1] == archive_todo:
                        dets = dets_file_contents[dets_line + 2].replace("'", "").replace('"', "")
                        dets = dets.split()

                        for dets_word in range(0, len(dets)):
                            
                            if len(dets[dets_word]) > 40:
                                old_word = dets[dets_word]
                                chunks = int(len(old_word) / 40)
                                new_word = ''
                                for i in range(1, chunks):
                                    bound_2 = i * 40
                                    bound_1 = bound_2 - 39
                                    segment = old_word[bound_1:bound_2]

                                    if i % 2 == 0:
                                        new_word = str('%s%s' %(new_word, segment))
                                    else:
                                        new_word = str('%s%s\n' %(new_word, segment))
                                
                                dets[dets_word] = new_word
    
                        if len(dets) > 10:
                            old_list = dets
                            chunks = int(len(old_list) / 10)
                            new_list = []
                            for k in range(1, chunks):
                                bound_2 = k * 10
                                bound_1 = bound_2 - 9
                                segment = old_list[bound_1:bound_2]
                                segment.append('\n')
                                segment = ' '.join(segment)
                                new_list.append(segment)

                            dets = ' '.join(new_list)
                        else:
                            dets = ' '.join(dets)

                        if len(dets) == 0:
                            dets = ' '
                            
                        dets_list.append(dets)
                        date_line = dets_file_contents[dets_line + 1].split()
                        date = date_line[0]

                        time_start = date_line[1]
                        if int(time_start) > 1259:
                            time_start_h = str('%.02i' %(int(time_start[:2]) - 12))
                            time_start_m = str('%.02i' %(int(time_start[2:])))
                            time_start = str('%s:%spm' %(time_start_h, time_start_m))
                        else:
                            time_start_h = str('%.02i' %(int(time_start[:2])))
                            time_start_m = str('%.02i' %(int(time_start[2:])))
                            time_start = str('%s:%sam' %(time_start_h, time_start_m))
                        time_end = date_line[2]
                        if int(time_end) > 1259:
                            time_end_h = str('%.02i' %(int(time_end[:2]) - 12))
                            time_end_m = str('%.02i' %(int(time_end[2:])))
                            time_end = str('%s:%spm' %(time_end_h, time_end_m))
                        else:
                            time_end_h = str('%.02i' %(int(time_end[:2])))
                            time_end_m = str('%.02i' %(int(time_end[2:])))
                            time_end = str('%s:%sam' %(time_end_h, time_end_m))
                        
                        date = str('%s :: %s - %s' %(date, time_start, time_end))
                        date_list.append(date)

            # make a dataframe 
            note_list = note_list[0:len(dets_list)] #this was a desparation move...

            for entry in range(0, len(date_list)):
                note_list[entry] = str('\n\n<----- %s ----->\n%s' %(date_list[entry], note_list[entry]))
                dets_list[entry] = str('\n\n<----- %s ----->\n%s' %(date_list[entry], dets_list[entry]))

            notes_df = pd.DataFrame({'Log': dets_list, 'Notes': note_list})
            notes_df = str(tabulate(notes_df, headers = 'keys', tablefmt = 'psql', showindex = False))

            # print note
            note_header = str( '\n\n%s\n-------------------\n\n' %(archive_todo) )

            os.system(str('echo \'%s\' > %s' %(note_header, notes_terminal)))
            os.system(str('echo \'%s\' > %s' %(notes_df, notes_terminal)))

            archive_note.close()
            dets_file.close()

            time.sleep(.1)

    time.sleep(.1)

    # active project notes
    proj_header = str('\n\n===================\n===================\n\n%s NOTES - ACTIVE\n\n===================\n===================\n\n' %proj_name.upper())
    os.system(str('echo \'%s\' > %s' %(proj_header, notes_terminal)))

    for task in task_list: #list of tasks in the project
        notes_dir    = '%s/%s' %(task_path, task)
        notes_list   = next(os.walk(notes_dir))[2]
        notes_list.remove('log.txt')
        notes_list.remove('dets.txt')
        notes_list   = sorted(notes_list)

        if '.DS_Store' in notes_list:
            os.system('rm -rf %s/.DS_Store' %notes_dir)
            notes_list.remove('.DS_Store')

        dets_file            = open('%s/dets.txt' %notes_dir, 'r')
        dets_file_contents   = dets_file.readlines()

        # task header
        task_header = str( '\n\n-------------------\n%s\n-------------------\n\n' %task )
        os.system(str('echo \'%s\' > %s' %(task_header, notes_terminal)))

        note_list = []
        dets_list = []
        date_list = []

        for task_todo in notes_list:
            task_note           = open('%s/%s' %(notes_dir, task_todo), 'r')
            task_note_contents  = task_note.readlines()
            task_todo            = os.path.splitext(task_todo)[0][:-6]
            if len(task_todo) == 0:
                continue

            for note_line in range(0, len(task_note_contents)):
                this_note_line = task_note_contents[note_line].split()
                if len(this_note_line) > 0:
                    if this_note_line[0][:-1] == task_todo:
                        if len(this_note_line) > 0:
                            if this_note_line[0][:-1] == task_todo:
                                note_find = True
                                note_find_line = note_line + 1
                                while note_find: #find end of note
                                    if note_find_line <= (len(task_note_contents) - 1):
                                        if len(task_note_contents[note_find_line].split()) > 0:
                                            if task_note_contents[note_find_line].split()[0][:-1] == task_todo:
                                                note_find = False
                                            else:
                                                note_find_line += 1
                                        else:
                                            note_find_line += 1
                                    else:
                                        note_find = False
                                    end_note = note_find_line - 1

                                note = ''
                                if note_line <= end_note:
                                    for note_line_contents in range((note_line + 2), end_note):
                                        note = note + '\n' + task_note_contents[note_line_contents]

                        note = note.replace("'", "").replace('"', "")
                        note = note.split()

                        for note_word in range(0, len(note)):     

                            if len(note[note_word]) > 40:
                                old_word = note[note_word]
                                chunks = int(len(old_word) / 40)
                                new_word = ''
                                for i in range(1, chunks):
                                    bound_2 = i * 40
                                    bound_1 = bound_2 - 39
                                    segment = old_word[bound_1:bound_2]

                                    if i % 2 == 0:
                                        new_word = str('%s%s' %(new_word, segment))
                                    else:
                                        new_word = str('%s%s\n' %(new_word, segment))
                                
                                note[note_word] = new_word

                        if len(note) > 10:
                            old_list = note
                            chunks = int(len(old_list) / 10)
                            new_list = []
                            for k in range(1,chunks):
                                bound_2 = k * 10
                                bound_1 = bound_2 - 9
                                segment = old_list[bound_1:bound_2]
                                segment.append('\n')
                                segment = ' '.join(segment)
                                new_list.append(segment)

                            note = ' '.join(new_list)

                        else:
                            note = ' '.join(note)

                        if len(note) == 0:
                            note = ' '

                        note_list.append(note)

            for dets_line in range(0, len(dets_file_contents)):
                this_dets_line = dets_file_contents[dets_line].split()
                if len(this_dets_line) > 0:
                    if this_dets_line[0][:-1] == task_todo:
                        dets = dets_file_contents[dets_line + 2].replace("'", "").replace('"', "")
                        dets = dets.split()

                        for dets_word in range(0, len(dets)):
                            
                            if len(dets[dets_word]) > 40:
                                old_word = dets[dets_word]
                                chunks = int(len(old_word) / 40)
                                new_word = ''
                                for i in range(1, chunks):
                                    bound_2 = i * 40
                                    bound_1 = bound_2 - 39
                                    segment = old_word[bound_1:bound_2]

                                    if i % 2 == 0:
                                        new_word = str('%s%s' %(new_word, segment))
                                    else:
                                        new_word = str('%s%s\n' %(new_word, segment))
                                
                                dets[dets_word] = new_word
    
                        if len(dets) > 10:
                            old_list = dets
                            chunks = int(len(old_list) / 10)
                            new_list = []
                            for k in range(1, chunks):
                                bound_2 = k * 10
                                bound_1 = bound_2 - 9
                                segment = old_list[bound_1:bound_2]
                                segment.append('\n')
                                segment = ' '.join(segment)
                                new_list.append(segment)

                            dets = ' '.join(new_list)
                        else:
                            dets = ' '.join(dets)

                        if len(dets) == 0:
                            dets = ' '
                            
                        dets_list.append(dets)
                        date_line = dets_file_contents[dets_line + 1].split()
                        date = date_line[0]

                        time_start = date_line[1]
                        if int(time_start) > 1259:
                            time_start_h = str('%.02i' %(int(time_start[:2]) - 12))
                            time_start_m = str('%.02i' %(int(time_start[2:])))
                            time_start = str('%s:%spm' %(time_start_h, time_start_m))
                        else:
                            time_start_h = str('%.02i' %(int(time_start[:2])))
                            time_start_m = str('%.02i' %(int(time_start[2:])))
                            time_start = str('%s:%sam' %(time_start_h, time_start_m))
                        time_end = date_line[2]
                        if int(time_end) > 1259:
                            time_end_h = str('%.02i' %(int(time_end[:2]) - 12))
                            time_end_m = str('%.02i' %(int(time_end[2:])))
                            time_end = str('%s:%spm' %(time_end_h, time_end_m))
                        else:
                            time_end_h = str('%.02i' %(int(time_end[:2])))
                            time_end_m = str('%.02i' %(int(time_end[2:])))
                            time_end = str('%s:%sam' %(time_end_h, time_end_m))
                        
                        date = str('%s :: %s - %s' %(date, time_start, time_end))
                        date_list.append(date)

            # make a dataframe 
            note_list = note_list[0:len(dets_list)] #this was a desparation move...

            for entry in range(0, len(date_list)):
                note_list[entry] = str('\n\n<----- %s ----->\n%s' %(date_list[entry], note_list[entry]))
                dets_list[entry] = str('\n\n<----- %s ----->\n%s' %(date_list[entry], dets_list[entry]))

            notes_df = pd.DataFrame({'Log': dets_list, 'Notes': note_list})
            notes_df = str(tabulate(notes_df, headers = 'keys', tablefmt = 'psql', showindex = False))

            # print note
            note_header = str( '\n\n%s\n-------------------\n\n' %(task_todo) )

            os.system(str('echo \'%s\' > %s' %(note_header, notes_terminal)))
            os.system(str('echo \'%s\' > %s' %(notes_df, notes_terminal)))

            task_note.close()
            dets_file.close()
            time.sleep(.1)

    time.sleep(.1)

    return task_path, task_list, archive_task_list


def print_task_notes(task_path, task_name, notes_terminal):
    # import command line packages
    import os

    # import time package
    import time

    # import dataframe packages
    import pandas as pd
    from tabulate import tabulate

    # current task notes
    task_header = str('\n\n===================\n===================\n\n%s TASK NOTES\n\n===================\n===================\n\n' %task_name.upper())
    os.system(str('echo \'%s\' > %s' %(task_header, notes_terminal)))

    notes_dir    = '%s/%s' %(task_path, task_name)
    notes_list   = next(os.walk(notes_dir))[2]
    notes_list.remove('log.txt')
    notes_list.remove('dets.txt')
    notes_list   = sorted(notes_list)

    if '.DS_Store' in notes_list:
        os.system('rm -rf %s/.DS_Store' %notes_dir)
        notes_list.remove('.DS_Store')

    dets_file            = open('%s/dets.txt' %notes_dir, 'r')
    dets_file_contents   = dets_file.readlines()

    note_list = []
    dets_list = []
    date_list = []

    for task_todo in notes_list:
        task_note           = open('%s/%s' %(notes_dir, task_todo), 'r')
        task_note_contents  = task_note.readlines()

        task_todo            = os.path.splitext(task_todo)[0][:-6]
        if len(task_todo) == 0:
            continue

        for note_line in range(0, len(task_note_contents)):
            this_note_line = task_note_contents[note_line].split()
            if len(this_note_line) > 0:
                if this_note_line[0][:-1] == task_todo:
                    if len(this_note_line) > 0:
                        if this_note_line[0][:-1] == task_todo:
                            note_find = True
                            note_find_line = note_line + 1
                            while note_find: #find end of note
                                if note_find_line <= (len(task_note_contents) - 1):
                                    if len(task_note_contents[note_find_line].split()) > 0:
                                        if task_note_contents[note_find_line].split()[0][:-1] == task_todo:
                                            note_find = False
                                        else:
                                            note_find_line += 1
                                    else:
                                        note_find_line += 1
                                else:
                                    note_find = False
                                end_note = note_find_line - 1

                            note = ''
                            if note_line <= end_note:
                                for note_line_contents in range((note_line + 2), end_note):
                                    note = note + '\n' + task_note_contents[note_line_contents]

                    note = note.replace("'", "").replace('"', "")
                    note = note.split()

                    for note_word in range(0, len(note)):     

                        if len(note[note_word]) > 40:
                            old_word = note[note_word]
                            chunks = int(len(old_word) / 40)
                            new_word = ''
                            for i in range(1, chunks):
                                bound_2 = i * 40
                                bound_1 = bound_2 - 39
                                segment = old_word[bound_1:bound_2]

                                if i % 2 == 0:
                                    new_word = str('%s%s' %(new_word, segment))
                                else:
                                    new_word = str('%s%s\n' %(new_word, segment))
                            
                            note[note_word] = new_word

                    if len(note) > 10:
                        old_list = note
                        chunks = int(len(old_list) / 10)
                        new_list = []
                        for k in range(1,chunks):
                            bound_2 = k * 10
                            bound_1 = bound_2 - 9
                            segment = old_list[bound_1:bound_2]
                            segment.append('\n')
                            segment = ' '.join(segment)
                            new_list.append(segment)

                        note = ' '.join(new_list)

                    else:
                        note = ' '.join(note)

                    if len(note) == 0:
                        note = ' '

                    note_list.append(note)

        for dets_line in range(0, len(dets_file_contents)):
            this_dets_line = dets_file_contents[dets_line].split()
            if len(this_dets_line) > 0:
                if this_dets_line[0][:-1] == task_todo:
                    dets = dets_file_contents[dets_line + 2].replace("'", "").replace('"', "")
                    dets = dets.split()

                    for dets_word in range(0, len(dets)):
                        
                        if len(dets[dets_word]) > 40:
                            old_word = dets[dets_word]
                            chunks = int(len(old_word) / 40)
                            new_word = ''
                            for i in range(1, chunks):
                                bound_2 = i * 40
                                bound_1 = bound_2 - 39
                                segment = old_word[bound_1:bound_2]

                                if i % 2 == 0:
                                    new_word = str('%s%s' %(new_word, segment))
                                else:
                                    new_word = str('%s%s\n' %(new_word, segment))
                            
                            dets[dets_word] = new_word
  
                    if len(dets) > 10:
                        old_list = dets
                        chunks = int(len(old_list) / 10)
                        new_list = []
                        for k in range(1, chunks):
                            bound_2 = k * 10
                            bound_1 = bound_2 - 9
                            segment = old_list[bound_1:bound_2]
                            segment.append('\n')
                            segment = ' '.join(segment)
                            new_list.append(segment)

                        dets = ' '.join(new_list)
                    else:
                        dets = ' '.join(dets)

                    if len(dets) == 0:
                        dets = ' '

                    dets_list.append(dets)

                    date_line = dets_file_contents[dets_line + 1].split()
                    date = date_line[0]

                    time_start = date_line[1]
                    if int(time_start) > 1259:
                        time_start_h = str('%.02i' %(int(time_start[:2]) - 12))
                        time_start_m = str('%.02i' %(int(time_start[2:])))
                        time_start = str('%s:%spm' %(time_start_h, time_start_m))
                    else:
                        time_start_h = str('%.02i' %(int(time_start[:2])))
                        time_start_m = str('%.02i' %(int(time_start[2:])))
                        time_start = str('%s:%sam' %(time_start_h, time_start_m))
                    time_end = date_line[2]
                    if int(time_end) > 1259:
                        time_end_h = str('%.02i' %(int(time_end[:2]) - 12))
                        time_end_m = str('%.02i' %(int(time_end[2:])))
                        time_end = str('%s:%spm' %(time_end_h, time_end_m))
                    else:
                        time_end_h = str('%.02i' %(int(time_end[:2])))
                        time_end_m = str('%.02i' %(int(time_end[2:])))
                        time_end = str('%s:%sam' %(time_end_h, time_end_m))
                    
                    date = str('%s :: %s - %s' %(date, time_start, time_end))
                    date_list.append(date)

        # make a dataframe 
        note_list = note_list[0:len(dets_list)] #this was a desparation move...

        for entry in range(0, len(date_list)):
            note_list[entry] = str('\n\n<----- %s ----->\n%s' %(date_list[entry], note_list[entry]))
            dets_list[entry] = str('\n\n<----- %s ----->\n%s' %(date_list[entry], dets_list[entry]))

        notes_df = pd.DataFrame({'Log': dets_list, 'Notes': note_list})
        notes_df = str(tabulate(notes_df, headers = 'keys', tablefmt = 'psql', showindex = False))

        # print note
        note_header = str( '\n\n%s\n-------------------\n\n' %(task_todo) )

        os.system(str('echo \'%s\' > %s' %(note_header, notes_terminal)))
        os.system(str('echo \'%s\' > %s' %(notes_df, notes_terminal)))

        task_note.close()
        dets_file.close()

        time.sleep(.1)

    time.sleep(.1)
