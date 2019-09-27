:: Developed by fmawelle
:: No warranties whatsoever

:: This file can be run manually or automatically
:: if automatic, it is assumed that another process
:: checks if  new/changed projects exists
:: if it does, the files is then executed as follows:

:: prevent input/prompts from being displayed
@echo off

:: ----------------------App Designer Location----------------------------------
:: change directory to the directory where the pside is installed
c:
cd C:\PT8.57.07_Client_ORA\bin\client\winx86 

:: -----------------------The Back Up Process-----------------------------------
:: if you stored your projects for backup in a list in a txt file
:: each line representing a project to be backed up then
:: for each line or project name in your projectlist.txt
:: %i = projectname
:: backup the project
:: the first directory is where the projectlist.txt file is written 
:: the second directory is where the projects will actually be backed up to
:: the last directory is where your log files will be written to
FOR /F %%i in (C:\Users\user\Documnents\pbeast\Projects\projectlist.txt) DO PSIDE -HIDE -QUIET -CT ORACLE -CS 192.168.1.112 -CD CS92U014 -CO  PS -CP houston -PJTF %%i -FP C:\Users\user\Documnents\pbeast\Projects -LF C:\Users\user\Documnents\pbeast\Projects\%%i.log

:: rename the project list file
:: and archive it
:: D:
:: cd C:\Users\YOURUSERHERE\FOLDER\FOLDER\FOLDER - Where is the projectlist.txt written to?
cd C:\Users\user\Documnents\pbeast\Projects
FOR /f "tokens=1-8 delims=:./ " %%G IN ("%date%_%time%") DO (SET datetime=%%G%%H%%I%%J%%K)
SET archiveFile=projectlist_%datetime%.txt
rename projectlist.txt %archiveFile%
:: where do you want to move the archival file to?
:: move %archiveFile% C:\Users\YOURUSER\FOLDER\FOLDER\FOLDER\FOLDER - Or whereever you want the files to be archived to
move %archiveFile% C:\Users\user\Documnents\pbeast\Projects\_archives_