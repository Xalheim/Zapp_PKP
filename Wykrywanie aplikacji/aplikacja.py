import psutil
import datetime
import time


def sprawdz_proces(nazwa_procesu):
    for proc in psutil.process_iter(['pid', 'name', 'create_time']): # petla przechodzi przez kazdy aktualny proces na PC
        if proc.info['name'] == nazwa_procesu:
            return True, datetime.datetime.now() - datetime.datetime.fromtimestamp(proc.info['create_time']) # zwraca istnienie procesu oraz czas dzialania od wlaczenia
    return False, None


def zapisz_czas_do_pliku(nazwa_aplikacji,czas, nazwa_pliku):
    with open(nazwa_pliku, 'r') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        podział = line.strip().split(";") #rozdzielamy kolejno nazwe procesu [0]; ilosc wlaczen [1]; suma czasu uzywania [2]
        if podział[0] == nazwa_aplikacji:
            podział[1] = str(int(podział[1]) + 1)
            podział[2] = str(float(podział[2])+czas)
            lines[index] = ";".join(podział) + '\n' # zlaczenie do zapisu oryginalnego

    with open(nazwa_pliku, 'w') as file: #aktualizacja pliku
        file.writelines(lines)


def wczytaj_czasy_z_pliku(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as file:
            czasy = [line.strip().split(";")[2] for line in file.readlines()]
            return czasy
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    nazwa_szukanego_procesu = "notepad++.exe" # TODO implementacja listy procesow
    czas_poprzedni = 0 # failsafe
    znaleziony, czas_dzialania = sprawdz_proces(nazwa_szukanego_procesu) # bool czy proces istnieje, czas trwania procesu
    szukaj = True
    aktywny = False
    while(szukaj):
        if znaleziony:
            print("Program działa.")
            aktywny = True
        else:
            if aktywny == True: #jesli nie ma programu a byl wlaczony, wykonaj zapis
                szukaj = False
                aktywny = False
                zapisz_czas_do_pliku(nazwa_szukanego_procesu, czas_poprzedni.total_seconds(), "baza_danych.txt")
                print("Zapisano użycie programu")
            else:
                print("Program nie działa.")
        czas_poprzedni = czas_dzialania
        znaleziony, czas_dzialania = sprawdz_proces(nazwa_szukanego_procesu)
        time.sleep(1)
