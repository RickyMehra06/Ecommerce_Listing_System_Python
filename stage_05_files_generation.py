from datetime import date
import os
from os import listdir

class createFillzFiles:
    def __init__(self,logger):

        self.Application_logs = r'Application_logs/'
        self.logger =logger                
        self.col_list = ['product-id-type', 
                         'item-condition', 
                         'add-delete',
                         'will-ship-internationally',
                         'country-code_USD', 
                         'currency-code_USD',
                         'country-code_CAD', 
                         'currency-code_CAD',
                         'country-code_AUS', 
                         'currency-code_AUS',
                         'rule-name', 
                         'rule-action', 
                         'expedited-shipping', 
                         'item-note']
        
        self.rule_name = "lowest_0.02"    
        
        self.fillz_col_usd = ['SKU_USD', 'ASIN10', 'Quantity', 'SP_USD','product-id-type',
                              'item-condition','add-delete','will-ship-internationally',
                              'expedited-shipping', 'item-note']        
        self.auto_col_usd = ['SKU_USD', 'Min_SP_USD', 'Max_SP_USD', 'country-code_USD', 
                             'currency-code_USD', 'rule-name', 'rule-action']
        
        
        self.fillz_col_cad = ['SKU_CAD', 'ASIN10', 'Quantity', 'SP_CAD','product-id-type',
                              'item-condition','add-delete','will-ship-internationally',
                              'expedited-shipping', 'item-note']        
        self.auto_col_cad = ['SKU_CAD', 'Min_SP_CAD', 'Max_SP_CAD', 'country-code_CAD', 
                             'currency-code_CAD', 'rule-name', 'rule-action']
        
        
        self.fillz_col_aus = ['SKU_AUS', 'ASIN10', 'Quantity', 'SP_AUS','product-id-type',
                              'item-condition','add-delete','will-ship-internationally',
                              'expedited-shipping', 'item-note']        
        self.auto_col_aus = ['SKU_AUS', 'Min_SP_AUS', 'Max_SP_AUS', 'country-code_AUS', 
                             'currency-code_AUS', 'rule-name', 'rule-action']
        self.Output_Folder = r"Output_Folder/"
                  
    def skuNames(self, data, currency_code):
        try:
            sku = []                      
            for x, y in zip(data["Publisher"], data["ISBN"]):
                temp_sku = str(x) + "-" + str(currency_code) + "-" + str(y)
                sku.append(temp_sku)
            print("SKU created as per the required {} currency.\n" .format(currency_code))
            self.logger.log("SKU created as per the required {} currency." .format(currency_code))
            return sku
        
        except Exception as e:
            print("There is a problem in creating SKU for the {} currency.\n" .format(currency_code), str(e))
            self.logger.log("There is a problem in creating SKU for the {} currency.\n" .format(currency_code), str(e))
            
    def createConstantColumns(self, data):
        
        try:
            list1,list2,list3,list4,list5,list6,list7,list8,list9,list10,list11,list12,list13,list14 = ([] for i in range(14))

            for i in range(len(data)):
                list1.append(1)
                list2.append(11)
                list3.append('a')
                list4.append('n')
                
                list5.append("US") 
                list6.append("USD")
                list7.append("CD") 
                list8.append("CAD")
                list9.append("AU") 
                list10.append("AUD")            
                
                list11.append(self.rule_name)
                list12.append('start')
                
                list13.append("")
                list14.append("")
            return (list1,list2,list3,list4,list5,list6,list7,list8,list9,list10,list11,list12,list13,list14)
        
        except Exception as e:
            print("There is a problem in creating file structure.\n", str(e))
            self.logger.log("There is a problem in creating file structure.\n", str(e))
    
    def outputFolderExistance(self):
        try:  
            if not os.path.isdir(self.Output_Folder):
                os.makedirs(self.Output_Folder)
            else:
                for f in listdir(self.Output_Folder):
                    os.remove(self.Output_Folder+ "/" + f)
        except Exception as e:
            print("There is a problem in Output Folder.\n\n", str(e)) 
            self.logger.log("There is a problem in Output Folder.\n\n", str(e)) 

    def fillzListingAndAutoFiles(self, data, currency_code):
        
        today = date.today()       
        try:
            if currency_code == "USD":
                fillz = data[self.fillz_col_usd]
                fillz = fillz.rename(columns={"SKU_USD": "SKU", "ASIN10" : "product-id", "SP_USD" : "price", "Quantity" : "quantity"})
                fillz = fillz.reindex(columns=['SKU','product-id','product-id-type','price','item-condition','quantity','add-delete','will-ship-internationally','expedited-shipping','item-note'])
                fillz.to_excel(r'Output_Folder/Listiing_USD-'+ str(today)+'.xlsx', index = False)
                
                auto = data[self.auto_col_usd]
                auto = auto.rename(columns={'SKU_USD': 'SKU', 'Min_SP_USD': 'minimum-seller-allowed-price',
                                            'Max_SP_USD':'maximum-seller-allowed-price', 'country-code_USD':'country-code', 
                                            'currency-code_USD':'currency-code'})
                auto.to_excel(r'Output_Folder/Automated_USD-'+ str(today)+'.xlsx', index = False)
                print('USD Fillz and Automated files have been generated successfully.')
                self.logger.log('USD Fillz and Automated files have been generated successfully.')
            
            elif currency_code == "CAD":
                fillz = data[self.fillz_col_cad]
                fillz = fillz.rename(columns={"SKU_CAD": "SKU", "ASIN10" : "product-id", "SP_CAD" : "price", "Quantity" : "quantity"})
                fillz = fillz.reindex(columns=['SKU','product-id','product-id-type','price','item-condition','quantity','add-delete','will-ship-internationally','expedited-shipping','item-note'])
                fillz.to_excel(r'Output_Folder/Listiing_CAD-'+ str(today)+'.xlsx', index = False)
                
                auto = data[self.auto_col_cad]
                auto = auto.rename(columns={'SKU_CAD': 'SKU', 'Min_SP_CAD': 'minimum-seller-allowed-price',
                                            'Max_SP_CAD':'maximum-seller-allowed-price', 'country-code_CAD':'country-code', 
                                            'currency-code_CAD':'currency-code'})
                auto.to_excel(r'Output_Folder/Automated_CAD-'+ str(today)+'.xlsx', index = False)
                print('CAD Fillz and Automated files have been generated successfully')
                self.logger.log('CAD Fillz and Automated files have been generated successfully.')
            else:
                fillz = data[self.fillz_col_aus]
                fillz = fillz.rename(columns={"SKU_AUS": "SKU", "ASIN10" : "product-id", "SP_AUS" : "price", "Quantity" : "quantity"})
                fillz = fillz.reindex(columns=['SKU','product-id','product-id-type','price','item-condition','quantity','add-delete','will-ship-internationally','expedited-shipping','item-note'])
                fillz.to_excel(r'Output_Folder/Listiing_AUS-'+ str(today)+'.xlsx', index = False)
                
                auto = data[self.auto_col_aus]
                auto = auto.rename(columns={'SKU_AUS': 'SKU', 'Min_SP_AUS': 'minimum-seller-allowed-price',
                                            'Max_SP_AUS':'maximum-seller-allowed-price', 'country-code_AUS':'country-code', 
                                            'currency-code_AUS':'currency-code'})
                auto.to_excel(r'Output_Folder/Automated_AUS-'+ str(today)+'.xlsx', index = False)
                print('AUS Fillz and Automated files have been generated successfully')
                self.logger.log('AUS Fillz and Automated files have been generated successfully.')
                
            
        except Exception as e:
            print("There is a problem in creating Fillz and Automated Pricing files.\n", str(e))
            self.logger.log("There is a problem in creating Fillz and Automated Pricing files.\n", str(e))


