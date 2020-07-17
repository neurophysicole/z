def print_proj_notes(proj_path, proj_name, notes_terminal, dets_terminal):
    # printing all of the project notes before selecting the task could help inform of what needs to be worked on..
    
    # import command line packages
    import os

    # import time package
    import time

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
    os.system(str('echo \'%s\' > /dev/ttys00%i' %(proj_header, notes_terminal)))

    for archive_task in archive_task_list:
        # get the notes
        archive_note_dir    = '%s/archive/%s' %(task_path, archive_task)
        archive_note_list   = next(os.walk(archive_note_dir))[1]
        archive_note_list   = sorted(archive_note_list)

        # task header
        task_header = str( '\n\n-------------------\n%s Task Notes - Archive\n-------------------\n\n%s\n\n' %archive_task )
        os.system(str('echo \'%s\' > /dev/ttys00%i' %(task_header, notes_terminal)))

        for archive_todo in archive_note_list:
            archive_note            = open('%s/%s' %(archive_note_dir, archive_todo), 'r')
            archive_note_contents   = archive_note.read()
            archive_note.close()

            # print note
            note = str( '\n\n%s To Do\n-------------------\n%s\n' %(os.path.splitext(archive_todo)[0], archive_note_contents) )
            os.system(str('echo \'%s\' > /dev/ttys00%i' %(note, notes_terminal)))

    time.sleep(.1)

    # active project notes
    proj_header = str('\n\n===================\n===================\n\n%s NOTES - ACTIVE\n\n===================\n===================\n\n' %proj_name.upper())
    os.system(str('echo \'%s\' > /dev/ttys00%i' %(proj_header, notes_terminal)))

    for task in task_list: #list of tasks in the project
        note_dir    = '%s/%s' %(task_path, task)
        note_list   = next(os.walk(note_dir))[1]
        note_list   = sorted(note_list)

        # task header
        task_header = str( '\n\n-------------------\n%s Task Notes\n-------------------\n\n' %task )
        os.system(str('echo \'%s\' > /dev/ttys00%i' %(task_header, notes_terminal)))

        for task_todo in note_list:
            task_note           = open('%s/%s' %(note_dir, task_todo), 'r')
            task_note_contents  = task_note.read()
            task_note.close()

            # print note
            note = str( '\n\n%s To Do\n-------------------\n%s\n' %(os.path.splitext(task_todo)[0], task_note_contents) )
            os.system(str('echo \'%s\' > /dev/ttys00%i' %(note, notes_terminal)))

    time.sleep(.1)

    return task_path, task_list, archive_task_list


def print_task_notes(task_path, task_name, notes_terminal, dets_terminal):
    # import command line packages
    import os

    # import time package
    import time

    # current task notes
    task_header = str('\n\n===================\n===================\n\n%s TASK NOTES\n\n===================\n===================\n\n' %task_name.upper())
    os.system(str('echo \'%s\' > /dev/ttys00%i' %(task_header, notes_terminal)))

    note_dir    = '%s/%s' %(task_path, task_name)
    note_list   = next(os.walk(note_dir))[2]
    note_list   = sorted(note_list)

    for task_todo in note_list:
        task_note           = open('%s/%s' %(note_dir, task_todo), 'r')
        task_note_contents  = task_note.read()
        task_note.close()

        # print note
        note = str( '\n\n%s To Do\n-------------------\n%s\n' %(os.path.splitext(task_todo)[0], task_note_contents) )
        os.system(str('echo \'%s\' > /dev/ttys00%i' %(note, notes_terminal)))

    time.sleep(.1)


def print_proj_details(proj_path, proj_name, notes_terminal, dets_terminal):
    # import command line packages
    import os

    # import time package
    import time

    # get the task
    task_path = '%s/%s' %(proj_path, proj_name)

    # active project notes
    det_header = str('\n\n===================\n===================\n\n%s DETS\n\n===================\n===================\n\n' %proj_name.upper())

    os.system(str('echo \'%s\' > /dev/ttys00%i' %(det_header, dets_terminal)))

    dets_file       = open('%s/dets.txt' %task_path, 'r')
    dets_contents   = dets_file.read()
    dets_file.close()

    dets = str('%s' %dets_contents)
    os.system(str('echo \'%s\' > /dev/ttys00%i' %(dets, dets_terminal)))

    return task_path