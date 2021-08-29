import requests
from bs4 import BeautifulSoup
import time
import threading
import numpy as np
import pandas as pd
from pandas import DataFrame

def scraper():
    #Zeggen welke pagina we willen nemen
    url = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions')
    page = BeautifulSoup(url.text, 'html.parser')
    df = pd.DataFrame()
    
    # info ophalen
    items = page.findAll('div',{'class':'sc-1g6z4xm-0 hXyplo'})
    
    for findings in items:
        hashv = findings.find('div', class_='sc-1au2w4e-0 bTgHwk').text
        hashv = hashv.replace('Hash', '')
        tijd = findings.find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
        waardes = findings.find_all('div', class_='sc-1au2w4e-0 fTyXWG')
        btw_waarde = 'a'
        btc_waarde = waardes[0].text
        btc_waarde = btc_waarde.split(')')[1]
        usd_waarde = waardes[1].text
        usd_waarde = usd_waarde.split(')')[1]

        df2 = pd.DataFrame([hashv, tijd, btc_waarde, usd_waarde])
        df2 = df2.transpose()
        df2.columns = ['hash', 'tijd', 'btc_waarde', 'usd_waarde']

        df = df.append(df2)
    
    df = df.sort_values(by='btc_waarde', ascending=False)
    val = df.iloc[0]
    with open("logfile.txt", 'a') as logfile:
        print(val, file=logfile)

    #Check in terminal schrijven
    print("Logfile updated")
    
    #Timer die het elke minuut laat lopen
    time.sleep(60)
    
while True:
    scraper()
