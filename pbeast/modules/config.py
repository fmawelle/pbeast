from pathlib import Path
import pathlib

class Settings:
    ''' Class to hold connection settings and file locations 
     change the assignment values here to match your settings '''
    # Database connection settings
    DB_HOST = '111.111.1.111' # change this to either the IP address or the host name of your database
    DB_SERVICE_NAME = 'CS92U014' # this is the service name for connection to your Oracle DB
    DB_PORT = 1521 # Most likely the port will remain the same (1521), if not change it to the correct one that matches yours
    DB_USERNAME = 'SYSTEM' # Which user will be used to access the DB?
    DB_PASSWORD = 'password' # The user password

    # file location settings
    # The projectlist.txt will be  written here. 
    # This directory should match with the directory in backup.bat that references the projectlist.txt
    # and the one where the projects will be backed up to
    BACKUP_PATH = r'C:\Users\user\Documnents\pbeast\Projects'
    
    # this is where logs related to the process will be logged, 
    # This is different from the logs from app designer 
    # The logs from app designer project will be written to the same direcory as the backup path
    LOG_FILEPATH =  r'C:\Users\user\Documnents\pbeast\Projects\_logs_'
    
    # this should be the full path of the .bat file that is included with this project
    BATCH_FILE = r'C:\Users\user\Documnents\pbeast\backup.bat' 