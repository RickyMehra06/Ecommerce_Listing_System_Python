import pandas as pd
from os import listdir
import pymongo
import getpass

class dBOperation:
    
    def __init__(self, logger):
        self.goodFilesPath = r"Good_Raw/"
        self.Application_logs = r'Application_logs/'
        self.logger =logger     
        
    def dataBaseConnection(self, user_name, user_password):      
    
        try:
            #user_name = input("Please enter your MongoDb_UserName: ")
            #user_password = getpass.getpass("Please enter your MongoDb Password: ")
            
            client = pymongo.MongoClient("mongodb+srv://"+user_name+":"+user_password+"@cluster0.gt9dl1l.mongodb.net/?retryWrites=true&w=majority")
            client.server_info()
            return client
           
            print("Mongodb is connected successfully!!\n")
            self.logger.log("Mongodb is connected successfully!!\n")  
        
        except Exception as e:
            print("Mongodb is not connected, please check your credentials or contact the administrator.\n" , str(e))
            self.logger.log("Mongodb is not connected, please check your credentials or contact the administrator.\n" , str(e))
    
    def replaceMissingWithNull(self):

        try:
            temp_df = pd.DataFrame()
            for file in listdir(self.goodFilesPath):
                temp_file = pd.read_excel(self.goodFilesPath+"/"+file)
                temp_df = temp_df.append(temp_file, ignore_index=True)
            
            if (temp_df.isnull().any().sum())>0:
                temp_df.fillna(0, inplace = True)
                temp_df['ISBN'] = [str(x) if not x else str(x).split('.')[0] for x in temp_df.ISBN] 
                #temp_df['ISBN'] = temp_df['ISBN'].astype('Int64').astype('str')
                temp_df['Date'] = temp_df['Date'].apply(str).str.split('T').str[0].str.split(" ").str[0]
                                  
                print("Missing values are replaced with zero for uploading raw data into the database.\n")
                self.logger.log("Missing values are replaced with zero for uploading raw data into the database.")
                return temp_df
            
            else:
                print("There is no missing values in the files of Good_Raw Folder.\n")
                self.logger.log("There is no missing values in the files of Good_Raw Folder.")
                return temp_df
            
        except Exception as e:
            print("There is a problem in replacing missing values.\n", str(e))
            self.logger.log("There is a problem in replacing missing values.\n", str(e))
    
    def insertIntoTableGoodData(self,temp_df, client):

        try:                                           
            database = client['GoodRawDb']
            collection = database["Invetory"]
            
            data_dict = temp_df.to_dict("records")
            collection.insert_many(data_dict)

            client.close()
                    
            print("Good Raw data has been uploaded in Mongodb successfully!! \n")
            self.logger.log("Good Raw data has been uploaded in Mongodb successfully!!")
        
        except Exception as e:
            print("Problem in uploading good raw data into Mongodb.\n"+ str(e))
            self.logger.log("Problem in uploading good raw data into Mongodb.\n"+ str(e))
            