# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 03:45:18 2020

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 02:11:23 2020

@author: user
"""
        
import requests
import pandas as pd
import datetime as dt
import os
from  pathlib import Path
import pickle
import matplotlib.pyplot as plt
import time as t

date= dt.datetime.today()
Hour = dt.datetime.now().hour

date= dt.datetime.today().strftime("%Y-%m-%d")
weekno = dt.datetime.today().weekday()
if weekno==5:
    print("Saturday")
    date=(dt.datetime.today()- dt.timedelta(1)).strftime("%Y-%m-%d")
if weekno==6:
    print( "sunday")
    date=(dt.datetime.today()- dt.timedelta(2)).strftime("%Y-%m-%d")

params = {
    'symbol': 'BANKNIFTY'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
}

import time
x=True
while x:
    minute= dt.datetime.now().minute
    Time=dt.datetime.now().strftime("%H:%M:%S")
    if (minute in (2 , 15,  30,  45)):
          Ticker=['BANKNIFTY']
          for k in Ticker:
              url="https://www.nseindia.com/api/option-chain-indices" 
              print(k)
              params = {'symbol': k}
              headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}     
              with requests.Session() as req:
                  req.headers.update(headers)
                  response = req.get("https://www.nseindia.com")
                  data1 = req.get(url, params=params).json() 
                  if not  data1:
                      print("empty @ "+ k)
                  else:
                      data=data1["records"]["data"]
                      columns = pd.DataFrame(data[0]).transpose().columns
                      final_data=pd.DataFrame(columns=columns)
                      for i in range(0,len(data)):
                          z=pd.DataFrame(data[i])
                          zz=z.transpose()
                          if(len(zz.index)==3):
                              final_data=final_data.append(zz.loc[[zz.index[2]]]) 
                          elif(len(zz.index)==4):
                              final_data=final_data.append(zz.loc[[zz.index[2]]]) 
                              final_data=final_data.append(zz.loc[[zz.index[3]]])  
                      final_data=final_data.reset_index() 
                      final_data=final_data.rename(columns = {'index':'option_type'})
                      final_data=final_data[(final_data['openInterest']>0)].reset_index(drop=True)
                      spot= int(final_data['underlyingValue'].unique()[0])
                      final_data=final_data[final_data['strikePrice'].between(0.975*spot, 1.025*spot, inclusive=True)]
                      call_put_OI = pd.DataFrame(final_data.groupby("option_type")['openInterest'].agg({sum})).transpose()
                      call_put_OI['time']=Time
                      call_put_OI['Diff']=call_put_OI['PE']-call_put_OI['CE']
                      columns=['CE', 'PE', 'Diff', 'time']
                      if(Path.exists(Path("E:\code and finance\Data\Intraday\BANKNIFTY", date+".xlsx"))):
                           hist=pd.read_excel(Path("E:\code and finance\Data\Intraday\BANKNIFTY", date+".xlsx"),usecols=columns)                
                           hist=hist.append(call_put_OI)
                           hist.to_excel(Path("E:\code and finance\Data\Intraday\BANKNIFTY", date+".xlsx"))
                           plt.plot(hist['time'],hist['Diff'],color='blue', label="Diff" )
                           plt.plot(hist['time'],hist['CE'], color='red', label="CE")
                           plt.plot(hist['time'],hist['PE'], color='green', label="PE")
                           plt.show()
                           print(hist)
                      else:
                           call_put_OI.to_excel(Path("E:\code and finance\Data\Intraday\BANKNIFTY", date+".xlsx")) 

                      t.sleep(60*10)
                      call_put_OI.to_pickle(Path("E:\code and finance\Data\Intraday\BANKNIFTY", date+".pkl") )
    
    Hour = dt.datetime.now().hour
    if((Hour>=9 and Hour<=15) ): 
      x=True
    else:
      x=False 







    