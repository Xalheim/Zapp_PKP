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
1. Sciagnij plik zip 'softplg_wtyczka'
2. Zaloguj sie do serwera
3. rozpakowanie zbioru do katalogu docelowego
	unzip /home/adminer/download/main.zip -d /var/www/html/glpi/plugin
4. weryfikacja czy w katalogu jest rozpakowany zbiór empty-main
	ll /var/www/html/glpi/plugin
5. zmiana uprawnien i członkostw
	sudo chown -R www-data:www-data /var/www/html/glpi/plugin/example-main
	sudo chmod -R 775 empty /var/www/html/glpi/plugin/example-main
6. zmiana nazwy pluginu 
	mv /var/www/html/glpi/plugin/example-main /var/www/html/glpi/plugin/example
7. weryfikacja pojawienia się pluginu w GLPi Wtyczki/Zainstalowane
8. instalacja wtyczki
9. aktywacja wtyczki
