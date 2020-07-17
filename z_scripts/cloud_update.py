def repo_pull(home_dir, main_dir):

    # load packages
    import os
    import sys

    # pullit
    os.system('cd %s' %main_dir) #need to pull from the repo directory
    os.system('git pull')

    os.system('cd %s' %home_dir) #return back to the home directory

def repo_commit(home_dir, main_dir, proj_name, task_name, task_details):

    # load packages
    import os
    import sys

    # commit
    os.system('cd %s' %main_dir) #need to be in the repo directory
    os.system('git commit -m \"%s: %s: %s\"' %(proj_name, task_name, task_details)) #commit message consists of the task details

    os.system('cd %s' %home_dir) #return back to the home directory

def repo_push(home_dir, main_dir):

    # load packages
    import os
    import sys

    # pushit
    os.system('cd %s' %main_dir) #move into the repo directory
    os.system('git push origin master')

    os.system('cd %s' %home_dir) #move back to the home directory