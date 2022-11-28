from stage_01_data_ingestion import fileHandling
from stage_02_data_upload import dBOperation
from stage_03_data_transformation import preProcessor
from stage_04_data_formation import requiredPrice
from stage_05_files_generation import createFillzFiles
from app_logs import app_logger

import numpy as np
import pandas as pd
import glob
from datetime import date

import pymongo
import getpass

from flask import Flask, request, jsonify, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

def __getitem__(key):
    return __dict__[key]

@app.route('/fillz_api', methods=['POST'])
def fillz_api():
    data = [x for x in request.form.values()]
    for enum, i in enumerate(data):
        if enum<=8:
            data[enum] = round(float(i),2)
        else:
            data[enum] = str(i)

    print(data)
      
    print("API is successfully executed!!")

    path = r"Input_Original_Raw"
    goodFilesPath = r"Good_Raw/".strip("\u202a")
    masterFilePath = r'Input_Master_Data\Master_File.xlsx'
    noAsinDetailsFilePath = r'No_Asin_File'
    shipping_file_path = r'Input_Master_Data\Shipping_Charge.xlsx'
    Application_logs = r'Application_logs/'
    today = date.today()

    logger = app_logger()
    logger.log_folder()

    filehandling = fileHandling(logger)   
        
    filehandling.validateFileNames(path)
    filehandling.validateMissingValuesInWholeColumn()
    valid_length = fileHandling(logger).validateColumnsLength()
    valid_length

    col_name = valid_length[0]
    no_of_col = valid_length[1]
    fileHandling(logger).validateSchemaNames(col_name, no_of_col)
    #fileHandling(logger).validateSchemaNames(valid_length[0], valid_length[1])
        
    dboperation = dBOperation(logger)
        
    #client = dboperation.dataBaseConnection()
    client = dboperation.dataBaseConnection(data[9], data[10])
    temp_df = dboperation.replaceMissingWithNull()
    dboperation.insertIntoTableGoodData(temp_df,client)
        
        
    preprocess = preProcessor(logger)
        
    df = preprocess.readFilesFromDir()
    df, invalid_df = preprocess.validateMissingValues(df)
    df, invalid_df = preprocess.removeNon13ISBN(df, invalid_df)
    df, invalid_df = preprocess.validateCurrencyCode(df, invalid_df)
    df, invalid_df = preprocess.validatePrice(df, invalid_df)
    df, invalid_df = preprocess.validateQuantity(df, invalid_df)

    df = preprocess.dropQuantityBelowThreshold(df)
    df = preprocess.createQuantityBins(df)
        
    master_df = preprocess.masterAsinFile()
    df = preprocess.combineDataWithMasterFile(df,master_df) 
        
    df = preprocess.currencyConversionAsPerGOC(df)        
    df = preprocess.discountedPrice(df)
    df = preprocess.priceInTargetCurrency(df,data[0], data[1], data[2])
               
    shipping_df = preprocess.shippingCharge()
    df = preprocess.combineShippingData(df, shipping_df)
    df = preprocess.calculateNetCostPrice(df)
        
        
    requiredprice = requiredPrice(logger)
        
    df["SP_USD"]  = requiredprice.requiredSellingPrice(df["NCP_USD"], 3.75, 1.80, data[3])[0]
    df["Pro_USD"] = requiredprice.requiredSellingPrice(df["NCP_USD"], 3.75, 1.80, data[3])[1]
        
    df["SP_CAD"]  = requiredprice.requiredSellingPrice(df["NCP_CAD"], 5.00, 1.00, data[4])[0]
    df["Pro_CAD"] = requiredprice.requiredSellingPrice(df["NCP_CAD"], 5.00, 1.00, data[4])[1]
        
    df["SP_AUS"]  = requiredprice.requiredSellingPrice(df["NCP_AUS"], 7.00, 1.00, data[5])[0]
    df["Pro_AUS"] = requiredprice.requiredSellingPrice(df["NCP_AUS"], 7.00, 1.00, data[5])[1]  
        
        
    df["Min_SP_USD"]  = requiredprice.minMaxSellingPrice(df["NCP_USD"], 3.75, 1.80, data[6])[0]
    df["Max_SP_USD"]  = df["Min_SP_USD"]+10        
    df["Min_Pro_USD"] = requiredprice.minMaxSellingPrice(df["NCP_USD"], 3.75, 1.80, data[6])[1]
        
    df["Min_SP_CAD"]  = requiredprice.minMaxSellingPrice(df["NCP_CAD"], 5.00, 1.00, data[7])[0]
    df["Max_SP_CAD"]  = df["Min_SP_CAD"]+10  
    df["Min_Pro_CAD"] = requiredprice.minMaxSellingPrice(df["NCP_CAD"], 5.00, 1.00, data[7])[1]
        
    df["Min_SP_AUS"]  = requiredprice.minMaxSellingPrice(df["NCP_AUS"], 7.00, 1.00, data[8])[0]
    df["Max_SP_AUS"]  = df["Min_SP_AUS"]+10  
    df["Min_Pro_AUS"] = requiredprice.minMaxSellingPrice(df["NCP_AUS"], 7.00, 1.00, data[8])[1]
       
        
    fillzfiles = createFillzFiles(logger)
        
    df["SKU_USD"] = fillzfiles.skuNames(df, "USD")
    df["SKU_CAD"] = fillzfiles.skuNames(df, "CAD")
    df["SKU_AUS"] = fillzfiles.skuNames(df, "AUS")
    #df.to_excel(r'class9A_validate.xlsx')
        
    constant_df = pd.DataFrame(np.transpose(fillzfiles.createConstantColumns(df)), columns=fillzfiles.col_list)
    df = pd.concat([df, constant_df], axis =1)
    #df.to_excel(r'Class9B_validate.xlsx')
        
    #print(fillzfiles.col_list[0], fillzfiles.col_list[1])
    fillzfiles.outputFolderExistance()
        
    fillzfiles.fillzListingAndAutoFiles(df,"USD")
    fillzfiles.fillzListingAndAutoFiles(df,"CAD")
    fillzfiles.fillzListingAndAutoFiles(df,"AUS")

    return render_template('home.html', output_data = "USD, CAD & AUS files are created!!")        
        
if __name__ =='__main__':
    app.run(debug=True)
   
   
