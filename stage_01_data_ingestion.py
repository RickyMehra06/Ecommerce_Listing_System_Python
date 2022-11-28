import pandas as pd
import os
import os.path
from os import listdir
import shutil
import json
import re 

import warnings
warnings.filterwarnings('ignore')

class fileHandling():
    def __init__(self,logger):
        self.goodFilesPath = r"Good_Raw/".strip("\u202a")
        self.badFilesPath = r"Bad_Raw/"
        self.schema_path = r'Table_Schema_Sample.json'
        self.pattern = ('Dist_Inventory_'+ r'\d{1}_\d{2}-\d{2}-\d{4}')
        self.Application_logs = r'Application_logs/'
        self.logger =logger

    def __getitem__(self, key):
        return self.__dict__[key]            
    
    def validateFileNames(self, path):
        try:  
            if not os.path.isdir(self.goodFilesPath):
                os.makedirs(self.goodFilesPath)
            else:
                for f in listdir(self.goodFilesPath):
                    os.remove(self.goodFilesPath + "/" + f)
            
            if not os.path.isdir(self.badFilesPath):
                os.makedirs(self.badFilesPath)
            else:
                for f in listdir(self.badFilesPath):
                    os.remove(self.badFilesPath + "/" + f)
                    
        except Exception as e:
            print("There is a problem in Good or Bad File path.\n", str(e))
            self.logger.log("There is a problem in Good or Bad File path.", str(e))
            
        try:         
            for file in listdir(path):
                f_name = os.path.basename(file).split(".")[0]          
                match = re.search(self.pattern, f_name)           
                if f_name == match.group():
                    shutil.copy(path + '/'+ f_name + '.xlsx', self.goodFilesPath)
                    print("{} moved to Good_Files Folder.\n" .format(f_name))
                    self.logger.log("{} moved to Good_Files Folder." .format(f_name))
       
                else:
                    shutil.copy(path + '/'+ f_name + '.xlsx', self.badFilesPath)
                    print("{} moved to Bad_Files Folder.\n" .format(f_name))
                    self.logger.log("{} moved to Bad_Files Folder." .format(f_name))
        
        except Exception as e:
            print("Please review the file naming convention.\n", str(e))
            self.logger.log("Please review the file naming convention.", str(e))              
        
    def validateColumnsLength(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                #print(dic)
                f.close()
                col_names= dic["ColName"]
                NumberofColumns = dic["NumberofColumns"]
        
            for file in listdir(self.goodFilesPath):
                temp_file = pd.read_excel(self.goodFilesPath + '\\'+ file)
                temp_file.dtypes
                
                if temp_file.shape[1] == NumberofColumns:
                    print("{} file has same numbers of columns as table schema!!\n" .format(file.split(".")[0]))
                    self.logger.log("{} file has same numbers of columns as table schema." .format(file.split(".")[0]))
                else:
                    shutil.move(self.goodFilesPath + '/'+ file, self.badFilesPath)
                    print("{} file does not have same numbers of columns as table schema and moved to Bad Files Folder!!\n" .format(file.split(".")[0]))
                    self.logger.log("{} file does not have same numbers of columns as table schema and moved to Bad Files Folder." .format(file.split(".")[0]))
            return col_names, NumberofColumns
        
        except Exception as e:
            print("There is a problem in validating number of columns of the files.\n", str(e))
            self.logger.log("There is a problem in validating number of columns of the files.", str(e))
            
    def validateMissingValuesInWholeColumn(self):
        try:
            for file in listdir(self.goodFilesPath):
                temp_file = pd.read_excel(self.goodFilesPath + '\\'+ file)
                #print(file)
                for columns in temp_file:
                    if (len(temp_file[columns]) - temp_file[columns].count()) == len(temp_file[columns]):
                        shutil.move(self.goodFilesPath + '/'+ file, self.badFilesPath)
                        print("{} column of the {} has All Missing values. \n" .format(columns, file.split(".")[0]))
                        self.logger.log("{} column of the file {} has All Missing values." .format(columns, file.split(".")[0]))
                        break    # If one of the column is empty then it will move to bad file folder & starts reading next file
                    else:
                        print("{} column of the file {} is non-empty whole column.\n" .format(columns, file.split(".")[0]))
                        self.logger.log("{} column of the file {} is non-empty whole column" .format(columns, file.split(".")[0]))
        
        except Exception as e:
            print("There is a problem in validating missing values in the entire column.\n", str(e))    
            self.logger.log("There is a problem in validating missing values in the entire column.", str(e))
        
    def validateSchemaNames(self, col_names, NumberofColumns):
        try:
            for file in listdir(self.goodFilesPath):
                #print(file)
                dic_df = {}                
                temp_file = pd.read_excel(self.goodFilesPath + '\\'+ file)
                for i, j in zip(temp_file.columns, temp_file.dtypes):
                    dic_df.update({str(i) : str(j)})
                    #print(dic_df)

                count = 0        
                for (a,b), (x,y) in zip(dic_df.items(), col_names.items()):
                    if (a in x) & (b in y):
                        count += 1
                        continue                     
                    
                if count == NumberofColumns:
                    print("{} has valid schema file !! \n" .format(file.split(".")[0]))
                    self.logger.log("{} has valid schema file." .format(file.split(".")[0]))          
                else:
                    shutil.move(self.goodFilesPath + '/'+ file, self.badFilesPath)
                    print("{} does NOT have valid schema file !! \n" .format(file.split(".")[0]))  
                    self.logger.log("{} does NOT have valid schema file." .format(file.split(".")[0]))  
                
        except Exception as e:
            print("There is a problem in validating file schema name.\n", str(e))
            self.logger.log("There is a problem in validating file schema name.", str(e))

