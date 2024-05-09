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




