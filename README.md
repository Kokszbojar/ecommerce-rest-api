Instalacja (Unix/macOS):

  python3 -m venv .venv
  
  source .venv/bin/activate
  
  python -m pip install --upgrade pip
  
  python -m pip install -r requirements.txt

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Wszystkie linki są zagnieżdżone za pomocą routera i wyświetlania obiektów przy pomocy hiperlinków pozwalających na drogę w kierunku coraz to cieńszych "gałęzi drzewa"

Nie bawiłem się w ukrywanie linków dla zwykłych lub niezalogowanych użytkowników (można to zrobić tworząc np. swoje własne szablony)

Ale jeśli taki użytkownik spróbuje odczytać takowe dane otrzyma informację iż nie posiada on do nich dostępu

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Główną funkcjonalnością jest składanie zamówienia, która została podzielona na dwa etapy:

  1. Dodawanie poszczególnych produktów do "koszyka"
  2. Wprowadzanie danych personalnych oraz potwierdzenie zamówienia

Po złożeniu zamówienia zostaje wysłana informacja na emaila przypisanego do konta (póki co konta są tworzone przez shella bądź django-admin panel)

Oraz tworzy nam się nowy obiekt "koszyka" jakoby chcielibyśmy zamówić kolejne produkty

Dodam tylko że "koszyk" i zamówienie to jeden i tem sam obiekt przez cały proces składania zamówienia

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Statystyki sprzedaży wymagały sporo pracy ponieważ nie mogłem znaleźć odpowiedniego rozwiązania które finalnie okazało się bardzo proste i skuteczne, a mianowicie

Stworzyłem nowy model "Sales" z 3 polami - 2 daty oraz ilość (wyświetlanych przedmiotów)

Wystarczy podać początkową, końcową datę wraz z godziną i ilość wyświetlanych produktów

W odpowiedzi otrzymujemy prosty słownik z nazwami przedmiotów oraz ilością sprzedanych sztuk w określonym czasie

Ostatnie wyszukanie zapisuje nam się jak po raz kolejny trafimy na ten endpoint

Wykorzystanie powyższego modelu pozwoliło mi zaoszczędzić czas niewielkim kosztem optymalizacji, ponieważ:
  1. Wszystkie widoki wyświetlania oraz wprowadzania danych do modelu są obsługiwane przez domyślne mixins z rest_framework
  2. Automatyczne mapowanie poprzez default router
  3. Zapamiętywanie poprzednich wyszukań w historii

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Wszystkie widoki oraz serializery zostały obudowane w klasy i funkcje wbudowane w django rest framework tak aby oszczędzić na czasie i zachować przejrzystość kodu

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Wysyłanie przypomnienia o płatności za pomocą biblioteki Celery

Ustawienie aplikacji Celery zgodnie ze standardem czyli w tym przypadku - ecommerce/ecommerce/celery.py

Oraz zadań w ecommerce/restapi/tasks.py

Wywoływanie zadań za pomocą silnika rabbitmq

sudo apt-get install rabbitmq-server

Oraz "pracownika"

celery -A ecommerce worker -B

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Jeśli chodzi o zautomatyzowane testy to niestety nie przygotowałem żadnych na ten moment, ale

Bardzo rzetelnie sprawdziłem każdy z endpointów manualnie i nie pozostawiłem miejsca na żaden oczywisty błąd

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

W ustawieniach ecommerce/ecommerce/settings.py dane do backendu mailowego to moje prywatne aby zaoszczędzić czasu przy sprawdzaniu projektu

Sugeruję zainstalować projekt, stworzyć swoje własne konto z prawdziwym mailem i sprawdzić samemu jak działa omówione api

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Jeśli masz jakieś uwagi to proszę swobodnie utworzyć zgłoszenie lub podzielić się nimi ze mną bezpośrednio przez prywatną wiadomość lub maila.
