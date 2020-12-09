#essential Imports
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import smtplib
import time
import random
import subprocess as sp

def check_KatS (zelle):    
    #812M4-Fachdienstausbildung 1 Teil 4
    F1M4_1 = '\.*(T|t)echnik\s?(U|u)nd\s?(S|s)icherheit.*'
    F1M4_2 = '\.*812\s?(M|m)\s?4.*'
    if re.search(F1M4_1,zelle) or re.search(F1M4_2,zelle):
        return '812M4'
        
    #812M5-Fachdienstausbildung 1 Teil 5
    F1M5_1 = '\.*(W|w)asserrettung\s?(I|i)m\s?(K|k)at(S|s).*'
    F1M5_2 = '\.*812\s?(M|m)\s?5.*'
    if re.search(F1M5_1,zelle) or re.search(F1M5_2,zelle):
        return '812M5'
        
    #812M6-Fachdienstausbildung 1 Teil 6
    F1M6_1 = '\.*(G|g)rundlehrgang\s?(H|h)ochwasser.*'
    F1M6_2 = '\.*812\s?(M|m)\s?6.*'
    if re.search(F1M6_1,zelle) or re.search(F1M6_2,zelle):
        return '812M6'
                
    #821-Retten aus Hochwassergefahren
    RH_1 = '\.*(H|h)ochwassergefahren.*'
    RH_2 = '\.*821.*'
    if re.search(RH_1,zelle) or re.search(RH_2,zelle):
        return '821'
        
    #822-Zusatzausbildung Deichsicherung
    DS_1 = '\.*(D|d)eichsicherung.*'
    DS_2 = '\.*822.*'
    if re.search(DS_1,zelle) or re.search(DS_2,zelle):
        return '822'
        
    #823M1-Maschinist Teil 1
    M1_1 = '\.*(M|m)aschinist.*1.*'
    M1_2 = '\.*823\s?(M|m)\s?1.*'
    if re.search(M1_1,zelle) or re.search(M1_2,zelle):
        return '823M1'
        
    #823M2-Maschinist Teil 2
    M2_1 = '\.*(M|m)aschinist.*2.*'
    M2_2 = '\.*823\s?(M|m)\s?2.*'
    if re.search(M2_1,zelle) or re.search(M2_2,zelle):
        return '823M2'
        
    #831M1-Gruppenführer Teil 1
    G1_1 = '\.*(G|g)ruppenführer.*1.*'
    G1_2 = '\.*831\s?(M|m)\s?1.*'
    if re.search(G1_1,zelle) or re.search(G1_2,zelle):
        return '831M1'
        
    #831M2-Gruppenführer Teil 2
    G2_1 = '\.*(G|g)ruppenführer.*2.*'
    G2_2 = '\.*831\s?(M|m)\s?2.*'
    if re.search(G2_1,zelle) or re.search(G2_2,zelle):
        return '831M2'
        
    #831M3-Gruppenführer Teil 3
    G3_1 = '\.*(G|g)ruppenführer.*3.*'
    G3_2 = '\.*831\s?(M|m)\s?3.*'
    if re.search(G3_1,zelle) or re.search(G3_2,zelle):
        return '831M3'
        
    #831M4-Gruppenführer Teil 4
    G4_1 = '\.*(G|g)ruppenführer.*4.*'
    G4_2 = '\.*831\s?(M|m)\s?4.*'
    if re.search(G4_1,zelle) or re.search(G4_2,zelle):
        return '831M4'
        
    #831M5-Gruppenführer Teil 5
    G5_1 = '\.*(G|g)ruppenführer.*5.*'
    G5_2 = '\.*831\s?(M|m)\s?5.*'
    if re.search(G5_1,zelle) or re.search(G5_2,zelle):
        return '831M5'
        
def check_Boot (zelle):        
    #511-Bootsführer A (Binnen)
    BFA_1 = '\.*(B|b)ootsführerschein\s?(A|a).*'
    BFA_2 = '\.*511.*'
    BFA_3 = '\.*(B|b)oot.*A.*'
    if re.search(BFA_1,zelle) or re.search(BFA_2,zelle) or re.search(BFA_3,zelle):
        return '511'
        
def check_IuK (zelle):      
    #715-BOS Sprechfunker (digital)
    BOSD_1 = '\.*(B|b)(O|o)(S|s).*(D|d)(I|i)(G|g)(I|i)(T|t)(A|a)(L|l).*'
    BOSD_2 = '\.*715.*'
    if re.search(BOSD_1,zelle) or re.search(BOSD_2,zelle):
        return '715'
        
def check_SR (zelle):       
    #1011-Strömungsretter Stufe 1
    SR1_1 = '\.*(S|s)trömungsretter\s?1.*'
    SR1_2 = '\.*1011.*'
    SR1_3 = '.*(S|s)\s?(R|r)\s?1.*'
    if re.search(SR1_1,zelle) or re.search(SR1_2,zelle) or re.search(SR1_3,zelle):
        return '1011'
        
def scan_KatS (ls_KatS):
    ls_KatS_tmp = [[0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']],[0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']]]
    URL_KatS = 'https://hessen.dlrg.de/fuer-mitglieder/lehrgaenge/lehrgaenge-im-lv-hessen/katastrophenschutz/'
    
    #error-management
    try:
        response_KatS = requests.get(URL_KatS)
        soup = BeautifulSoup(response_KatS.text, 'html.parser')
    except:
        print("Website not available")
        print("retry in 30 Minutes")
        time.sleep(1800)
        print("retrying ...")
        response_KatS = requests.get(URL_KatS)
        soup = BeautifulSoup(response_KatS.text, 'html.parser')
        
    zeile_master_even = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl even bg_lightgrey'})
    zeile_master_odd = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl odd bg_lightgrey'})
          
    for zeile in zeile_master_even:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
        
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
            
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_KatS(str(name_3))
                if erg:
                    index = getIndex(8, erg)
                    
                    if index >= 0 and index <= 11:
                        ls_KatS_tmp [index] [0] += 1
                        if ls_KatS_tmp [index] [0] == 1:
                            ls_KatS_tmp [index] [1] [0] = status
                            ls_KatS_tmp [index] [2] [0] = datumStart
                            ls_KatS_tmp [index] [3] [0] = datumEnde
                            ls_KatS_tmp [index] [4] [0] = meldeschluss
                        elif ls_KatS_tmp [index] [0] == 2:
                            ls_KatS_tmp [index] [1] [1] = status
                            ls_KatS_tmp [index] [2] [1] = datumStart
                            ls_KatS_tmp [index] [3] [1] = datumEnde
                            ls_KatS_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
        
    for zeile in zeile_master_odd:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
                
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_KatS(str(name_3))
                if erg:
                    index = getIndex(8, erg)
                    
                    if index >= 0 and index <= 11:
                        ls_KatS_tmp [index] [0] += 1
                        if ls_KatS_tmp [index] [0] == 1:
                            ls_KatS_tmp [index] [1] [0] = status
                            ls_KatS_tmp [index] [2] [0] = datumStart
                            ls_KatS_tmp [index] [3] [0] = datumEnde
                            ls_KatS_tmp [index] [4] [0] = meldeschluss
                        elif ls_KatS_tmp [index] [0] == 2:
                            ls_KatS_tmp [index] [1] [1] = status
                            ls_KatS_tmp [index] [2] [1] = datumStart
                            ls_KatS_tmp [index] [3] [1] = datumEnde
                            ls_KatS_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
    
    #fid, index, status, datumStart, datumEnde, meldeschluss
    
    for i in range (len(ls_KatS)):
        if ls_KatS_tmp [i] [0] > ls_KatS [i] [0]:
            for k in range (0, 1+1):
                if ls_KatS_tmp [i][1][k]!= '':
                    report (8, i, ls_KatS_tmp [i][1][k], ls_KatS_tmp [index] [2] [k], ls_KatS_tmp [index] [3] [k], ls_KatS_tmp [index] [4] [k])
                   
    return ls_KatS_tmp

def scan_Boot (ls_Boot):
    ls_Boot_tmp = [[0, ['',''], ['',''], ['',''], ['','']]]
    URL_Boot = 'https://hessen.dlrg.de/fuer-mitglieder/lehrgaenge/lehrgaenge-im-lv-hessen/bootswesen/'
    
    #error-management
    try:
        response_Boot = requests.get(URL_Boot)
        soup = BeautifulSoup(response_Boot.text, 'html.parser')
    except:
        print("Website not available")
        print("retry in 30 Minutes")
        time.sleep(1800)
        print("retrying ...")
        response_Boot = requests.get(URL_Boot)
        soup = BeautifulSoup(response_Boot.text, 'html.parser')

    zeile_master_even = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl even bg_lightgrey'})
    zeile_master_odd = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl odd bg_lightgrey'})
          
    for zeile in zeile_master_even:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
                
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_Boot(str(name_3))
                if erg:
                    index = getIndex(5, erg)
                    
                    if index >= 0 and index <= 0:
                        ls_Boot_tmp [index] [0] += 1
                        if ls_Boot_tmp [index] [0] == 1:
                            ls_Boot_tmp [index] [1] [0] = status
                            ls_Boot_tmp [index] [2] [0] = datumStart
                            ls_Boot_tmp [index] [3] [0] = datumEnde
                            ls_Boot_tmp [index] [4] [0] = meldeschluss
                        elif ls_Boot_tmp [index] [0] == 2:
                            ls_Boot_tmp [index] [1] [1] = status
                            ls_Boot_tmp [index] [2] [1] = datumStart
                            ls_Boot_tmp [index] [3] [1] = datumEnde
                            ls_Boot_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
        
    for zeile in zeile_master_odd:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
                
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_Boot(str(name_3))
                if erg:
                    index = getIndex(5, erg)
                    
                    if index >= 0 and index <= 0:
                        ls_Boot_tmp [index] [0] += 1
                        if ls_Boot_tmp [index] [0] == 1:
                            ls_Boot_tmp [index] [1] [0] = status
                            ls_Boot_tmp [index] [2] [0] = datumStart
                            ls_Boot_tmp [index] [3] [0] = datumEnde
                            ls_Boot_tmp [index] [4] [0] = meldeschluss
                        elif ls_Boot_tmp [index] [0] == 2:
                            ls_Boot_tmp [index] [1] [1] = status
                            ls_Boot_tmp [index] [2] [1] = datumStart
                            ls_Boot_tmp [index] [3] [1] = datumEnde
                            ls_Boot_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
                
    for i in range (len(ls_Boot)):
        if ls_Boot_tmp [i] [0] > ls_Boot [i] [0]:
            for k in range (0, 1+1):
                if ls_Boot_tmp [i][1][k]!= '':
                    report (5, i, ls_Boot_tmp [i][1][k], ls_Boot_tmp [index] [2] [k], ls_Boot_tmp [index] [3] [k], ls_Boot_tmp [index] [4] [k])
                    
    return ls_Boot_tmp

def scan_IuK (ls_IuK):
    ls_IuK_tmp = [[0, ['',''], ['',''], ['',''], ['','']]]
    URL_IuK = 'https://hessen.dlrg.de/fuer-mitglieder/lehrgaenge/lehrgaenge-im-lv-hessen/sprechfunk/iuk/'
    
    #error-management
    try:
        response_IuK = requests.get(URL_IuK)
        soup = BeautifulSoup(response_IuK.text, 'html.parser')
    except:
        print("Website not available")
        print("retry in 30 Minutes")
        time.sleep(1800)
        print("retrying ...")
        response_IuK = requests.get(URL_IuK)
        soup = BeautifulSoup(response_IuK.text, 'html.parser')

    zeile_master_even = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl even bg_lightgrey'})
    zeile_master_odd = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl odd bg_lightgrey'})
          
    for zeile in zeile_master_even:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
                
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_IuK(str(name_3))
                if erg:
                    index = getIndex(7, erg)
                    
                    if index >= 0 and index <= 0:
                        ls_IuK_tmp [index] [0] += 1
                        if ls_IuK_tmp [index] [0] == 1:
                            ls_IuK_tmp [index] [1] [0] = status
                            ls_IuK_tmp [index] [2] [0] = datumStart
                            ls_IuK_tmp [index] [3] [0] = datumEnde
                            ls_IuK_tmp [index] [4] [0] = meldeschluss
                        elif ls_IuK_tmp [index] [0] == 2:
                            ls_IuK_tmp [index] [1] [1] = status
                            ls_IuK_tmp [index] [2] [1] = datumStart
                            ls_IuK_tmp [index] [3] [1] = datumEnde
                            ls_IuK_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
        
    for zeile in zeile_master_odd:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
                
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_IuK(str(name_3))
                if erg:
                    index = getIndex(7, erg)
                    
                    if index >= 0 and index <= 0:
                        ls_IuK_tmp [index] [0] += 1
                        if ls_IuK_tmp [index] [0] == 1:
                            ls_IuK_tmp [index] [1] [0] = status
                            ls_IuK_tmp [index] [2] [0] = datumStart
                            ls_IuK_tmp [index] [3] [0] = datumEnde
                            ls_IuK_tmp [index] [4] [0] = meldeschluss
                        elif ls_IuK_tmp [index] [0] == 2:
                            ls_IuK_tmp [index] [1] [1] = status
                            ls_IuK_tmp [index] [2] [1] = datumStart
                            ls_IuK_tmp [index] [3] [1] = datumEnde
                            ls_IuK_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
                
    for i in range (len(ls_IuK)):
        if ls_IuK_tmp [i] [0] > ls_IuK [i] [0]:
            for k in range (0, 1+1):
                if ls_IuK_tmp [i][1][k]!= '':
                    report (7, i, ls_IuK_tmp [i][1][k], ls_IuK_tmp [index] [2] [k], ls_IuK_tmp [index] [3] [k], ls_IuK_tmp [index] [4] [k])
                    
    return ls_IuK_tmp


def scan_SR (ls_SR):
    ls_SR_tmp = [[0, ['',''], ['',''], ['',''], ['','']]]
    URL_SR = 'https://hessen.dlrg.de/fuer-mitglieder/lehrgaenge/lehrgaenge-im-lv-hessen/stroemungsrettung/'
    
    #error-management
    try:
        response_SR = requests.get(URL_SR)
        soup = BeautifulSoup(response_SR.text, 'html.parser')
    except:
        print("Website not available")
        print("retry in 30 Minutes")
        time.sleep(1800)
        print("retrying ...")
        response_SR = requests.get(URL_SR)
        soup = BeautifulSoup(response_SR.text, 'html.parser')

    zeile_master_even = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl even bg_lightgrey'})
    zeile_master_odd = soup.find_all('div', {'class': 'row row-striped row-hover screen-xl odd bg_lightgrey'})
          
    for zeile in zeile_master_even:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
                
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_SR(str(name_3))
                if erg:
                    index = getIndex(10, erg)
                    
                    if index >= 0 and index <= 0:
                        ls_SR_tmp [index] [0] += 1
                        if ls_SR_tmp [index] [0] == 1:
                            ls_SR_tmp [index] [1] [0] = status
                            ls_SR_tmp [index] [2] [0] = datumStart
                            ls_SR_tmp [index] [3] [0] = datumEnde
                            ls_SR_tmp [index] [4] [0] = meldeschluss
                        elif ls_SR_tmp [index] [0] == 2:
                            ls_SR_tmp [index] [1] [1] = status
                            ls_SR_tmp [index] [2] [1] = datumStart
                            ls_SR_tmp [index] [3] [1] = datumEnde
                            ls_SR_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
        
    for zeile in zeile_master_odd:
        name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
        status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
        datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
        meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})
        
        datumStart = ''
        datumEnde = ''
        meldeschluss = ''
                
        #Ermitteln Status des Lehrgangs
        for status_1 in status_master:
            status_2 = status_1.select_one('span')
            
            if status_2 is not None:
                status = checkStatus(str(status_2))
                
        #Ermitteln von Beginn und Ende
        for datum_1 in datum_master:
            datum_2 = datum_1.find_all('span')     
            laenge = len(datum_2)-1            
            if laenge == 0:
                datumStart = extractDate(str(datum_2[0]))
            elif laenge == 1:
                datumStart = extractDate(str(datum_2[0]))
                datumEnde = extractDate(str(datum_2[1]))
                
        #Ermitteln von Meldeschluss
        for melde_1 in meldeschluss_master:
            melde_2 = melde_1.find_all(text = True)
            i = 0        
            while meldeschluss == '' and i <= len(melde_2):
                meldeschluss = extractDate(str(melde_2[i]))
                i += 1
                
        #Ermittlen des angegebenen Lehrganges
        for name_1 in name_master:
            name_2 = name_1.find_all(text = True)
            
            for name_3 in name_2:
                erg = check_SR(str(name_3))
                if erg:
                    index = getIndex(10, erg)
                    
                    if index >= 0 and index <= 0:
                        ls_SR_tmp [index] [0] += 1
                        if ls_SR_tmp [index] [0] == 1:
                            ls_SR_tmp [index] [1] [0] = status
                            ls_SR_tmp [index] [2] [0] = datumStart
                            ls_SR_tmp [index] [3] [0] = datumEnde
                            ls_SR_tmp [index] [4] [0] = meldeschluss
                        elif ls_SR_tmp [index] [0] == 2:
                            ls_SR_tmp [index] [1] [1] = status
                            ls_SR_tmp [index] [2] [1] = datumStart
                            ls_SR_tmp [index] [3] [1] = datumEnde
                            ls_SR_tmp [index] [4] [1] = meldeschluss
                    
                    del erg
        del status
                
    for i in range (len(ls_SR)):
        if ls_SR_tmp [i] [0] > ls_SR [i] [0]:
            for k in range (0, 1+1):
                if ls_SR_tmp [i][1][k]!= '':
                    report (10, i, ls_SR_tmp [i][1][k], ls_SR_tmp [index] [2] [k], ls_SR_tmp [index] [3] [k], ls_SR_tmp [index] [4] [k])
                    
    return ls_SR_tmp

        
def checkStatus(status):
    c_ab = '\.*ABGESAGT.*'
    c_frei = '\.*FREI.*'
    c_wait = '\.*WARTE.*'
        
    if re.search(c_ab,status.upper()):
        return 'ABGESAGT'
    elif re.search(c_frei,status.upper()):
        return 'FREI'
    elif re.search(c_wait,status.upper()):
        return 'WARTELISTE'
    else:
        return 'UNBEKANNT'

def getIndex (fid, erg):
    #Boot
    if fid == 5:
        if erg == '511':
            return 0
        else:
            return 9999
        
    #IuK
    elif fid == 7:
        if erg == '715':
            return 0
        else:
            return 9999
    
    #KatS
    elif fid == 8:
        if erg == '812M4':
            return 0
        elif erg == '812M5':
            return 1
        elif erg == '812M6':
            return 2
        elif erg == '821':
            return 3
        elif erg == '822':
            return 4
        elif erg == '823M1':
            return 5
        elif erg == '823M2':
            return 6
        elif erg == '831M1':
            return 7
        elif erg == '831M2':
            return 8
        elif erg == '831M3':
            return 9
        elif erg == '831M4':
            return 10
        elif erg == '831M5':
            return 11
        else:
            return 9999
    
    #Strömungsrettung
    elif fid == 10:
        if erg == '1011':
            return 0
        else:
            return 9999
        
def extractDate(objekt):
    datum = ''
    maskeDatum = '\d{2}\.\d{2}\.\d{4}'
    if re.search('\d{2}\.\d{2}\.\d{4}', objekt):
        datum = re.search('\d{2}\.\d{2}\.\d{4}', objekt).group(0)
    if datum:
        return datum
    else:
        return ''
    
def report (fid, index, status, datumStart, datumEnde, meldeschluss):
    #print als log des Report
    print ('report: ' + str(fid) + ' | ' + str(index))
    
    #Boot
    if fid == 5:
        if index == 0:
            deployMail('Fachbereich Boot', '511 - Bootsfuehrerschein A', status, datumStart, datumEnde, meldeschluss)
            
    #IuK
    elif fid == 7:
        if index == 0:
            deployMail('Fachbereich IuK', '715 - BOS-Sprechfunker (DIGITAL)', status, datumStart, datumEnde, meldeschluss)
    
    #KatS
    elif fid == 8:
        if index == 0:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '812M4 - Grundlehrgang Technik und Sicherheit', status, datumStart, datumEnde, meldeschluss)
        elif index == 1:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '812M5 - Grundlehrgang Wasserrettung im KatS', status, datumStart, datumEnde, meldeschluss)
        elif index == 2:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '812M6 - Grundlehrgang Hochwasser', status, datumStart, datumEnde, meldeschluss)
        elif index == 3:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '821 - Retten aus Hochwassergefahren', status, datumStart, datumEnde, meldeschluss)
        elif index == 4:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '822 - Zusatzausbildung Deichsicherung', status, datumStart, datumEnde, meldeschluss)
        elif index == 5:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '823M1 - Maschinist Teil 1', status, datumStart, datumEnde, meldeschluss)
        elif index == 6:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '823M2 - Maschinist Teil 2', status, datumStart, datumEnde, meldeschluss)
        elif index == 7:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '831M1 - Gruppenfuehrer Teil 1', status, datumStart, datumEnde, meldeschluss)
        elif index == 8:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '831M2 - Gruppenfuehrer Teil 2', status, datumStart, datumEnde, meldeschluss)
        elif index == 9:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '831M3 - Gruppenfuehrer Teil 3', status, datumStart, datumEnde, meldeschluss)
        elif index == 10:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '831M4 - Gruppenfuehrer Teil 4', status, datumStart, datumEnde, meldeschluss)
        elif index == 11:
            deployMail('Katastrophenschutz / Oeffentliche Gefahrenabwehr', '831M5 - Gruppenfuehrer Teil 5', status, datumStart, datumEnde, meldeschluss)
            
    #Strömungsrettung
    elif fid == 10:
        if index == 0:
            deployMail('Fachbereich Strömungsrettung', '1011 - Stroemungsretter Stufe 1', status, datumStart, datumEnde, meldeschluss)
            
def deployMail (fbName, lgName, status, datumStart, datumEnde, meldeschluss):
        
    smtpUser = 'lg.info@gmx.net'
    smtpPass = '60636a37777e9a6d76f41b6e55df69c4'
    
    toAdd = 'p-gerzen@t-online.de'
    fromAdd = 'lg.info@gmx.net'
    
    subject = 'Lehrgangs-Hinweis'
    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
    if datumEnde == '':
        body = 'System mit Feststellung!\n\nKennzeichnung:\n' + lgName + '\n\nStatus:\n' + status + '\n\nZeitraum:\n' + datumStart + '\n\nMeldeschluss:\n' + meldeschluss
    else:
        body = 'System mit Feststellung!\n\nKennzeichnung:\n' + lgName + '\n\nStatus:\n' + status + '\n\nZeitraum:\n' + datumStart + ' bis ' + datumEnde + '\n\nMeldeschluss:\n' + meldeschluss
        
    s = smtplib.SMTP('mail.gmx.net',587)
    
    s.ehlo()
    s.starttls()
    s.ehlo()
    
    s.login(smtpUser,smtpPass)
    main = header + '\n\n' + body
    print(str(main))
    s.sendmail(fromAdd, toAdd, main)
    
    s.quit()

#------------------------------------------------------------------------------------------
#[[Anzahl gefundener Lehrgänge], [Status-LG-1, Status-LG-2], [start-1, start-2], [ende-1, ende-2], [meldeschluss-1, meldeschluss-2]], [...]

#ls_KatS = [812M4, 812M5, 812M6, 821, 822, 823M1, 823M2, 831M1, 831M2, 831M3, 831M4, 831M5]
ls_KatS = [[0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']],[0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']], [0, ['',''], ['',''], ['',''], ['','']]]
#ls_Boot = [511]
ls_Boot = [[0, ['',''], ['',''], ['',''], ['','']]]
#ls_IuK = [715]
ls_IuK = [[0, ['',''], ['',''], ['',''], ['','']]]
#ls_SR = [1011]
ls_SR = [[0, ['',''], ['',''], ['',''], ['','']]]
#Variable für Terminal-Leerung nach x Iterationen
count = 0

tmp = sp.call('clear', shell=True)
print('----- LV-Crawler in VERSION 4 ALPAH -----')

while 1:
    ls_Boot = scan_Boot (ls_Boot)
    ls_IuK = scan_IuK (ls_IuK)
    ls_KatS = scan_KatS (ls_KatS)
    ls_SR = scan_SR (ls_SR)

    print(datetime.now())
           
    #waits 10 to 15 Muinits untill next Crawl
    ts = random.randint(600,900)
    time.sleep(ts)
    
    #nach 20 Itterationen erfolgt reste in Terminal
    if count == 20-1:
        tmp = sp.call('clear', shell=True)
        count = 0
        print('----- LV-Crawler in VERSION 4 -----')
        
    count +=1
