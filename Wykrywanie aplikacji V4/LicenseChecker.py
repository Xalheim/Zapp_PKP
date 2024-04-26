def check_license_types(file_name):  # Program goes through the current savefile, and checks each license has been assigned
    with open('lista_procesow.csv', 'r') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        podzial = line.strip().split(",")  # rozdzielamy kolejno nazwe procesu [0]; ilosc wlaczen [1]; suma czasu uzywania [2]
        if not (int(podzial[1]) == 1 or int(podzial[1]) == 2):
            license_type = 0
            while license_type == 0:
                podana_licencja = input(
                    f'\nWybierz typ licencji dla aplikacji {podzial[0]}:\n1. Licencja przypisana do użytkownika\n2. Licencja na sesję\n')
                if not podana_licencja.isdigit():
                    print("Wybór z poza zakresu\n")
                elif int(podana_licencja) == 1:
                    license_type = 1
                elif int(podana_licencja) == 2:
                    license_type = 2
                else:
                    print("Wybór z poza zakresu\n")

            if license_type == 1:
                print(f'\nSettings file has been created successfully for {podzial[0]}. License type saved as: 1. Licencja przypisana do użytkownika\n')
            elif license_type == 2:
                print(f'\nSettings file has been created successfully for {podzial[0]}. License type saved as: 2. Licencja na sesję\n')
            podzial[1] = str(license_type)
            lines[index] = ",".join(podzial) + '\n'  # zlaczenie do zapisu oryginalnego

    with open('lista_procesow.csv', 'w') as file:  # aktualizacja pliku
        file.writelines(lines)
