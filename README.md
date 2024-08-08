Naszym zadaniem jest wykonanie wtyczki wspólpracującej z agentem glpi, która będzie odpowiedzialna za monitorowanie używanego oprogramowania przez użytkowników.

Wtyczka będzie pobierała informacje od komputera oraz wysyłała je do agenta.

Po dokonaniu tego, będziemy w stanie wyświetlać informacje o oprogramowaniu w specjalnej zakładce "Utylizacja" która będzie dostępna jako zakładka w agencie.

Oprogramowanie będzie pobierane z agenta GLPI, a następnie przekazywane dla programu na komputerze (aktualnie app w języku python)
Wtyczka będzie umożliwiała wyświetlanie użycia oprogramowania w zależności od wybranego użytkownika, będzie ona wyświetlała listę pobranych aplikacji.

Każde oprogramowanie będzie miało skrócone informacje wyświetlone na liście (np. czas trwania ogólny w miesiącu, ilość włączeń, czy czas użycia jest satysfakcjonujący według ustalonych parametrów), zaś dla dogłębniejszej analizy poszczególnych sesji, jesteśmy w stanie wejść w każdy z procesów pojedyńczo. 

Będzie tam wyświetlona każda sesja oddzielnie specyficznie dla użytkownika oraz procesu, z dokładnymi danymi przechowanymi oraz przenalizowanymi przez wtyczkę.

Aplikacja python jest w stanie pobrać wybrane nazwy procesów, po czym będzie sprawdzała regularnie czy są one w danym momencie włączone lub nie.

W momencie wykrycia pożądanego procesu, jest to notowane oraz przechowywane w trakcie działania. W momencie zakończenia programu python lub wyłączeniu procesu, zostaje zapisana informacja do pliku csv, gdzie każda sesja jest oddzielnie przechowywana w każdej linijce, zawierając nazwę, czas startu oraz czas końca.


  Instrukcja instalacji wtyczki do glpi
1. Sciagnij plik zip 'softplg_wtyczka.zip'
2. Wstawienie zipa na serwer za pomocą Webmina : ->Tools->Upload and Download->Upload to Server - Miejsce docelowe /home/adminer/download
3. Rozpakowanie zbioru do katalogu docelowego - unzip /home/adminer/download/softplg_wtyczka.zip -d /var/www/html/glpi/plugins
5. Weryfikacja czy w katalogu jest rozpakowany zbiór softplg_wtyczka - ll /var/www/html/glpi/plugins
6. Zmiana uprawnien
	sudo chown -R www-data:www-data /var/www/html/glpi/plugins/softplg_wtyczka
	sudo chmod -R 775 /var/www/html/glpi/plugins/softplg_wtyczka
7. zmiana nazwy pluginu 
	mv /var/www/html/glpi/plugin/example-main /var/www/html/glpi/plugin/example
8. Weryfikacja pojawienia się pluginu w GLPi Wtyczki/Zainstalowane
9. Instalacja wtyczki
10. Aktywacja wtyczki
11. Weryfikacja pojawienia się w zakładce Wtyczki
