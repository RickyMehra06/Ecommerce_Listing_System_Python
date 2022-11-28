# Python Project - Automate Ecommerce Listing System:


## Softwares and Tools Requirements

1. [VS Code IDE](https://code.visualdtudio.com/)
2. [Mongodb](https://www.mongodb.com/)
3. [Github Account](https://github.com)
4. [Git Cli](https://cli.github.com/)
5. [Microsoft Excel](https://www.microsoft.com//)


##  To create a new environment

conda create -p venv python==3.7 -y


# Problem Statement:
The account manager of the Amazon seller wants to create a bulk listing excel file to be uploaded at the Amazon seller portal. The inventory files in the form of excel/csv are received from the publishers or distributors at a certain time daily. The sample of such files can be referenced at Input_Origin_Raw folder.

Using MS Excel it takes 40-45 minutes to process the each inventory file in order to create the required bulk listing file. Since Amazon charges it's fee on the selling price (SP) it becomes complex to generate the selling price of thousands of the products to achieve the fixed profit amount in MS Excel as each product has its cost price and shipping charges as per their weights & dimensions.

The manager wants to automate the above process using Python in order to save processing time, money and allows user to choose the amount of profit while generating these files for each country region. 


# Solution Provided:

* Gradient descent approach is used to achieve the selling price for the desired amount of profit and the same can be refrenced at stage_04_data_formation.py module.
* Since inventory receiving timing is not same from each stakeholder, this automate Python system gives manager an option to choose one or more files at time of processing.
* Time taken to complete the task is below 8 minutes which was earlier 45 minutes for each file.


## Input Files

* Input_Original_Raw: Raw Excel files are received from the publisher or distributors (frequeny-daily). 
* Input_Master_Data: It has two types of input files given below:
    * Master_File: It contains information like ASIN, Weight, Status, Disclaimer status of the particular ISBN (product).
    * Shipping_Charge File: It contains information for shipping charged for the target countries - USA, Canada and Australia
      for both disclaimer and non-disclaimer products.


##  Output Files:
 Two types of excel files are generated which are required to be uploaded at the Amazon seller portal.

 ### 1. Fillz Listing File:
 * SKU: User defined unique number of the product required to identify whose order has been received.
 * Product-id: It contain ASIN by which particular product is listed at Amazon seller portal.
 * Product-id-type: 
 * Price: Selling price of the product. It is calculated by considering the cost price, packing charge, shipping charge and Amazon fee.
 * Item-condition:
 * Quantity: Quantity of the product to be uploaded at Amazon portal.
 * Add-delete: 'a' is an alias to add a product.
 * Will-ship-internationally: Used to ship internationally from the domestics location.

 ### 2. Automated Price File:
 * SKU: User defined unique number of the product required to identify whose order has been received.
 * Minimum-seller-allowed-price: Minimum price below the buy-box price.
 * Maximum-seller-allowed-price: Maximum price above the buy-box price.
 * Country-code: Two letters country code of the target country.
 * Currency-code: Three letters currency code for the target country.
 * Rule-name: User defined Rule Name given at Amazon portal.
 * Rule-action: 'start' is used to to activate the automate pricing rule as per the given rule name.


