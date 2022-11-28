import os
from os import listdir
from datetime import datetime

class app_logger:
    def __init__(self):
        self.Application_logs = r"Application_logs/"
    
    def log_folder(self):
        try:  
            if not os.path.isdir(self.Application_logs):
                os.makedirs(self.Application_logs)
                print("Log folder is created successfully.\n")
            else:
                for f in listdir(self.Application_logs):
                    os.remove(self.Application_logs + "/" + f)
                    print("Previous log file has been deleted.\n")
        except Exception as e:
            print("There is a problem in log folder, kindly review.\n", str(e))
            
    def log(self, message):
        try:
            self.now = datetime.now()
            self.date = self.now.date()
            self.current_time = self.now.strftime("%H:%M:%S")
            
            with open('Application_logs/log_file.txt', 'a+') as f:
                f.write(str(self.date) + "--" + str(self.current_time) + "\t" + message +"\n")
                f.close()
                #print("Log file is updated successfully.\n")
        except Exception as e:
            print("There is a problem in updating log file.\n", str(e))