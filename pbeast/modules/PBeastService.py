import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import sys
from backup import BackUp


class PBeastService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PBeastService'
    _svc_display_name_ = 'Project Beast'
    _svc_description_ = 'This service is used to back up your app designer projects every hour'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()

    def main(self):
        self.ret_code = None
        print('\nBackup service started....\n')
        while self.ret_code != win32event.WAIT_OBJECT_0:
            # one hour = 3600000ms or 1*60*60*1000
            pause_time_milisecs = 8*60*60*1000
            print('Projects to back up......\n')
            pbObject = BackUp()
            pbObject.backup_to_file()
            # block for specified miliseconds (1 hr)
            # wait for a stop event
            self.ret_code = win32event.WaitForSingleObject(
                self.hWaitStop, pause_time_milisecs)
        print('\nShutting down service \n')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PBeastService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PBeastService)
