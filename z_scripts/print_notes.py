def print_proj_notes(proj_path, proj_name):
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
    print('\n\n-------------------\n-------------------\n\n%s NOTES - ARCHIVE\n\n' %proj_name.upper())
    for archive_task in archive_task_list:
        archive_note_dir = '%s/archive/%s' %(task_path, archive_task)
        archive_note_list = next(os.walk(archive_note_dir))[2]
        archive_note_list.remove('time_on_task.txt')
        for archive_tasknote in archive_note_list:
            archive_note = open('%s/%s' %(archive_note_dir, archive_tasknote), 'r')
            archive_note_contents = archive_note.read()
            print('\n> %s\n -- %s\n%s\n' %(archive_task, archive_tasknote, archive_note_contents))
            archive_note.close()

    time.sleep(.1)

    # active project notes
    print('\n\n-------------------\n-------------------\n\n%s NOTES - ACTIVE\n\n' %proj_name.upper())
    for task in task_list: #list of tasks in the project
        task_dir = '%s/%s' %(task_path, task)
        task_dir = next(os.walk(task_dir))[2]
        task_dir.remove('time_on_task.txt')
        for note in task_dir: #list of the notes within the task
            tasknote = open('%s/%s/%s' %(task_path, task, note), 'r')
            tasknote_contents = tasknote.read()
            print('\n> %s\n -- %s\n%s\n' %(task, note, tasknote_contents))
            tasknote.close()

    time.sleep(.1)

    return task_path, task_list, archive_task_list


def print_task_notes(task_path, task_name):
    # import command line packages
    import os

    # import time package
    import time

    # current task notes
    print('\n\n-------------------\n-------------------\n\n%s NOTES\n\n' %task_name.upper())
    note_dir = '%s/%s' %(task_path, task_name)
    note_dir = next(os.walk(note_dir))[2]
    note_dir.remove('time_on_task.txt')
    for note in note_dir: #list all of the notes within the current task
        note_tasknote = open('%s/%s/%s' %(task_path, task_name, note), 'r')
        note_tasknote_contents = note_tasknote.read()
        print('\n--> %s\n%s\n' %(note, note_tasknote_contents))
        note_tasknote.close()

    time.sleep(.1)