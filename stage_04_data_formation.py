class requiredPrice:
   
    def __init__(self, logger):
        self.Application_logs = r'Application_logs/'
        self.logger =logger  

    def requiredSellingPrice(self,ncp, sc, fixed_fee, req_profit):
        try:
            sp = []
            profit_col = []
            gift_wrap = 0
            
            for x in ncp:                
                learning_rate = 1.5
                profit = req_profit
                
                while (profit >= req_profit):
                    temp_sp = x*learning_rate        
                    total = temp_sp + sc + gift_wrap                
                    fee = total*.15 + fixed_fee
                    earning = total - fee
                    profit = round((earning-x),2)                
                    #print("\n Index -" + str(enum) +" The current profit of " + str(temp_sp) + " is > ",profit)
                    
                    if profit >= req_profit:
                        learning_rate = learning_rate - 0.0001
                    else:
                        sp.append(round(temp_sp,2))
                        profit_col.append(profit)
                                    
            print("Selling price is calculated for required currency.\n")
            self.logger.log("Selling price is calculated for required currency.")
            return sp, profit_col
        
        except Exception as e:
            print("There is a problem in calculating Required Selling Price.\n", str(e))
            self.logger.log("There is a problem in calculating Required Selling Price.\n", str(e))                       
 
    def minMaxSellingPrice(self,ncp, sc, fixed_fee, min_profit):
        try:
            min_sp = []
            min_profit_col = []
            gift_wrap = 0
            
            for x in ncp:                
                learning_rate = 1.5
                minimum_profit = min_profit
                
                while (minimum_profit >= min_profit):
                    temp_min_sp = x*learning_rate             
                    total = temp_min_sp + sc + gift_wrap                
                    fee = total*.15 + fixed_fee
                    earning = total - fee
                    minimum_profit = round((earning-x),2)                
                    #print("\n Index -" + str(enum) +" The minimum profit of " + str(temp_sp) + " is > ",min_profit)
                    
                    if minimum_profit >= min_profit:
                        learning_rate = learning_rate - 0.0001
                    else:
                        min_sp.append(round(temp_min_sp,2))
                        min_profit_col.append(minimum_profit)                        
            print("Minimum Selling price is calculated.\n")
            self.logger.log("Minimum Selling price is calculated.")
            return min_sp, min_profit_col
            
        except Exception as e:
            print("There is a problem in calculating Minimum Selling Price.\n", str(e))
            self.logger.log("There is a problem in calculating Minimum Selling Price.\n", str(e))

