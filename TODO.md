## Remaining Tasks
- ### Main Application
    - Change the paths in detector_utils.py && recognize.py to relative
    - To replace keyboard q interrupt by time like 30 sec in recognize.py
    - connect backend to frontend 
    - Add startup script for applications after probabilitiy vals are found
## Partially Done
    - Data set (Static model) 
    - static model implementation
## Done
- ### UI
    - file chooser of selecting exe's
    - loginScreen, settingsScreen, dashboard 
    - User Register and Auth using json file
    - Make code more redable, cogent, modular 
    - Recheck all the functions and corner cases
    - Recheck all the var assignments and their passing
    - Encrypt and decrypt val of password before writing to file
## Dropped
- dynamic model implementation 
- Data set (Dynamic model)
## Issues
- ### UI
    - if a user wants to save settings for app pref's, he has to select/reselect all else there will be error even if he wants to change only one pref (error at checking empty) [Solved] " Please check for corner conditions "
    - if password is empty it will take it empty, getPwd is not working
