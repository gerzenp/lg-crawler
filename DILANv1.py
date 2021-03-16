#essential Imports
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import smtplib
import time
import random
import subprocess as sp
import psycopg2
import psycopg2.extras
from getpass import getpass

#-entfernen von im isc nicht mehr vorhandener Lehrgänge aus Datenbank
def removeLG(DB):
    #verbinden zu Datenbank
    try:
        conn = psycopg2.connect(dbname=DB[1], user=DB[2], password=DB[3], host=DB[0])
    except:
        print("Verbindung zu Datenbank konnte nicht hergestellt werden")
        exit()

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM lgstand WHERE control = 0")
    conn.commit()
    cur.close()
    conn.close()

#-setzen von control in lgstand auf 0
def resetControl(DB):
    #verbinden zu Datenbank
    try:
        conn = psycopg2.connect(dbname=DB[1], user=DB[2], password=DB[3], host=DB[0])
    except:
        print("Verbindung zu Datenbank konnte nicht hergestellt werden")
        exit()

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("UPDATE lgstand SET control = 0")
    conn.commit()
    cur.close()
    conn.close()

#-prüfen welche mails verschickt werden müssen
def checkMail(DB, MAIL):
    #verbinden zu Datenbank
    try:
        conn = psycopg2.connect(dbname=DB[1], user=DB[2], password=DB[3], host=DB[0])
    except:
        print("Verbindung zu Datenbank konnte nicht hergestellt werden")
        exit()

    #abfragen aller Werte !=0
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT a.name, a.start, a.ende, a.meldeschluss, a.status, b.bezeichnung FROM lgstand a INNER JOIN gliederung b on a.gliederung = b.gid WHERE a.control = 2")
    new = cur.fetchall()
    cur.close()
    conn.close()

    #versenden von mail je aktualisiertem Eintrag
    for index in range(len(new)):
        name = new[index][0]
        status = new[index][4]
        start = new[index][1]
        ende = new[index][2]
        meldeschluss = new[index][3]
        gliederung = new[index][5]

        deployMail(MAIL, name, status, start, ende, meldeschluss, gliederung)

def deployMail(MAIL, name, status, start, ende, meldeschluss, gliederung):
    
    #acc ermittlen
    position = str(MAIL[0]).find('@')
    acc = str(MAIL[0])[:position]

    #smtp-parameter festlegen
    toAdd = 'dilan@dlrg-frankfurt.de'
    fromAdd = 'DILAN-FFM by ' + str(acc) + ' <' + str(MAIL[0]) + '>'

    subject = '[AUTO] Lehrgang erkannt'

    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject

    body = 'Digitales Lehrgangs-Auswertung und Informations --Tool mit Feststellung!\n\nGliederung:\n' + str(gliederung) + '\n\nKennzeichnung:\n' + str(name) + '\n\nStatus:\n' + str(status) + '\n\nZeitraum:\n' + str(start) + ' bis ' + str(ende) + '\n\nMeldeschluss:\n' + str(meldeschluss)

    s = smtplib.SMTP(MAIL[2],MAIL[3])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(MAIL[0],MAIL[1])
    main = str(header) + '\n\n' + str(body)
    s.sendmail(str(fromAdd), str(toAdd), str(main))
    s.quit()

#-extrahiere datum from soup
def extractDate(objekt):
    datum = ''
    maskeDatum = '\d{2}\.\d{2}\.\d{4}'
    if re.search('\d{2}\.\d{2}\.\d{4}', objekt):
        datum = re.search('\d{2}\.\d{2}\.\d{4}', objekt).group(0)
    if datum:
        return datum
    else:
        return ''

#-extrahiere status from soup
def extractStatus(status):

    #Formalisierung der Pruef-Masken
    st_cancel   = '\.*ABGESAGT.*'
    st_frei     = '\.*FREI.*'
    st_wait     = '\.*WARTE.*'
    st_low      = '\.*WENIG.*'
    st_run      = '\.*BEGONNEN.*'
    st_full     = '\.*AUSGEBUCHT.*'
    st_melde    = '\.*MELDESCH.*'

    #Check for hit
    if re.search(st_cancel, status.upper()):
        return 'abgesagt'
    elif re.search(st_frei, status.upper()):
        return 'freie plaetze vorhanden'
    elif re.search(st_wait, status.upper()):
        return 'Warteliste verfuegbar'
    elif re.search(st_low, status.upper()):
        return 'nur noch wenige Plaetze verfuegbar'
    elif re.search(st_run, status.upper()):
        return 'Lehrgang hat begonnen'
    elif re.search(st_full, status.upper()):
        return 'ausgebucht'
    elif re.search(st_melde, status.upper()):
        return 'Meldeschluss erreicht'
    else:
        return 'unbekennt'

def checkLG(name, DB):
    #get regex from database
    try:
        conn = psycopg2.connect(dbname=DB[1], user=DB[2], password=DB[3], host=DB[0])
    except:
        print('Verbindung zu Datenbank konnte nicht hergestellt werden')
        exit()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT lehrgang, maske FROM regex_vl ORDER BY fachbereich')
    masken=cur.fetchall()
    cur.close()
    conn.close()

    for maske in range (len(masken)):
        #print(masken[maske][1])
        #print(masken[maske][0])
        if re.search(str(masken[maske][1]), str(name)):
            return str(masken[maske][0])  

    return ""

#--loop url
def subMain (URL_MASTER, DB, gliederung):
    #Try get soup from master
    try:
        response = requests.get(URL_MASTER)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
    except:
        print("could not get soup")

    #Aufloesen von Soup in einzelne Zeilen
    zeilen = soup.find_all('div',{'class': 'row row-striped row-hover screen-xl'})

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

        LGid = str(name_2[2])
        LGname = str(name_2[1])       

        #Analysieren angebotenen Lehrgangs
        hit = checkLG(LGname, DB)
        #print(hit)

        #check if detectec lg is in database
        try:
            conn = psycopg2.connect(dbname=DB[1], user=DB[2], password=DB[3], host=DB[0])
        except:
            print('Verbindung zu Datenbank konnte nicht hergestellt werden')
            exit()
        #Abfrage mit NAME, STARTDATUM und ENDDATUM
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM lgstand WHERE name = '" + str(hit) + "' AND start = '" + str(datumStart) + "' AND ende = '" + str(datumEnde) + "' AND gliederung = " + str(gliederung))
        request=cur.fetchall()

        #bei keinem Treffer in Datenbank - Einspielung in Datenbank - control wird mit 2 vermerkt
        if not request and hit != "":
            print("INSERT INTO lgstand VALUES (DEFAULT, '" +str(hit)+ "', '" + str(LGid) + "', '" + str(datumStart) + "', '" + str(datumEnde) + "', '" + str(meldeschluss) + "', '" + str(status) + "', 2, " + str(gliederung) + ")")
            cur.execute("INSERT INTO lgstand VALUES (DEFAULT, '" +str(hit)+ "', '" + str(LGid) + "', '" + str(datumStart) + "', '" + str(datumEnde) + "', '" + str(meldeschluss) + "', '" + str(status) + "', 2, " + str(gliederung) + ")")
            conn.commit()

        #bei  Treffer in Datenbank - control wird mit 1 vermerkt
        elif request and hit != "":
            print("UPDATE lgstand SET control = 1 WHERE name = '" + str(hit) + "' AND start = '" + str(datumStart) + "' AND ende = '" + str(datumEnde) + "'")
            cur.execute("UPDATE lgstand SET control = 1 WHERE name = '" + str(hit) + "' AND start = '" + str(datumStart) + "' AND ende = '" + str(datumEnde) + "'")
            conn.commit()

        cur.close()
        conn.close()

#-----MAIN----loop HESSEN from Database

#--check mail
#acc, pw, smtp, port
MAIL = ["", "", "", ""]
MAIL[0] = input("MAIL_USER: ")
MAIL[1] = getpass()
MAIL[2] = "SMTP.office365.com"
MAIL[3] = 587

try:
    s = smtplib.SMTP(MAIL[2],MAIL[3])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(MAIL[0],MAIL[1])
    s.quit()
    print("[okay] Mail-Server erfolgreich verbunden")
except:
    print("[error] Verbindung zu Mail-Server konnte nicht hergestellt werden")
    exit()

#--check database
DB = ["", "", "", ""]
DB[0] = "h2927408.stratoserver.net"
DB[1] = "DILAN"
DB[2] = input("DB_USER: ")
DB[3] = getpass()

try:
    conn = psycopg2.connect(dbname=DB[1], user=DB[2], password=DB[3], host=DB[0])
    print("[okay] Datenbank erfolgreich verbundne")
except:
    print("[error] Verbindung zu Datenbank konnte nicht hergestellt werden")
    exit()

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#loopen der hinterlegten Gliederungen
cur.execute("SELECT gid FROM gliederung")
gliederungen = cur.fetchall()

for k in range(len(gliederungen)):
    gl = str(gliederungen[k])[1:len(str(gliederungen[k]))-1:1]
    cur.execute("SELECT * FROM URL WHERE gliederung = " + gl)
    url = cur.fetchall()
    
    #aktualisieren Datenbestand auf lgstand
    for i in range (0, len(url)):
        print(url[i][1])
        subMain(url[i][1], DB, gl)

cur.close()
conn.close()

#prüfen, ob Mail versendet werden muss
checkMail(DB, MAIL)

#delete removed entries
removeLG(DB)

#restet parameter für nächsten Durchlauf
resetControl(DB)

print("Durchlauf abgeschlossen")