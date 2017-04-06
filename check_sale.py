import schedule
import time
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
from datetime import datetime

def check_sales():
    sales = pd.read_csv('sales_data.csv')
    sales.drop('Unnamed: 0',axis = 1,inplace = True)
    page = urlopen('http://www.digitalsalesdata.com/diydsd.php?Region=143441')
    page = BeautifulSoup(page,'lxml')
    data = page.find('table').findAll('td')
    sale = []
    chainsmokers= pd.read_csv('chainsmokers_data.csv')
    chainsmokers.drop('Unnamed: 0',axis = 1,inplace = True)
    lala_land = pd.read_csv('lala_data.csv')
    lala_land.drop('Unnamed: 0',axis = 1,inplace = True)
    cs = []
    lala = []
    ed_sale = pd.read_csv('ed.csv')
    ed_sale.drop('Unnamed: 0',axis = 1,inplace = True)
    ed = []
    for i,n in enumerate(data):
        for item in ['1','2','3','4','5','10','15','20','30','40','50','60','70','80','90','100']:
            try:
                if n.text == item:
                    sale.append([datetime.now().strftime('%m/%d/%Y %H:%M'),item,data[i+1].text,data[i+2].text, data[i+3].text])
            except (IndexError):
                pass
        try:
            if n.text == 'Something Just Like This':
                cs.append([datetime.now().strftime('%m/%d/%Y %H:%M'),data[i-2].text,data[i-1].text,n.text,data[i+1].text])
        except (IndexError):
            pass
       
        for item in ['Audition (The Fools Who Dream)','Love Me Now','City of Stars']:
            try:
                if n.text == item:
                    lala.append([datetime.now().strftime('%m/%d/%Y %H:%M'),data[i-2].text,data[i-1].text,n.text,data[i+1].text])
            except (IndexError):
                pass
        try:
            if n.text == 'Ed Sheeran':
                ed.append(([datetime.now().strftime('%m/%d/%Y %H:%M'),data[i-1].text,n.text,data[i+1].text,data[i+2].text]))
        except (IndexError):
            pass
    

    sales = sales.append(pd.DataFrame(sale,columns = ['time','rank','artist','song','sales']))
    sales.to_csv('sales_data.csv')
    chainsmokers = chainsmokers.append(pd.DataFrame(cs,columns = ['time','rank','artist','song','sales']))
    chainsmokers.to_csv('chainsmokers_data.csv')
    lala_land = lala_land.append(pd.DataFrame(lala,columns = ['time','rank','artist','song','sales']))
    lala_land.to_csv('lala_data.csv')
    ed_sale = ed_sale.append(pd.DataFrame(ed, columns = ['time','rank','artist','song','sales']))
    ed_sale.to_csv('ed.csv')
    print (datetime.now())
    print (sales.shape)
    print (chainsmokers.shape)
    print (lala_land.shape)



schedule.every(30).minutes.do(check_sales)
while 1:
    schedule.run_pending()
    time.sleep(1)
