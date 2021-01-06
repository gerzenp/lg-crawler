#benötigte Packete
import time
import requests
from bs4 import BeautifulSoup
import telegram_send
import sys
import re
import datetime
import csv

#Wird benötigt beim ersten mal um Telegram zu konfigurieren, danach kann die Zeile 8 ausgeklammert werden.
#telegram_send.configure(conf=(), channel=False, group=True, fm_integration=False)

try: #Try zur Fehlerbehebung; Nachricht dient zur Information im Chat

    Nachricht = ['Hallo Tarik und Jonathan, \n ich habe folgende Lergänge für euch gefunden:', 'Hallo Tarik und Jonathan, \n Leider gab es seit 24 Stunden keine neuen Lehrgänge, aber ich halte euch weiter auf dem Laufenden. Habt einen schönen Tag. \n Euer Rasperry Pi','ACHTTUNG FOLGENDE SEITE ENTHÄLLT 50 LEHRGÄNGE', 'Hallo Tarik und Jonathan \n ich habe gerade ein großes Update erhalten. Zum einen kann ich jetzt CSV-Dateien lesen und schreiben. Ich überprüfe nun auch die Seiten vom LV Bayer und ich habe noch ein mögliches Problem geschlossen. Sollten jemals 50 Lehrgänge auf einer Seite sein, werde ich euch informieren :). \n Achtung es folgt gleich ein SPAM \n Euer Rasperry Pi']
    y =[] #Y enthält alle Lehrgänge aus einem Durchgang
    x = [] #x enthält alle Lehrgänge und vergleicht diese
    Ergebnis = [] #Ergebnis enthält alle neuen Lehrgänge
    Delete = [] #Delete enthält alle bereits gelöschten Lehrgänge
    Erstenachricht = 0 #Zur Ermittlung, ob in einer Vorschleife bereits eine Nachricht verschickt wurde, andernfalls wird eine Begrüßung verschickt.
    Letztenachricht = 0 #Letztenachricht, dient zur Ermittlung, ob innerhalb der letzen 24 Stunden eine Nachricht verschickt wird und zur Absicherung, dass der Bot noch aktiv ist.
    SendeNachricht = [] #Aufgrund von Telegram Bot begrenzungen, können nur 20 Nachrichten pro Minute verschickt werden, diese Liste hält die Nachrichten entsprechend zurück
    Counter = 0 #Counter für die 20 Nachrichten pro minuten Schleife
    Listlänge = 0 #Counter für die 20 Nachrichten pro minuten Schleife
    Bracketremove = []
    #Liste Urlalt, entählt alle Lehrgangseiten mit dem alten 2013er DLRG Design
    Urlalt =  []
    Urlneu = []

    SendeNachricht.append(Nachricht[3])
    with open('Lehrgangsliste.csv', 'r') as Lehrgang_liste:
        for line in Lehrgang_liste:
            Bracketremove.append(line.split(';'))
        if len(Bracketremove) > 0:
            x = Bracketremove[0]
            Bracketremove.clear()
            for i in range(len(x)):
                Textremove = x[i]
                Textremove= Textremove.replace('\\n', '\n')
                x[i]=Textremove
        else:
            x = []

    with open('URLalt.csv', 'r') as URL_ALT:
        for line in URL_ALT:
            Bracketremove.append(line.split(';'))
        if len(Bracketremove) > 0:
            Urlalt = Bracketremove[0]
            Bracketremove.clear()
        else:
            Urlalt = []


    with open('URLneu.csv', 'r') as URL_NEU:
        for line in URL_NEU:
            Bracketremove.append(line.split(';'))
        if len(Bracketremove) > 0:
            Urlneu = Bracketremove[0]
            Bracketremove.clear()
        else:
            Urlneu = []

    while True: #Dauerschleife
        for i in range(len(x)):
            Textremove = x[i]
            Textremove= Textremove.replace('\\n', '\n')
            x[i]=Textremove
        try:
            for i in range(len(Urlalt)): #Abfrage aller URLs aus dem alten Design
                URLNummer = i
            #Ermitteln des HTML-COdes
                r = requests.get(Urlalt[i])
                soup = BeautifulSoup(r.text, 'html.parser')
                absetze = soup.find_all('td', class_="bg_lightgrey")
            #Definition für Übergangsvariablen, zum ermitteln der einzelnen Seiten
                Ergebnis1 = [] # Enthält alle neun Lehrgänge
                y1 = [] #Enthält zu Vergleichenden Text
            #Erittlung des Textes im HTML Code
                for absatz in absetze:
                    y1.append(absatz.text)

                if y1 == 100:
                    SendeNachricht.append(Nachricht[2])
                    SendeNachricht.append(Urlalt[URLNummer])
            #Vergleichen des Textes mit X und ggf. hinzufügen zum Ergebnis
                for i in y1:
                    if i in x:
                        ''
                    else:
                        Ergebnis1.append(i)
            #Liste aller neuen Lehrgänge erweitern
                for i in range(len(y1)):
                    y.append(y1[i])
            #Schreiben von allen neuen Lehrgängen in X
                for i in range(len(Ergebnis1)):
                    x.append(Ergebnis1[i])
                    Ergebnis.append(Ergebnis1[i])
            #Überprüfung ob es neue Lehrgänge im Ergebnis gibt
            if len(Ergebnis1) > 0:
                Erstenachricht = Erstenachricht + 1
            #Wenn es neue Lehrgänge gibt und es die erste Nachricht ist, wird eine Begrüßungsnachricht verschickt
            if Erstenachricht == 1 and len(Ergebnis1) >0:
                SendeNachricht.append(Nachricht[0])
                SendeNachricht.append(Urlalt[URLNummer])
                #Schreiben aller Ergebnisse in Sende Nachricht
                for i in range(len(Ergebnis1)):
                    SendeNachricht.append(Ergebnis1[i])
                #Wenn bereits eine Nachrichte verschickt wurde, wird nur der Link und die neuen Lehrgänge verschickt
            elif Erstenachricht > 1 and len(Ergebnis1) >0:
                SendeNachricht.append(Urlalt[URLNummer])
                for i in range(len(Ergebnis1)):
                    SendeNachricht.append(Ergebnis1[i])
            else:
                ''





        for i in range(len(Urlneu)): #Abfrage aller URLs aus dem alten Design
            URLNummer = i
            #Ermitteln des HTML-COdes
            r = requests.get(Urlneu[i])
            soup = BeautifulSoup(r.text, 'html.parser')
            absetze = soup.find_all('div', class_="row row-striped row-hover screen-xl even bg_lightgrey")
            #Definition für Übergangsvariablen, zum ermitteln der einzelnen Seiten
            Ergebnis1 = [] # Enthält alle neun Lehrgänge
            y1 = [] #Enthält zu Vergleichenden Text
            #Erittlung des Textes im HTML Code
            for absatz in absetze:
                y1.append(absatz.text)
            absetze = soup.find_all('div', class_="row row-striped row-hover screen-xl even bg_lightgrey")
            for absatz in absetze:
                y1.append(absatz.text)

            if y1 == 50:
                SendeNachricht.append(Nachricht[2])
                SendeNachricht.append(Urlneu[URLNummer])
            #Vergleichen des Textes mit X und ggf. hinzufügen zum Ergebnis
            for i in y1:
                if i in x:
                    ''
                else:
                    Ergebnis1.append(i)
            #Liste aller neuen Lehrgänge erweitern
            for i in range(len(y1)):
                y.append(y1[i])
            #Schreiben von allen neuen Lehrgängen in X
            for i in range(len(Ergebnis1)):
                x.append(Ergebnis1[i])
                Ergebnis.append(Ergebnis1[i])
            #Überprüfung ob es neue Lehrgänge im Ergebnis gibt
            if len(Ergebnis1) > 0:
                Erstenachricht = Erstenachricht + 1
            #Wenn es neue Lehrgänge gibt und es die erste Nachricht ist, wird eine Begrüßungsnachricht verschickt
            if Erstenachricht == 1 and len(Ergebnis1) >0:
                SendeNachricht.append(Nachricht[0])
                SendeNachricht.append(Urlneu[URLNummer])
                #Schreiben aller Ergebnisse in Sende Nachricht
                for i in range(len(Ergebnis1)):
                    SendeNachricht.append(Ergebnis1[i])
                #Wenn bereits eine Nachrichte verschickt wurde, wird nur der Link und die neuen Lehrgänge verschickt
            elif Erstenachricht > 1 and len(Ergebnis1) >0:
                SendeNachricht.append(Urlneu[URLNummer])
                for i in range(len(Ergebnis1)):
                    SendeNachricht.append(Ergebnis1[i])
            else:
                ''

        #Wegen eines Bugs des Telegram Packages muss die Sende Nachricht noch um '' verlängert werden
        SendeNachricht.append('')
        #Nur 20 Nachrichten pro Minute, um nicht in den nicht auffangbaren Fehler zu laufen
        for Listlänge in range(len(SendeNachricht)):
            if Counter <= 17:
                telegram_send.send(messages=SendeNachricht[Listlänge:Listlänge+1])
                Counter += 1
            else:
                telegram_send.send(messages=SendeNachricht[Listlänge:Listlänge+1])
                time.sleep(60)
                Counter = 0


        if len(SendeNachricht) > 0:
            print(datetime.datetime.now(), 'folgende Nachrichten wurden verschickt:', SendeNachricht)


        #Sende Nachricht wieder clearen
        SendeNachricht.clear()
        #s = input('Geben Sie etwas ein: ')
        #if s == 'ende':
        #    break
        #Überprüfung wann die letze Nachricht kam


        if Erstenachricht > 0:
            Letztenachricht = 0
            Erstenachricht = 0
        else:
            Letztenachricht += 1
            Erstenachricht = 0


        #Wenn letzte Nachricht den 24 Stunden Grenze erreicht hat, neue Nachricht verschicken.
        if Letztenachricht == 5:
            telegram_send.send(messages=Nachricht[1:2])
            print('Ich bin noch aktiv')
            Letztenachricht = 0
            print(datetime.datetime.now(), 'Nachricht nach 24 Stunden verschickt')
        #Einfach Konsole Information
        if len(Ergebnis) > 0:
            print(datetime.datetime.now(),'Folgende Ergebnisse wurden gefunden:', Ergebnis)
        else:
            print(datetime.datetime.now(), "Keine neuen Lehrgänge")
        #Aufräumen von der X Liste
        for i in range(len(x)):
            if x[i] in y:
                ''
            else:
                Delete.append(x[i])



        #Alle Werte aus X und Delete löschen, die nicht mehr in Y sind
        if len(Delete) > 0:
            print(datetime.datetime.now(),'Folgende Werte werden aus X entfernt', Delete)
            for i in range(len(Delete)):
                x.remove(Delete[i])
            print(datetime.datetime.now(), 'Alle nicht vorhandenen Werte aus X entfernt')
        else:
            print(datetime.datetime.now(), "keine Werte zu löschen")


        with open('Lehrgangsliste.csv', mode='w') as Lehrgang_liste:
            for i in range(len(x)):
                Textremove = x[i]
                Textremove = Textremove.replace('\n', '\\n')
                x[i] = Textremove
            CSV_writer = csv.writer(Lehrgang_liste, delimiter=';')
            CSV_writer.writerow(x)


        #Die restlichen Variablen noch aufräumen
        Delete.clear()
        Ergebnis.clear()
        y.clear()
        print(datetime.datetime.now(), 'Befinde mich im Sleep')
        time.sleep(5)


#Fehlerabfang
except BaseException as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein Fehler aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetreten', err)
    time.sleep(3600)
    pass
except ArithmeticError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein Arithmetic Error aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except BufferError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein BufferError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except LookupError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein LookupError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except AssertionError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein AssertionError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except AttributeError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein AttributeError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except EOFError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein EOFError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except FloatingPointError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein FloatingPointError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except GeneratorExit as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein GeneratorExit aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ImportError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ImportError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ModuleNotFoundError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ModuleNotFoundError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except IndexError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein IndexError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except KeyError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein KeyError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except KeyboardInterrupt as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein KeyboarInterrupt aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except MemoryError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein MemoryError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except NameError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein NameError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except NotImplementedError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein NotImplementedError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except OSError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein OSError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except OverflowError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein OverflowError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except RecursionError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein RecoursionError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ReferenceError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ReferenceError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except RuntimeError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein RunttimeError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except StopIteration as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein StopIteration aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except StopAsyncIteration as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein StopyAsyncIteration aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except SyntaxError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein SyntaxError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    sys.exit(0)
except IndentationError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein IndentationError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    sys.exit(0)
except TabError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein TabError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except SystemError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein SystemError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except SystemExit as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein SystemExit aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    sys.exit(0)
except TypeError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein TypeError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except UnboundLocalError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein UnboundLocalError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except UnicodeError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein UnicodeError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except UnicodeEncodeError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein UnicodeEndcoddeError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except UnicodeDecodeError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein UnicodeDecodeError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except UnicodeTranslateError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein UnicodeTranslateError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ValueError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ValueError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ZeroDivisionError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ZeroDivisionError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except EnvironmentError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein EnvirontmentError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except IOError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein IOError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except WindowsError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein WindowsError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except BlockingIOError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein BlockingIOError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ChildProcessError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ChildProcessError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ConnectionError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ConnectionError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except BrokenPipeError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein BrokenPipeError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ConnectionAbortedError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ConnectionAbortedError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ConnectionRefusedError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ConnectionRefusedError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ConnectionResetError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ConnectionResetError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except FileExistsError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein FileExistsError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except InterruptedError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein InterruptedError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except IsADirectoryError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ISADirectoryError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except NotADirectoryError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein NotADirectoryError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except PermissionError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein PermissionError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except ProcessLookupError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein ProcessLookupError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except TimeoutError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein TimeoutError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except LookupError as err:
    Fehler = [err, '']
    telegram_send.send(messages='Es ist ein LookupError aufgetreten:')
    telegram_send.send(messages=Fehler[0:1])
    print('Es ist ein Fehler aufgetereten', err)
    time.sleep(3600)
    pass
except:
    time.sleep(60)
    telegram_send.send(messages='Es ist ein undefinierter Fehler aufgetreten:')
    print('Es ist ein Fehler aufgetereten')
    time.sleep(3600)
    pass


