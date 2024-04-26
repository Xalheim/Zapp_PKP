import os
import csv
import psutil
import datetime
import time
import keyboard
from colorama import Fore

from LicenseChecker import check_license_types


def check_process_runtime(process_name):
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):  # loop checks every process running
        if proc.info['name'] == process_name:
            return True, datetime.datetime.fromtimestamp(proc.info['create_time'])  # zwraca istnienie procesu oraz czas wlaczenia aplikacjidatetime.datetime.now() -
    return False, None


def zapisz_czas_do_pliku(nazwa_aplikacji, czas, nazwa_pliku):
    with open('AppCounterUserLogs/' + nazwa_pliku, 'r') as file:
        lines = file.readlines()

    with open('AppCounterUserLogs/' + nazwa_pliku, 'w') as file:  # aktualizacja pliku
        file.writelines(lines)
        file.writelines(f"{nazwa_aplikacji},{str(czas)},{str(datetime.datetime.now())}\n")

def wczytaj_czasy_z_pliku(nazwa_pliku):
    try:
        with open('AppCounterUserLogs/'+nazwa_pliku, 'r') as file:
            czasy = [line.strip().split(",")[3] for line in file.readlines()]
            return czasy
    except FileNotFoundError:
        return []


if __name__ == "__main__":

    if not os.path.isdir('AppCounterUserLogs'):
        os.mkdir('AppCounterUserLogs')

    if not os.path.isfile('lista_procesow.csv'):
        print("lista_procesow.csv does not exist, please read processes from Server")
        exit(1)

    with open("lista_procesow.csv", 'r') as csvfile:
        lista_procesow = [line.strip().split(",")[0] for line in csvfile.readlines()]         # Pobieramy aplikacje nas interesujace, za pomoca pliku csv

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = str(today_date) + "__USERNAMEAppUsage.csv"

    if not os.path.isfile("AppCounterUserLogs/"+file_name):     # TODO in the actual app make a timer that reloads lista_procesow periodically
        with open('AppCounterUserLogs/'+file_name, 'w', newline='') as newfile:
            writer = csv.writer(newfile)
            for proces in lista_procesow:
                writer.writerow([proces, "0", "0"])    # Nazwa procesu, typ licencji, ilosc wlaczen, czas aktywnosci

    #check_license_types(file_name)  # Checks if every program has a license type selected, otherwise asks for input TODO lista_procesow.csv per user, so far supports license for one user

    print(lista_procesow)
    for process in lista_procesow:
        pozycja = lista_procesow.index(process)
        running_apps = [False for i in range(len(lista_procesow))]
        past_apps = [False for i in range(len(lista_procesow))]
        current_runtime = [0 for i in range(len(lista_procesow))]
        past_time = [0 for i in range(len(lista_procesow))]
        running_apps[pozycja], current_runtime[pozycja] = check_process_runtime(process)

    while True:

        for process in lista_procesow:
            process_index = lista_procesow.index(process)

            if running_apps[process_index]:
                print(Fore.GREEN + "Proces [" + process + "] działa" + Fore.RESET)
                past_apps[process_index] = True

            else:
                if past_apps[process_index]: #jesli nie ma programu a byl wlaczony, wykonaj zapis
                    past_apps[process_index] = False
                    zapisz_czas_do_pliku(process, past_time[process_index], file_name)
                    print(Fore.CYAN + "Wykryto zakonczenie programu " + process + ". Zapisano do ' " + file_name + " '" + Fore.RESET)

                else:
                    print(Fore.RED + "Proces [" + process + "] nie działa" + Fore.RESET)

            past_apps[process_index] = running_apps[process_index]
            past_time[process_index] = current_runtime[process_index]
            running_apps[process_index], current_runtime[process_index] = check_process_runtime(process)

            if keyboard.is_pressed("space"):    # TODO Make functional app stop (final exec)
                for process_final in lista_procesow:
                    process_index_final = lista_procesow.index(process_final)
                    if running_apps[process_index_final]:
                        zapisz_czas_do_pliku(process_final, past_time[process_index_final], file_name)
                        print(Fore.CYAN + "Wykryto zakonczenie programu " + process_final + ". Zapisano do ' " + file_name + " '" + Fore.RESET)
                print("Stopping application")
                exit(0)
        time.sleep(1)
        print()
