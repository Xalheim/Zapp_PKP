Naszym zadaniem jest wykonanie wtyczki wspólpracującej z agentem glpi, która będzie odpowiedzialna za monitorowanie używanego oprogramowania przez użytkowników.

Wtyczka będzie pobierała informacje od komputera, przekształcała je w formę odpowiadającą formatowi bazy danych, a następnie zapisywała ją.

Po dokonaniu tego, będziemy w stanie wyświetlać informacje o oprogramowaniu w specjalnej zakładce "Utylizacja" która będzie dostępna jako zakładka w agencie.

Oprogramowanie będzie pobierane z agenta GLPI, a następnie przekazywane dla programu na komputerze (aktualnie app w języku python)
Wtyczka będzie umożliwiała wyświetlanie użycia oprogramowania w zależności od wybranego użytkownika, będzie ona wyświetlała listę pobranych aplikacji.

Każde oprogramowanie będzie miało skrócone informacje wyświetlone na liście (np. czas trwania ogólny w miesiącu, ilość włączeń, czy czas użycia jest satysfakcjonujący według ustalonych parametrów), zaś dla dogłębniejszej analizy poszczególnych sesji, jesteśmy w stanie wejść w każdy z procesów pojedyńczo. 

Będzie tam wyświetlona każda sesja oddzielnie specyficznie dla użytkownika oraz procesu, z dokładnymi danymi przechowanymi oraz przenalizowanymi przez wtyczkę.


Aktualnie została wykonana część projektu od strony komputera.
Aplikacja python tymczasowo pobiera aplikacje z pliku csv, zostanie to zamienione na dane przekazane przez wtyczkę w momencie implementacji pierwszej wersji wtyczki.
Aplikacja python jest w stanie pobrać wybrane nazwy procesów, po czym będzie sprawdzała regularnie czy są one w danym momencie włączone lub nie.

W momencie wykrycia pożądanego procesu, jest to notowane oraz przechowywane w trakcie działania. W momencie zakończenia programu python lub wyłączeniu procesu śledzonego, zostaje zapisana informacja do pliku csv, gdzie każda sesja jest oddzielnie przechowywana w każdej linijce, zawierając nazwę, czas startu oraz czas końca.


10.05.2024

Kod Python został poprawiony, by posiadał tylko język angielski.
Został wykonany Roadmap na następne 3 tygodnie, projekt został uzupełniony o brakujące informacje (czas działania, priorytet, skala, osoby działające).
Wykonano schemat bazy danych, który wykorzystamy do stworzenia tabeli w Agencie GLPI.

NOTATKA z ostatniego wykładu [10.05.2024] do wdrożenia + TODO:
~GLPI ma już sporo drzwi

-trzeba wybudować/zainstalować wtyczkę; rozszerzamy oprogramowanie za pomocą wtyczki

-wtyczka zapewnia: separację + kontrolę nad zmianami


~Rzeczy w wtyczce:
-dodanie nowego pola w Bazie Danych

-rozszerzenie graficzne elementów okien tam, gdzie chcemy wprowadzić np. sesje lub dodatkowe informacje, które pomogą zarządzać aplikacją w czasie

-kolekcja/dostarczanie/analiza danych pobieranych z urządzeń w systemie

~1 punkt (po stronie klienta):

-agent + aplikacja; korzystamy z appki do zbierania danych używając agenta do aplikacji do deploy'u (wdrożenia) lub użyć swojej appki do deploying'u (wdrażania)

-dobrze jak będzie obsłużony po stronie wtyczki

~2 punkt (po stronie systemu glpi [inventory] - "druga strona mostu"):

-glpi nie inwentaryzuje, że mając agenta po stronie klienckiej nie dopisze bezpośrednio do Bazy Danych, więc vvv

-wtyczka glpi inventory -> część delivery (zbierająca), nie jest to bezpośrednie pisanie po Bazie Danych

-zastosowanie platformy glpi jest wszelakie - nie każdy jest skoncentrowany na skanowaniu własnych zasobów

~Baza Danych samoczynnie nie rozszerzy się o jedną tabelę, ale sam fakt obsługi/rozszerzenia tej tabeli powinien być zainicjowany/wykonany z poziomu WTYCZKI

TODO:
~SUKCES PROJEKTU osiągniemy, gdy:

-rozszerzymy Bazę Danych lokalnie jednorazowo na aktualnej wersji

-poza dostarczeniem tej zmiany trzeba później tą zmianą zarządzać -> kolejne podbicie wersji, wtedy GLPI przychodzi ze swoim pakietem nie uwzględniając naszej modyfikacji bazowej