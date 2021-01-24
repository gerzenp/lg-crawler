#essential Imports
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import smtplib
import time
import random
import subprocess as sp

#EXTRACT DATE FROM SOUP
def extractDate(objekt):
    datum = ''
    maskeDatum = '\d{2}\.\d{2}\.\d{4}'
    if re.search('\d{2}\.\d{2}\.\d{4}', objekt):
        datum = re.search('\d{2}\.\d{2}\.\d{4}', objekt).group(0)
    if datum:
        return datum
    else:
        return ''

#EXTRACT STATUS FROM SOUP
def extractStatus(status):

    #Formalisierung der Pruef-Masken
    st_cancel   = '\.*ABGESAGT.*'
    st_frei     = '\.*FREI.*'
    st_wait     = '\.*WARTE.*'
    st_low      = '\.*WENIG.*'
    st_run      = '\.*BEGONNEN.*'

    #Check for hit
    if re.search(st_cancel, status.upper()):
        return 'ABGESAGT'
    elif re.search(st_frei, status.upper()):
        return 'FREIE PLÄTZE VORHANDEN'
    elif re.search(st_wait, status.upper()):
        return 'WARTELISTE VERFÜGBAR'
    elif re.search(st_low, status.upper()):
        return 'NUR NOCH WENIGE PLÄTZE VERFÜGBAR'
    elif re.search(st_run, status.upper()):
        return 'LEHRGANG HAT BEGONNEN'
    else:
        return 'UNBEKANNT'


#----------MAIN-BODY----------

#ECTRACTIONS
URL_MASTER = 'https://hessen.dlrg.de/fuer-mitglieder/lehrgaenge/lehrgaenge-im-lv-hessen/alle-lehrgaenge-beim-lv-hessen/'

#Try get soup from master
try:
    response = requests.get(URL_MASTER)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
except:
    print("could not get soup")

#Aufloesen von Soup in einzelne Zeilen
zeilen = soup.find_all('div',{'class': 'row row-striped row-hover screen-xl'})

#Aufloesen der Werte nach Tupeln
for zeile in zeilen:

    #parameter-reset
    status          = ''
    datumStart      = ''
    datumEnde       = ''
    meldeschluss    = ''



    #determine masters for attributs
    name_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-3'})
    status_master = zeile.find_all('div', {'class': 'col-sm-6 col-md-4 col-xl-2'})
    datum_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-datum mb-2'})
    meldeschluss_master = zeile.find_all('div', {'class': 'col-sm-12 col-md-6 col-xl seminar-meldeschluss'})

    #Ermitteln Status es Lehrgangs
    for status_1 in status_master:
        status_2 = status_1.select_one('span')

        if status_2 is not None:
            status = extractStatus(str(status_2))
            break
        else:
            status = 'NULL'

    #Ermitteln von Beginn und Ende des Lehrgangs
    for datum_1 in datum_master:
        datum_2 = datum_1.find_all('span')
        laenge = len(datum_2)-1
        if laenge == 0:
            datumStart = extractDate(str(datum_2[0]))
        elif laenge == 1:
            datumStart  = extractDate(str(datum_2[0]))
            datumEnde   = extractDate(str(datum_2[1]))

    #Ermitteln von Meldeschluss
    for melde_1 in meldeschluss_master:
        melde_2 = melde_1.find_all(text = True)
        i=0
        while meldeschluss == '' and i <= len(melde_2):
            meldeschluss = extractDate(str(melde_2[i]))
            i += 1
    
    #Ermitteln des angebotenen Lehrgangs
    for name_1 in name_master:
        name_2 = name_1.find_all(text = True)

    #print extractions
    print("-----------------------------------------------------------------")
    print("LG-Name:         " + str(name_2[1]))
    print("LG-id:           " + str(name_2[2]))
    print("Beginn:          " + datumStart)
    print("Ende:            " + datumEnde)
    print("LG-Status:       " + status)
    print("Meldeschluss:    " + meldeschluss)

print("done")