import os
import csv
import psutil
import datetime
import time
import keyboard
from colorama import Fore
def sprawdz_proces(nazwa_procesu):
    for proc in psutil.process_iter(['pid', 'name', 'create_time']): # petla przechodzi przez kazdy aktualny proces na PC
        if proc.info['name'] == nazwa_procesu:
            return True, datetime.datetime.now() - datetime.datetime.fromtimestamp(proc.info['create_time']) # zwraca istnienie procesu oraz czas dzialania od wlaczenia
    return False, None


def zapisz_czas_do_pliku(nazwa_aplikacji, czas, nazwa_pliku):
    if not os.path.isfile("UserLogs/"+nazwa_pliku):
        with open('UserLogs/'+nazwa_pliku, 'w', newline='') as newfile:
            writer = csv.writer(newfile)
            for process in lista_procesow:
                writer.writerow([process, "0", "0"])

    # TODO If new licence added during use, add to the lista_procesow.csv list

    with open('UserLogs/'+nazwa_pliku, 'r') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        podział = line.strip().split(",") #rozdzielamy kolejno nazwe procesu [0]; ilosc wlaczen [1]; suma czasu uzywania [2]
        if podział[0] == nazwa_aplikacji:
            podział[1] = str(int(podział[1]) + 1)
            podział[2] = str(float(podział[2])+czas)
            lines[index] = ",".join(podział) + '\n' # zlaczenie do zapisu oryginalnego

    with open('UserLogs/'+nazwa_pliku, 'w') as file: #aktualizacja pliku
        file.writelines(lines)


def wczytaj_czasy_z_pliku(nazwa_pliku):
    try:
        with open('UserLogs/'+nazwa_pliku, 'r') as file:
            czasy = [line.strip().split(",")[2] for line in file.readlines()]
            return czasy
    except FileNotFoundError:
        return []


if __name__ == "__main__":

    if not os.path.isdir('UserLogs'):
        os.mkdir('UserLogs')

    # TODO create user config for license
    # if not os.path.isfile("config.csv"):
    #     create config.csv
    with open("lista_procesow.csv", 'r') as csvfile:
        lista_procesow = [line.strip().split("\n")[0] for line in csvfile.readlines()]         # Pobieramy aplikacje nas interesujace, za pomoca pliku csv

    print(lista_procesow)
    for process in lista_procesow:
        pozycja = lista_procesow.index(process)
        running_apps = [False for i in range(len(lista_procesow))]
        past_apps = [False for i in range(len(lista_procesow))]
        current_runtime = [0 for i in range(len(lista_procesow))]
        past_time = [0 for i in range(len(lista_procesow))]
        running_apps[pozycja], current_runtime[pozycja] = sprawdz_proces(process)

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = str(today_date) + "__USERNAMEAppUsage.csv"

    while(True):

        for process in lista_procesow:
            process_index = lista_procesow.index(process)

            if running_apps[process_index]:
                print(Fore.GREEN + "Proces [" + process + "] działa" + Fore.RESET)
                past_apps[process_index] = True

            else:
                if past_apps[process_index]: #jesli nie ma programu a byl wlaczony, wykonaj zapis
                    past_apps[process_index] = False
                    zapisz_czas_do_pliku(process, past_time[process_index].total_seconds(), file_name)
                    print(Fore.CYAN + "Wykryto zakonczenie programu " + process + ". Zapisano do ' " + file_name + " '" + Fore.RESET)

                else:
                    print(Fore.RED + "Proces [" + process + "] nie działa" + Fore.RESET)

            past_apps[process_index] = running_apps[process_index]
            past_time[process_index] = current_runtime[process_index]
            running_apps[process_index], current_runtime[process_index] = sprawdz_proces(process)

            if keyboard.is_pressed("space"):
                for process_final in lista_procesow:
                    process_index_final = lista_procesow.index(process_final)
                    if running_apps[process_index_final]:
                        zapisz_czas_do_pliku(process_final, past_time[process_index_final].total_seconds(), file_name)
                        print(Fore.CYAN + "Wykryto zakonczenie programu " + process_final + ". Zapisano do ' " + file_name + " '" + Fore.RESET)
                print("Stopping application")
                exit(0)
        time.sleep(1)
        print()