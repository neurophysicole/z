
# zpz
This project has been my first real work in Python - well, my first real programming work entirely, really. So heads up if anything weird happens.

### Functionality
- This program was designed on Mac, using Python 2.7. Not sure if it will work under any other circumstances..
- To work this program, you will also have to download some Python packages (all listed in the beginning of the main z.py file.
- If you are working with Py3, you may use a different version of PySimpleGUI (what I have downloaded is for Py2.7).

### Structure
- This program stores notes in individual text files and logs activity in two separate logs (one project log within the project folder, and one master log in the main folder).
- The folder structure is split into _scheduled segments_ > _project segments_ > and _task segments_.
- The scheduled segments are meant to be something like semesters or years, or whatever you specify.
- When a new project is developed, a new project folder is created.
- When a new task is developed, a new task folder is created.
- All notes made will be stored in individual text files within the task folder. Each session will be assigned its own text file (named according to date and time).
- When a project is completed, it is moved to the main archive.
- When a task is completed, it is moved to the project archive.
- Time-on-task is summed and stored in a text file within the relevant folder.
- Everything is backed up by being copied to a Box folder -- this may have to be adapted depending on your file structure -- I have a Box Drive folder stored on my computers so I am able to be working with a completely up-to-date version of my work/note history.
- Settings are stored in a settings.py file, and some settings are read from a settings.txt file.
