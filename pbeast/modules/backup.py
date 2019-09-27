# backup.py

from __future__ import print_function

import cx_Oracle
import subprocess
from datetime import datetime as dttm
from config import Settings


class BackUp:
    '''class used to back up projects'''
    # use a separate config file to store these values 
    # ------------------------------------------------------------------------------------
    #               set the connection properties TNS/DB connection
    # ------------------------------------------------------------------------------------
    src_host = Settings.DB_HOST
    src_service = Settings.DB_SERVICE_NAME
    port = Settings.DB_PORT
    db_username = Settings.DB_USERNAME
    db_passwd = Settings. DB_PASSWORD
    dsn_tns = cx_Oracle.makedsn(src_host, port, service_name=src_service)

    # ---------------------------------------------------------------------------------------
    #              Get Connection properties
    # ---------------------------------------------------------------------------------------
    client_version = cx_Oracle.clientversion()
    # ---------------------------------------------------------------------------------------
    #             Folders and file locations
    # ---------------------------------------------------------------------------------------
    backup_path = Settings.BACKUP_PATH
    log_filepath = Settings.LOG_FILEPATH
    batch_file = Settings.BATCH_FILE
    log_filename = r'log.txt'

    # count of projects
    project_count = 0

    def write_to_file(self, line, filename, path):
        ''' Helper function for writing lines into a file.
        Appends to an existing or creates a new one. Takes string to be written,
        the file name, and absolute path as arguments '''
        if path and path[-1] != '\\':
            path = path + '\\'
        if line.strip() and filename:
            file = open(path + filename, 'a')
            # write to file
            file.write(str(line)+'\n')
            # print to console
            print(line)
            file.close()
        else:
            print('No valid file name or path provided.')

    def run_cmdline(self, file):
        ''' Run the .bat file that does the actual back up process.
    Takes the absolute path/file name as argument'''
        msg = ''
        try:
            if file.strip():
                file_details = file.split('\\')
                filename = file_details[len(file_details)-1]
                BackUp.write_to_file(
                    self, f"\nRunning {filename} .....", self.log_filename, self.log_filepath)
                # run the subroutine
                subprocess.CompletedProcess = subprocess.run(
                    [file],  text=True, capture_output=True)
                # get the results from the run command
                ret_code = subprocess.CompletedProcess.returncode
                ret_error = subprocess.CompletedProcess.stderr
                ret_sdtout = subprocess.CompletedProcess.stdout
                if ret_code == 0:
                    # successfully ran .bat file
                    msg = f"End running {filename} file.....\n{ret_sdtout}"
                else:
                    msg = f'\nReturn code: {ret_code}\n{ret_error}'
            else:
                msg = "Please provide a complete file location"
        except:
            msg = "There was an error running the .bat file"
        finally:
            BackUp.write_to_file(
                self, msg, self.log_filename, self.log_filepath)
    # ------------------------------------------------------------------------------------
    #               Connect to the database
    #               get the list of projects
    #               write it to a file
    # ------------------------------------------------------------------------------------

    def conntect_to_db(self, username, passwd):
        self.username = username
        self.password = passwd
        msg = ''
        try:
            conn = cx_Oracle.connect(
                user=self.username, password=self.password, dsn=self.dsn_tns)
            msg = '\nSuccessfully connected to ' + self.src_service
            return conn
        except cx_Oracle.DatabaseError as ex:
            msg = '\nDatabase Error:\n ' + str(ex)
        except cx_Oracle.InterfaceError as ix:
            msg = '\nInterface Error:\n ' + str(ix)
        finally:
            BackUp.write_to_file(
                self, msg, self.log_filename, self.log_filepath)

    def get_projects(self):
        ''' Queries the list of changed/new
         projects and writes it to a file '''
        self.project_count = 0
        conn = BackUp.conntect_to_db(
            self, self.db_username, self.db_passwd)
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT projectname,
                    projectdescr,
                    lastupddttm,
                    lastupdoprid
                FROM SYSADM.PSPROJECTDEFN
                WHERE lastupddttm > (SELECT CREATED
                                FROM
                                V$DATABASE)""")
            for projectname, projectdescr,lastupddttm, lastupdoprid in cursor:
                projectname = projectname
                projectdescr = projectdescr
                lastupddttm = lastupddttm
                lastupdoprid = lastupdoprid
                # create projectlist.txt file
                BackUp.write_to_file(self,
                                     projectname, 'projectlist.txt', BackUp.backup_path)
                self.project_count += 1
            # close thecursor object and connection
            cursor.close()
            conn.close()
            return self.project_count
        else:
            msg = 'No project list created. Connection was not established to the database'
            BackUp.write_to_file(self,
                                 msg, self.log_filename, self.log_filepath)
            return self.project_count

    # Copy projects to a file

    def backup_to_file(self):
        ''' Copy projects to file. Calls the run_cmdline() method only if project files
        were successfully created by the get_projects() method.'''
        BackUp.write_to_file(
            self, f'\n'+('*'*20) + 'BEGIN - ' + str(dttm.now(tz=None)) +' ' + ('*'*20), self.log_filename, self.log_filepath)
        queried_projects = BackUp.get_projects(
            self)
        BackUp.write_to_file(
            self, f'{queried_projects} projects to back up.', self.log_filename, self.log_filepath)
        if queried_projects and queried_projects >= 0:
            BackUp.run_cmdline(self, self.batch_file)
        BackUp.write_to_file(
            self, f'\n'+('*'*20) + 'END - '+str(dttm.now(tz=None))+' ' + ('*'*20), self.log_filename, self.log_filepath)
    # To implemented later

    def backup_to_database(self):
        ''' Copy projects to a database. To be implemented '''
        pass


# this block will not execute when imported
# only use to debug/test the file
if __name__ == "__main__":
    # create a backup object
    bkObj = BackUp()
    bkObj.backup_to_file()
