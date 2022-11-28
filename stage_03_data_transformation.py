import pandas as pd
import os
import os.path
from os import listdir
from datetime import date


class preProcessor:    
    def __init__(self, logger):
        self.goodFilesPath = r"Good_Raw/"
        self.invalid_path = "Invalid_rows\\"
        self.masterFilePath = r'Input_Master_Data\Master_File.xlsx'
        self.noAsinDetailsFilePath = r'No_Asin_File'
        
        self.shipping_file_path = r'Input_Master_Data\Shipping_Charge.xlsx'
        self.today = date.today()

        self.Application_logs = r'Application_logs/'
        self.logger =logger
        
    def readFilesFromDir(self):
        try:
            df=pd.DataFrame()
            count=0
            for file in listdir(self.goodFilesPath):
                temp_file = pd.read_excel(self.goodFilesPath+"/"+file)
                count = count+1
                df = df.append(temp_file, ignore_index=True)
            df['ISBN'] = [str(x).split('.')[0] for x in df.ISBN]
            df['ISBN'] = [str(int(x)) if isinstance(x, int) else str(x) for x in df.ISBN]  # Int can take max 10 digits so converted in str
            
            for x in df.select_dtypes(include=['datetime64']).columns.tolist():   # To convert Datetime to string, use below code
                df[x] = df[x].astype(str)
            print("{} number of files located in the Good_Raw Files Folder.\n" .format(count))
            self.logger.log("{} number of files located in the Good_Raw Files Folder." .format(count))
            return df
        
        except Exception as e:
            print("Problem in reading Good_Raws files and in creating dataframe.\n"+ str(e))
            self.logger.log("Problem in reading Good_Raws files and in creating dataframe.\n"+ str(e))

    def validateMissingValues(self, df):

        invalid_df = pd.DataFrame()   
        
        try:
            invalid_df = df[df.isna().any(axis=1)]
            df.dropna(axis = 0, inplace = True)     # df.dropna(axis = 0, how ='any')
            print("{} number of rows have missing values.\n" .format(invalid_df.shape[0]))
            self.logger.log("{} number of rows have missing values." .format(invalid_df.shape[0]))
            return df, invalid_df
        
        except Exception as e:
            print("There is a problem in removing missing values from rows.\n", str(e))
            self.logger.log("There is a problem in removing missing values from rows.\n", str(e))
            
    def removeNon13ISBN(self, df, invalid_df):
        
        df['ISBN'] = df['ISBN'].astype(str)
        df['ISBN13_len'] = df['ISBN'].apply(len)
        invalid_count= invalid_df.shape[0]
       
        try:                       
            invalid_df = invalid_df.append(df.loc[df['ISBN13_len'] != 13])
            df.drop(df[df.ISBN13_len != 13].index, inplace = True)
            df.drop(["ISBN13_len","Date"], axis = 1, inplace = True)
            #df.reset_index(inplace = True, drop = True)
            print("{} ISBNs are not of exactly 13 digits and removed from listing.\n" .format(invalid_df.shape[0]-invalid_count))
            self.logger.log("{} ISBNs are not of exactly 13 digits and removed from listing." .format(invalid_df.shape[0]-invalid_count))
            return df, invalid_df
        
        except Exception as e:
            df.drop(["ISBN13_len","Date"], axis = 1, inplace = True)
            #df.reset_index(inplace = True, drop = True)
            print("All ISBNs are of exactly 13 digits !!\n", str(e))
            self.logger.log("All ISBNs are of exactly 13 digits.", str(e))
            return df, invalid_df              
         
        # To convert ISBN13 column into STRING sothat Merge function can pick vale from Master 
        #df["ISBN13"] = df["ISBN13"].astype(str)
        
    def validateCurrencyCode(self, df, invalid_df):

        currency_list = ['INR', 'USD', 'CAD', 'EUR', 'GBP']
        invalid_count= invalid_df.shape[0]
        
        try:
            invalid_df = invalid_df.append(df[~df['Currency'].isin(currency_list)], ignore_index=True)
            df = df[df['Currency'].isin(currency_list)]
            #df.reset_index(inplace = True, drop=True)
            print("{} number of rows have invalid currency code.\n". format(invalid_df.shape[0]-invalid_count))
            self.logger.log("{} number of rows have invalid currency code.". format(invalid_df.shape[0]-invalid_count))
            return df, invalid_df
        
        except Exception as e:
            print("Problem in validating currency code.\n"+ str(e))
            self.logger.log("Problem in validating currency code.\n"+ str(e))
   
    def validatePrice(self,df, invalid_df):

        invalid_count= invalid_df.shape[0]
        
        try:
            invalid_df = invalid_df.append(df.loc[df['Price']<=0])
            df = df.loc[df['Price']>0]
            #df.reset_index(inplace = True, drop=True)
            print("{} number of rows have price less than or equals to zero.\n". format(invalid_df.shape[0]-invalid_count))
            self.logger.log("{} number of rows have price less than or equals to zero.". format(invalid_df.shape[0]-invalid_count))
            return df, invalid_df
        
        except Exception as e:
            print("Problem in validating price less than or equals to zero.\n"+ str(e))
            self.logger.log("{} number of rows have price less than or equals to zero.". format(invalid_df.shape[0]-invalid_count))
    
    def validateQuantity(self, df, invalid_df):

        today = date.today()        
        try:
            invalid_count= invalid_df.shape[0]
            invalid_df = invalid_df.append(df.loc[df['Quantity']<=0])
            invalid_df.reset_index(inplace = True, drop=True)
            
            if not os.path.isdir(self.invalid_path):
                os.makedirs(self.invalid_path)
            else:
                for f in listdir(self.invalid_path):
                    os.remove(self.invalid_path + "/" + f)
            invalid_df.to_excel(self.invalid_path+ "/Invalid_Raws_File_"+str(today)+'.xlsx', index = False)
                    
            df = df.loc[df['Quantity']>0]
            df.reset_index(inplace = True, drop=True)
            print("{} number of rows have Qunatity less than or equals to zero.\n". format(invalid_df.shape[0]-invalid_count))
            self.logger.log("{} number of rows have Qunatity less than or equals to zero.". format(invalid_df.shape[0]-invalid_count))
            return df, invalid_df
        
        except Exception as e:
            print("Problem in validating Quatity less than or equals to zero.\n"+ str(e))
            self.logger.log("Problem in validating Quatity less than or equals to zero.\n"+ str(e))
        
    def dropQuantityBelowThreshold(self, data):
        try:
            for enum, (i,j) in enumerate(zip(data["Publisher"], data["Quantity"])):
                
                if (i in ["Osprey","Paragon","Amex"]) & (j <=3):
                    data.drop(([enum]), axis = 0, inplace = True)
                   
                elif (i in ["IBBD","CP","Tson"]) & (j <=4):
                    data.drop(([enum]), axis = 0, inplace = True)
                
                elif (i in ["Rappa","GBD","RBC"]) & (j<=5):
                    data.drop(([enum]), axis = 0, inplace = True)
                
                elif (i == "WBC") & (j<=6):
                    data.drop(([enum]), axis = 0, inplace = True)               
              
                else:
                    pass
            data.reset_index(inplace = True, drop=True)
            print("Quantities deleted below threshold levels.\n")
            self.logger.log("Quantities deleted below threshold levels.")
            return data
                    
        except Exception as e:
            print("Problem deleting quantity below threshold level for respective distributor.\n"+ str(e))
            self.logger.log("Problem deleting quantity below threshold level for respective distributor.\n"+ str(e))
                       
   
    def createQuantityBins(self, data):
        
        max_quantity = data['Quantity'].max()
        bins = [1,10,25,50,100,max_quantity+1]
        group = [2,5,10,25,50]
        
        try:
            data['Quantity'] = pd.cut(data['Quantity'], bins, labels=group) # This line will change the data type to "Category"
            data['Quantity'] = data['Quantity'].astype(int)       
            data.reset_index(inplace = True, drop = True)
            print("Quantities converted into respective bins...\n")
            self.logger.log("Quantities converted into respective bins.")
            #X.to_excel(r"class4B_validate.xlsx", index = None)
            return data
        
        except Exception as e:
            print("Problem in creating the bins for Quantity.\n"+ str(e))
            self.logger.log("Problem in creating the bins for Quantity.\n"+ str(e))
            
    def masterAsinFile(self):        
        try:
            master = pd.read_excel(self.masterFilePath)
            master['ISBN'] = [str(int(x)) if isinstance(x, int) else str(x) for x in master['ISBN']]
            print("Master file has been loaded successfully.\n")
            self.logger.log("Master file has been loaded successfully.")
            return master
        
        except Exception as e:
            print("There is a problem in reading ASIN master file.\n\n", str(e))
            self.logger.log("There is a problem in reading ASIN master file.\n\n", str(e))
    
    def combineDataWithMasterFile(self, data, master):

        today = date.today()        
        try:
            data = pd.merge(data, master[["ISBN", "ASIN10", "Weight", "Status", "Disclaimer"]], on = 'ISBN', how ='left')
            data.drop(data[data["Weight"] >= 2.500].index, inplace = True)
            data.drop(data[data["Status"] == "Barred"].index, inplace = True)
            
            data_no_asin = data[pd.isnull(data["ASIN10"])]
            
            try:  
                if not os.path.isdir(self.noAsinDetailsFilePath):
                    os.makedirs(self.noAsinDetailsFilePath)
                else:
                    for f in listdir(self.noAsinDetailsFilePath):
                        os.remove(self.noAsinDetailsFilePath + "/" + f)
                        
                data_no_asin.to_excel(self.noAsinDetailsFilePath+ "/Required_ASIN_Details_"+str(today)+'.xlsx', index = False)
                print("{} ISBNs have no ASIN and weight available in the master file, please check Required_ASIN_Details file.\n" .format(len(data_no_asin)))
                self.logger.log("{} ISBNs have no ASIN and weight available in the master file, please check Required_ASIN_Details file." .format(len(data_no_asin)))

            except Exception as e:
                print("There is a problem in creating file for ISBNs whose ASIN are not available.\n", str(e))  
                self.logger.log("There is a problem in creating file for ISBNs whose ASIN are not available.\n", str(e))  
            
            data = data[pd.notnull(data["ASIN10"])]
            data.reset_index(inplace = True, drop = True)
            return data
       
        except Exception as e:
            print("There is a problem in reading master file.\n", str(e))
            self.logger.log("There is a problem in reading master file.\n", str(e))
    
    def currencyConversionAsPerGOC(self, data):
        try:
            inr_price = []
            for x, y in zip(data["Currency"], data["Price"]):
                if x in ["GBP", "UKP"]:
                    temp_price =  y * 100.60            # GBP/INR Rate
                elif x in ["EUR", "EURO", "EU"]:
                    temp_price =  y * 86.40             # EUR/INR Rate
                elif x == "USD":
                    temp_price =  y * 82.40             # USD/INR Rate
                elif x == "CAD":
                    temp_price =  y * 63.90             # CAD/INR Rate
                else:
                    temp_price =  y
                inr_price.append(temp_price)
            
            data["INR_Price"] = inr_price
            
            print("Prices converted as per GOC rates (Brought into INR).\n")
            self.logger.log("Prices converted as per GOC rates (Brought into INR).")
            return data            
                
        except Exception as e:
            print("There is a problem in converting prices as per GOC rates.\n", str(e))
            self.logger.log("There is a problem in converting prices as per GOC rates.\n", str(e))
            
    def discountedPrice(self, data):    
       
        try:
            discounted_price = []            
            for x, y in zip(data["Publisher"], data["INR_Price"]):
                if x in ['Osprey', 'Paragon','Amex']:
                    temp_price = y * .6
                elif x in ['CP', 'WBC', 'RBC', 'Rappa']:
                    temp_price = y * .7
                elif x in ['GBD', 'IBBD']:
                    temp_price = y * .65
                else:
                    temp_price = y * .55
                discounted_price.append(temp_price)
            
            data["Discounted_Price"] = discounted_price
                
            print("Discounts are applied on the INR prices.\n")
            self.logger.log("Discounts are applied on the INR prices.")
            return data
                        
        except Exception as e:
            print("There is a problem in updating discount rates.\n", str(e))
            self.logger.log("There is a problem in updating discount rates.\n", str(e))
            
    def priceInTargetCurrency(self, data, usd_rate, cad_rate, aus_rate):
        try:
            data["Discounted_Price"] = pd.to_numeric(data.Discounted_Price, errors = 'coerce')
            data["Discounted_Price"] = round(data["Discounted_Price"], 2)
            
            data["Weight"] = pd.to_numeric(data["Weight"], errors ='coerce')
            data["Weight"] = round(data["Weight"], 1) # Other wise few values starts reflecting like 3.000004 when converted in STRING by below line

            data["USD_Price"] = round((data["Discounted_Price"]/usd_rate),2)
            data["CAD_Price"] = round((data["Discounted_Price"]/cad_rate),2)
            data["AUS_Price"] = round((data["Discounted_Price"]/aus_rate),2)
            #data.to_excel(r"Dclass6C_validate.xlsx", index = None)
            
            data.drop(["Name","Currency", "Price", "Status", "INR_Price", "Discounted_Price"], axis =1, inplace = True)
            print("Prices converted into required currency price.\n")
            self.logger.log("Prices converted into required currency price.")
            return data
        except Exception as e:
            print("There is a problem in converting prices into required currency.\n", str(e))
            self.logger.log("There is a problem in converting prices into required currency.\n", str(e))
            
    def shippingCharge(self):
        try:
            shipping = pd.read_excel(self.shipping_file_path)
            print("Shipping charge file is loaded successfully.\n")
            self.logger.log("Shipping charge file is loaded successfully.")
            return shipping
        
        except Exception as e:
            print("There is a problem in reading Shipping Charge file.\n", str(e))
            self.logger.log("There is a problem in reading Shipping Charge file.\n", str(e))
    
    def combineShippingData(self,data, shipping):
        
        try:
            data = pd.merge(data, shipping, on = 'Weight', how ='left')
            print("Shipping charge file is merged with master dataframe.\n")
            self.logger.log("Shipping charge file is merged with master dataframe.")
            return data
               
        except Exception as e:
            print("There is a problem in merging Shipping file wth master file.\n", str(e))   
            self.logger.log("Shipping charge file is merged with master dataframe successfully.\n")
            
    def calculateNetCostPrice(self,data):

          packing_cost = 1.00          
          try:
              ncp_usd, ncp_cad, ncp_aus = [],[],[]
             
              for i in data.iterrows():
                  if i[1]["Disclaimer"] == "Yes":         ######  >>> df.iterrows() gives index at 0 and rows at 1
                      temp_cost_usd = i[1]["USD_Price"] + i[1]["SC_USD_D"] + packing_cost
                      temp_cost_cad = i[1]["CAD_Price"] + i[1]["SC_CAD_D"] + packing_cost
                      temp_cost_aus = i[1]["AUS_Price"] + i[1]["SC_AUS_D"] + packing_cost
                  else:
                      temp_cost_usd = i[1]["USD_Price"] + i[1]["SC_USD_ND"] + packing_cost
                      temp_cost_cad = i[1]["CAD_Price"] + i[1]["SC_CAD_ND"] + packing_cost
                      temp_cost_aus = i[1]["AUS_Price"] + i[1]["SC_AUS_ND"] + packing_cost
                      
                  ncp_usd.append(temp_cost_usd)
                  ncp_cad.append(temp_cost_cad)
                  ncp_aus.append(temp_cost_aus)
              
              data["NCP_USD"] = ncp_usd
              data["NCP_CAD"] = ncp_cad
              data["NCP_AUS"] = ncp_aus
              
              #data.to_excel(r"Class7C_validate.xlsx", index = None)  
              print("Net cost price is calculated as per currency.\n")
              self.logger.log("Net cost price is calculated as per currency.")
              return data
                      
          except Exception as e:
              print("There is a problem in calculating Net Cost Price.\n", str(e))
              self.logger.log("There is a problem in calculating Net Cost Price.\n", str(e))
              
    
            
    
            
    
            






