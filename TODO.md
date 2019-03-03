## Remaining Tasks
- ### Main Application
    - create a exe file of complete project
## Done
- ### UI
    - file chooser of selecting exe's
    - loginScreen, settingsScreen, dashboard 
    - User Register and Auth using json file
    - Make code more redable, cogent, modular 
    - Recheck all the functions and corner cases
    - Recheck all the var assignments and their passing
    - Encrypt and decrypt val of password before writing to file
## Issues
- ### UI
    - if a user wants to save settings for app pref's, he has to select/reselect all, (even if he wants to change only one pref) else there will be error " Please check for such corner conditions "
    - if password is empty it will take it empty, getPwd is not working
    - if fields are empty at the time of saving(save_func) i.e user has not selected the vals (from file chooser) in that session it gives error (not solvable, atleast easily, needs major change in handling data)