import requests as rq
from tkinter import *
from tkintermapview import TkinterMapView
import math

# Pobieranie współrzędnych dla adresu
def coords_func(address): # funkcja za parametr przyjmuje wprowadzony adres (np. Kaliskiego 17 Warszawa)
    base_url = "https://nominatim.openstreetmap.org/search" # strona OSM na której o adresie wczytywane są współrzędne
    params = {"q": address, "format": "json"}
    headers = {"User-Agent": "my-app/1.0"}
    response = rq.get(base_url, params=params, headers=headers) # pobiera dane na podstawie parametrów
    data = response.json()
    lat = data[0]["lat"]
    long = data[0]["lon"]
    return [float(lat), float(long)] # zwraca długość i szerokość geograficzną

# Klasy reprezentujące żłobki, pracowników i dzieci
zlobki_list=[] # deklaracja listy do zapisu obiektów reprezentowanych przez klasy (działa jak baza danych)
class Nursery:
    def __init__(self, name, location, workers:int=0, children:int=0): # deklaracja cech które musi posiadać klasa, pracownicy i dzieci początkowo 0
        self.name = name
        self.location = location
        self.workers = sum(pracownicy_list) # suma pracowników w danej placówce
        self.children = sum(dzieci_list) # suma dzieci w danej placówce
        self.coordinates = coords_func(location) # współrzędne na podstawie adresu

pracownicy_list=[]
class Worker: # ta sama zasada co wyżej
    def __init__(self, name, surname, location, nursery):
        self.name = name
        self.surname = surname
        self.location = location
        self.nursery = nursery
        self.coordinates = coords_func(location)

dzieci_list=[]
class Child: # ta sama zasada co wyżej
    def __init__(self, name, surname, location, nursery):
        self.name = name
        self.surname = surname
        self.location = location
        self.nursery = nursery
        self.coordinates = coords_func(location)

# ogólna funkcja zawierająca wszystkie okna (zaczyna od pierwszego - logowanie)
def logowanie(event=None):
    haslo=logowanie_entry.get() # pobierz tekst z okna wpisywania
    if haslo=='geoinfa': # wykonuj wszystko tylko jeśli hasło się zgadza

        # okno dotyczące żłobków
        def zlobki():

            def center_widgets_zlobki(event=None): # umieszcza wszystkie widżety na środku okna, zależnie od jefo rozmiaru
                window_width = root_zlobki_all.winfo_width()
                frame_height=root_zlobki.winfo_height()
                root_zlobki.place(x=window_width // 2, y=frame_height/2, anchor='center')

            def pokaz_wszystko_zlobek(): # pokazuje wszystki żłobki wprowadzone do listy
                listbox_zlobki.delete(0, END) # najpierw czyści okienko
                for idx, object in enumerate(zlobki_list):
                    listbox_zlobki.insert(idx, f'Żłobek {object.name}') # a potem wprowadza po kolei elementy z listy

            def dodaj_zlobek(): # obsługuje dodawanie żłobków do listy
                nazwa_zlobka=entry_zlobki_nazwa.get()
                miejsce_zlobka=entry_zlobki_miejsce.get()

                zlobki_list.append(Nursery(name=nazwa_zlobka, location=miejsce_zlobka)) # uzupełnia cechy klasy i dopisuje taki obiekt do listy

                entry_zlobki_nazwa.delete(0, END) # czyści okna wprowadzania
                entry_zlobki_miejsce.delete(0, END)

                pokaz_wszystko_zlobek() # pokazuje wszystkie obiekty listy

            def edytuj_zlobek(): # pozwala na edycję obiektów z listy żłobków
                i=listbox_zlobki.index(ACTIVE) # pobiera indeks zaznaczonego kursorem elementu

                entry_zlobki_nazwa.delete(0, END)
                entry_zlobki_miejsce.delete(0, END)

                entry_zlobki_nazwa.insert(0, zlobki_list[i].name) # wprowadza do okna cechy zaznaczonego obiektu
                entry_zlobki_miejsce.insert(0, zlobki_list[i].location)

                button_zlobki_dodaj_zlobek.config(text='Zapisz zmiany', command=lambda: aktualizuj_zlobek(i)) # zmienia napis na przycisku i używa na nim kolejnej funkcji

            def aktualizuj_zlobek(i): # aktualizuje wybrany wcześniej element na podstawie jego indeksu
                nazwa=entry_zlobki_nazwa.get() # pobiera dane z pól do wprowadzania
                miejsce=entry_zlobki_miejsce.get()

                zlobki_list[i].name=nazwa # zmienia wartości cech obiektu w danej klasie
                zlobki_list[i].location=miejsce

                button_zlobki_dodaj_zlobek.config(text='Dodaj żłobek', command=dodaj_zlobek) # dodaje nowy obiekt (zmieniony)

                entry_zlobki_nazwa.delete(0, END)
                entry_zlobki_miejsce.delete(0, END)

                pokaz_wszystko_zlobek()

            def usun_zlobek(): # usuwa obiekt z listy na podstawie zaznaczonego elementu listy
                i = listbox_zlobki.index(ACTIVE)

                zlobki_list.pop(i)

                pokaz_wszystko_zlobek()

            def pokaz_zlobek(): # pokazuje pełne informacje o zaznaczonym żłobku
                i = listbox_zlobki.index(ACTIVE)

                nazwa=zlobki_list[i].name # poszczególne cechy obiektu do zmiennych
                pracownicy=zlobki_list[i].workers
                dzieci=zlobki_list[i].children
                miejsce=zlobki_list[i].location

                label_zlobki_nazwa_szczegoly_wartosc.config(text=nazwa, bg='pink') # zmiana tekstu w miejscu pokazywania na wartości zmiennych
                label_zlobki_miejsce_szczegoly_wartosc.config(text=miejsce, bg='pink')
                label_zlobki_dzieci_szczegoly_wartosc.config(text=dzieci, bg='pink')
                label_zlobki_pracownicy_szczegoly_wartosc.config(text=pracownicy, bg='pink')

            root_zlobki_all = Toplevel(root_choice) # okienko podrzędne do okienka wyboru
            root_zlobki_all.title('System żłobków')
            szer = 670
            wys = 360
            root_zlobki_all.geometry(f'{szer}x{wys}')
            root_zlobki_all.bind('<Configure>', center_widgets_zlobki) # centruje wszystkie widżety w oknie

            root_zlobki=Frame(root_zlobki_all) # główna ramka okna
            root_zlobki.grid(row=0, column=0)

            ramka_zlobki_start = Frame(root_zlobki) # poszczególne ramki w ramce głównej
            ramka_zlobki_lista = Frame(root_zlobki)
            ramka_zlobki_formularz = Frame(root_zlobki)
            ramka_zlobki_szczegoly = Frame(root_zlobki)

            ramka_zlobki_start.grid(row=0, column=0, columnspan=2) # pozycje ramek
            ramka_zlobki_lista.grid(row=1, column=1)
            ramka_zlobki_formularz.grid(row=1, column=0)
            ramka_zlobki_szczegoly.grid(row=2, column=0, columnspan=2)

            # ---------------------------------------
            # ramka zlobki_start
            # ---------------------------------------
            label_zlobki_lista = Label(ramka_zlobki_start, text='Lista żłobków', font=('Arial', 14, 'bold italic'), fg='green')
            button_pokaz_liste = Button(ramka_zlobki_start, text='Pokaż wszystko', font=('Arial', 9, 'bold'), command=pokaz_wszystko_zlobek) # przycisk wykonujący pokazywanie wszystkiego

            label_zlobki_lista.grid(row=0, column=0, padx=(szer / 2 - label_zlobki_lista.winfo_reqwidth() / 2), pady=(10, 0)) # umieszczenie przycisku na środku
            button_pokaz_liste.grid(row=1, column=0)

            # ---------------------------------------
            # ramka zlobki_lista
            # ---------------------------------------
            listbox_zlobki = Listbox(ramka_zlobki_lista, width=50) # okienko w którym wyświetlają się elementy listy
            button_zlobki_pokaz_szczegoly = Button(ramka_zlobki_lista, text='Pokaż dane żłobka', command=pokaz_zlobek)
            button_zlobki_usun = Button(ramka_zlobki_lista, text='Usuń żłobek', command=usun_zlobek)
            button_zlobki_edytuj = Button(ramka_zlobki_lista, text='Edytuj żłobek', command=edytuj_zlobek)

            listbox_zlobki.grid(row=1, column=0, columnspan=3, pady=(10, 0)) # szerokość 3 kolumn, przesunięcie o 10 pikseli w prawo
            button_zlobki_pokaz_szczegoly.grid(row=2, column=0)
            button_zlobki_usun.grid(row=2, column=1)
            button_zlobki_edytuj.grid(row=2, column=2)

            # ---------------------------------------
            # ramka zlobki_formularz
            # ---------------------------------------
            label_zlobki_nowy_obiekt = Label(ramka_zlobki_formularz, text='Formularz edycji i dodawania:', font=('Arial', 10, 'italic'), bg='yellow')

            label_zlobki_nazwa = Label(ramka_zlobki_formularz, text='Nazwa żłobka')
            label_zlobki_miejsce = Label(ramka_zlobki_formularz, text='Adres żłobka')

            entry_zlobki_nazwa = Entry(ramka_zlobki_formularz) # pola do wprowadzania danych przez użytkownika
            entry_zlobki_miejsce = Entry(ramka_zlobki_formularz)

            label_zlobki_nowy_obiekt.grid(row=0, column=0, columnspan=2)
            label_zlobki_nazwa.grid(row=1, column=0, sticky=W) # przyczepienie do zachodu (W), czyli lewej
            label_zlobki_miejsce.grid(row=2, column=0, sticky=W)

            entry_zlobki_nazwa.grid(row=1, column=1, sticky=W)
            entry_zlobki_miejsce.grid(row=2, column=1, sticky=W)

            button_zlobki_dodaj_zlobek = Button(ramka_zlobki_formularz, text='Dodaj żłobek', font=('Arial', 8, 'bold'), fg='red', command=dodaj_zlobek)
            button_zlobki_dodaj_zlobek.grid(row=3, column=0, columnspan=2)

            # ---------------------------------------
            # ramka zlobki_szczegoly
            # ---------------------------------------
            label_zlobki_opis_obiektu = Label(ramka_zlobki_szczegoly, text='Szczegóły żłobka:', font=('Arial', 10, 'bold'))
            label_zlobki_nazwa_szczegoly = Label(ramka_zlobki_szczegoly, text='Nazwa żłobka', font=('Arial', 10, 'italic'))
            label_zlobki_nazwa_szczegoly_wartosc = Label(ramka_zlobki_szczegoly, text='...', width=20) # te trzy kropki są później zamieniane na poszczególne wartości cech obiektów

            label_zlobki_miejsce_szczegoly = Label(ramka_zlobki_szczegoly, text='Adres żłobka', font=('Arial', 10, 'italic'))
            label_zlobki_miejsce_szczegoly_wartosc = Label(ramka_zlobki_szczegoly, text='...', width=20)

            label_zlobki_dzieci_szczegoly = Label(ramka_zlobki_szczegoly, text='Liczba podopiecznych', font=('Arial', 10, 'italic'))
            label_zlobki_dzieci_szczegoly_wartosc = Label(ramka_zlobki_szczegoly, text='...', width=20)

            label_zlobki_pracownicy_szczegoly = Label(ramka_zlobki_szczegoly, text='Liczba pracowników', font=('Arial', 10, 'italic'))
            label_zlobki_pracownicy_szczegoly_wartosc = Label(ramka_zlobki_szczegoly, text='...', width=20)

            label_zlobki_opis_obiektu.grid(row=0, column=0, columnspan=8, pady=10)

            label_zlobki_nazwa_szczegoly.grid(row=1, column=0)
            label_zlobki_nazwa_szczegoly_wartosc.grid(row=2, column=0)

            label_zlobki_miejsce_szczegoly.grid(row=1, column=1)
            label_zlobki_miejsce_szczegoly_wartosc.grid(row=2, column=1)

            label_zlobki_dzieci_szczegoly.grid(row=1, column=2)
            label_zlobki_dzieci_szczegoly_wartosc.grid(row=2, column=2)

            label_zlobki_pracownicy_szczegoly.grid(row=1, column=3)
            label_zlobki_pracownicy_szczegoly_wartosc.grid(row=2, column=3)

            root_zlobki_all.mainloop() # całość wykonywana w ciągłej pętli - powoduje że okienko się nie zamyka samo


        # okno dotyczące pracowników
        def pracownicy():

            def center_widgets_pracownicy(event=None): # umieszcza wszystkie widżety na środku okna, zależnie od jefo rozmiaru
                window_width = root_pracownicy_all.winfo_width()
                frame_height=root_pracownicy.winfo_height()
                root_pracownicy.place(x=window_width // 2, y=frame_height/2, anchor='center')

            def pokaz_wszystko_pracownicy(): # pokazuje wszystkich pracowników wprowadzonych do listy
                radiobutton_all.select() # zaznacza przełącznik (radiobutton) dla wszystkich
                listbox_pracownicy.delete(0, END)
                for idx, object in enumerate(pracownicy_list):
                    listbox_pracownicy.insert(idx, f'Pracownik {object.name} {object.surname}') # po kolei pokazuje pracowników

            def pokaz_zaznaczone_pracownicy(): # pokazuje pracowników
                if var.get()==1: # jeśli zaznaczona pierwsza opca
                    pokaz_wszystko_pracownicy() # pokazuje wszystkich
                elif var.get()==2: # jeśli zaznaczona druga opcja
                    zlobek=entry_start_zlobek.get() # odczytuja jacy pracownicy mają być wyświetleni na podstawie żłobka
                    listbox_pracownicy.delete(0, END)
                    for idx, object in enumerate(pracownicy_list):
                        if object.nursery==zlobek: # jeśli cecha obiektu zgadza się z wprowadzoną przez użytkownika
                            listbox_pracownicy.insert(idx, f'Pracownik {object.name} {object.surname}') # to go wyświetla
                        else:
                            pass

            def dodaj_pracownika(): # dodaje pracowników do listy (jak w przypadku żłobków)
                imie=entry_pracownicy_imie.get()
                nazwisko=entry_pracownicy_nazwisko.get()
                zamieszkanie=entry_pracownicy_zamieszkanie.get()
                zlobek=entry_pracownicy_zlobek.get()

                pracownicy_list.append(Worker(name=imie, surname=nazwisko, location=zamieszkanie, nursery=zlobek))

                entry_pracownicy_imie.delete(0, END)
                entry_pracownicy_nazwisko.delete(0, END)
                entry_pracownicy_zamieszkanie.delete(0, END)
                entry_pracownicy_zlobek.delete(0, END)

                pokaz_zaznaczone_pracownicy()

            def edytuj_pracownika(): # edytuje info o pracowniku
                global lista_prac # definiuje globalną listę roboczą
                if var.get()==1: # jesli pierwsza opcja
                    lista_prac=pracownicy_list # to lista bez zmian

                elif var.get()==2: # jeśli druga
                    zlobek=entry_start_zlobek.get()
                    lista_prac=[]
                    do_usuniecia = []
                    for object in pracownicy_list:
                        if object.nursery == zlobek:
                            lista_prac.append(object) # to dopisuje do listy tylko te obiekty które spełniają warunek odnośnie żłobka
                            do_usuniecia.append(object)
                    for obj in do_usuniecia:
                        pracownicy_list.remove(obj) # pozostałe usuwa z listy głównej

                i=listbox_pracownicy.index(ACTIVE)

                entry_pracownicy_imie.delete(0, END) # czyści pola do wprowadzania
                entry_pracownicy_nazwisko.delete(0, END)
                entry_pracownicy_zamieszkanie.delete(0, END)
                entry_pracownicy_zlobek.delete(0, END)

                entry_pracownicy_imie.insert(0, lista_prac[i].name) # wypełnia pola cechami obiektu edytowanego
                entry_pracownicy_nazwisko.insert(0, lista_prac[i].surname)
                entry_pracownicy_zamieszkanie.insert(0, lista_prac[i].location)
                entry_pracownicy_zlobek.insert(0, lista_prac[i].nursery)

                button_pracownicy_dodaj_pracownika.config(text='Zapisz zmiany', command=lambda: aktualizuj_pracownika(i))

            def aktualizuj_pracownika(i):
                global pracownicy_list # przywołuje zadeklarowaną wcześniej listę
                imie=entry_pracownicy_imie.get() # pobiera wartości z pola wpisywania
                nazwisko=entry_pracownicy_nazwisko.get()
                zamieszkanie=entry_pracownicy_zamieszkanie.get()
                zlobek=entry_pracownicy_zlobek.get()

                if var.get() == 1: # jeśli opcja pierwsza
                    lista_prac[i].name=imie # zmienia wartości cech
                    lista_prac[i].surname=nazwisko
                    lista_prac[i].location=zamieszkanie
                    lista_prac[i].nursery=zlobek
                    pracownicy_list=lista_prac # wpisuje normalnie do listy

                elif var.get()==2: # jeśli opcja druga
                    lista_prac[i].name=imie # zmienia wartości cech
                    lista_prac[i].surname=nazwisko
                    lista_prac[i].location=zamieszkanie
                    lista_prac[i].nursery=zlobek
                    for object in lista_prac:
                        pracownicy_list.append(object) # dopisuje liste ze zmienionym obiektem do głównej

                button_pracownicy_dodaj_pracownika.config(text='Dodaj pracownika', command=dodaj_pracownika) # dodaje zmienionego pracownika do listy

                entry_pracownicy_imie.delete(0, END) # czyści pola wprowadzania
                entry_pracownicy_nazwisko.delete(0, END)
                entry_pracownicy_zamieszkanie.delete(0, END)
                entry_pracownicy_zlobek.delete(0, END)

                pokaz_zaznaczone_pracownicy()

            def usun_pracownika(): # usuwa obiekt pracownika z listy
                i = listbox_pracownicy.index(ACTIVE)

                if var.get()==1: # jeśli opcja 1
                    pracownicy_list.pop(i) # usuwa z listy

                elif var.get()==2: # jeśli opcja 2
                    zlobek=entry_start_zlobek.get()
                    removal_list=[]
                    do_usuniecia = []
                    for object in pracownicy_list[:]:
                        if object.nursery == zlobek:
                            removal_list.append(object) # to dopisuje do listy do usunięcia tylko te obiekty które spełniają warunek odnośnie żłobka
                            do_usuniecia.append(object)
                    for obj in do_usuniecia:
                        pracownicy_list.remove(obj)
                    removal_list.pop(i) # usuwa ten obiekt
                    for object in removal_list:
                        pracownicy_list.append(object) # a pozostałe obiekty w liście roboczej dopisuje do głównej

                pokaz_zaznaczone_pracownicy()

            def pokaz_pracownika(): # pokazuje pełne dane o pracowniku
                i = listbox_pracownicy.index(ACTIVE)
                if var.get()==1: # jeśli opcja 1
                    imie=pracownicy_list[i].name # przypisuje informacje o zaznaczonym pracowniku do zmiennej
                    nazwisko=pracownicy_list[i].surname
                    zamieszkanie=pracownicy_list[i].location
                    zlobek=pracownicy_list[i].nursery

                elif var.get()==2: # jeśli opcja 2
                    zlobek=entry_start_zlobek.get()
                    show_list=[]
                    do_usuniecia = []
                    for object in pracownicy_list[:]:
                        if object.nursery == zlobek:
                            show_list.append(object) # to dopisuje do listy do wyświetlenia tylko te obiekty które spełniają warunek odnośnie żłobka
                            do_usuniecia.append(object)
                    for obj in do_usuniecia:
                        pracownicy_list.remove(obj) # usuwa z głównej listy
                    imie=show_list[i].name # i też przypisuje informacje o zaznaczonym pracowniku do zmiennej
                    nazwisko=show_list[i].surname
                    zamieszkanie=show_list[i].location
                    zlobek=show_list[i].nursery

                label_pracownicy_imie_szczegoly_wartosc.config(text=imie) # zamienia tekst na wartości cech pracownika
                label_pracownicy_nazwisko_szczegoly_wartosc.config(text=nazwisko)
                label_pracownicy_zamieszkanie_szczegoly_wartosc.config(text=zamieszkanie)
                label_pracownicy_zlobek_szczegoly_wartosc.config(text=zlobek)

            root_pracownicy_all = Toplevel(root_choice) # okno podrzędne do okna wyboru
            root_pracownicy_all.title('System żłobków')
            szer = 690
            wys = 490
            root_pracownicy_all.geometry(f'{szer}x{wys}')
            root_pracownicy_all.bind('<Configure>', center_widgets_pracownicy) # centruje wszystkie widżety

            root_pracownicy=Frame(root_pracownicy_all) # główna ramka
            root_pracownicy.grid(row=0, column=0)

            ramka_pracownicy_start = Frame(root_pracownicy) # ramki podrzędne
            ramka_pracownicy_lista = Frame(root_pracownicy)
            ramka_pracownicy_formularz = Frame(root_pracownicy)
            ramka_pracownicy_szczegoly = Frame(root_pracownicy)

            ramka_pracownicy_start.grid(row=0, column=0, columnspan=2)
            ramka_pracownicy_lista.grid(row=1, column=1)
            ramka_pracownicy_formularz.grid(row=1, column=0)
            ramka_pracownicy_szczegoly.grid(row=2, column=0, columnspan=2)

            # ---------------------------------------
            # ramka pracownicy_start
            # ---------------------------------------
            label_pracownicy_lista = Label(ramka_pracownicy_start, text='Lista pracowników żłobków', font=('Arial', 12, 'bold'))
            button_pracownicy_pokaz_liste = Button(ramka_pracownicy_start, text='Pokaż wszystko', command=pokaz_wszystko_pracownicy)
            label_pracownicy_wybor = Label(ramka_pracownicy_start, text='Wybierz formułę wyświetlania pracowników')
            var = IntVar() # inicjalizacja radiobuttona, czyli tego przełącznika
            radiobutton_all = Radiobutton(ramka_pracownicy_start, text='Wszyscy pracownicy', variable=var, value=1) # opcja 1 radiobuttona z opisem
            radiobutton_some = Radiobutton(ramka_pracownicy_start, text='Pracownicy z danego żłobka (nazwa)', variable=var, value=2) # opcja 2 radiobuttona z opisem
            entry_start_zlobek = Entry(ramka_pracownicy_start)
            button_pracownicy_pokaz_wybrane = Button(ramka_pracownicy_start, text='Pokaż zaznaczone', command=pokaz_zaznaczone_pracownicy)

            label_pracownicy_lista.grid(row=0, column=0, columnspan=3, padx=(szer / 2 - label_pracownicy_lista.winfo_reqwidth() / 2), pady=(10, 0)) # wycentrowane i lekko przesunięte
            button_pracownicy_pokaz_liste.grid(row=1, column=0, columnspan=3)
            label_pracownicy_wybor.grid(row=2, column=0, pady=(10, 0), columnspan=3)
            radiobutton_all.grid(row=3, column=0, columnspan=3)
            radiobutton_some.grid(row=4, column=0, columnspan=3)
            entry_start_zlobek.grid(row=5, column=0, columnspan=3)
            button_pracownicy_pokaz_wybrane.grid(row=6, column=0, columnspan=3)

            # ---------------------------------------
            # ramka pracownicy_lista
            # ---------------------------------------
            listbox_pracownicy = Listbox(ramka_pracownicy_lista, width=50) # pole do wyświetlania obiektów z listy
            button_pracownicy_pokaz_szczegoly = Button(ramka_pracownicy_lista, text='Pokaż dane pracownika', command=pokaz_pracownika)
            button_pracownicy_usun = Button(ramka_pracownicy_lista, text='Usuń pracownika', command=usun_pracownika)
            button_pracownicy_edytuj = Button(ramka_pracownicy_lista, text='Edytuj pracownika', command=edytuj_pracownika)

            listbox_pracownicy.grid(row=0, column=0, columnspan=3, pady=(10, 0))
            button_pracownicy_pokaz_szczegoly.grid(row=1, column=0)
            button_pracownicy_usun.grid(row=1, column=1)
            button_pracownicy_edytuj.grid(row=1, column=2)

            # ---------------------------------------
            # ramka pracownicy_formularz
            # ---------------------------------------
            label_pracownicy_nowy_obiekt = Label(ramka_pracownicy_formularz, text='Formularz edycji i dodawania:', font=('Arial', 10))
            label_pracownicy_imie = Label(ramka_pracownicy_formularz, text='Imię')
            label_pracownicy_nazwisko = Label(ramka_pracownicy_formularz, text='Nazwisko')
            label_pracownicy_zamieszkanie = Label(ramka_pracownicy_formularz, text='Zamieszkały/a')
            label_pracownicy_zlobek = Label(ramka_pracownicy_formularz, text='Prznależność')

            entry_pracownicy_imie = Entry(ramka_pracownicy_formularz)
            entry_pracownicy_nazwisko = Entry(ramka_pracownicy_formularz)
            entry_pracownicy_zamieszkanie = Entry(ramka_pracownicy_formularz)
            entry_pracownicy_zlobek = Entry(ramka_pracownicy_formularz)

            label_pracownicy_nowy_obiekt.grid(row=0, column=0, columnspan=2)
            label_pracownicy_imie.grid(row=1, column=0, sticky=W)
            label_pracownicy_nazwisko.grid(row=2, column=0, sticky=W)
            label_pracownicy_zamieszkanie.grid(row=3, column=0, sticky=W)
            label_pracownicy_zlobek.grid(row=4, column=0, sticky=W)

            entry_pracownicy_imie.grid(row=1, column=1, sticky=W)
            entry_pracownicy_nazwisko.grid(row=2, column=1, sticky=W)
            entry_pracownicy_zamieszkanie.grid(row=3, column=1, sticky=W)
            entry_pracownicy_zlobek.grid(row=4, column=1, sticky=W)

            button_pracownicy_dodaj_pracownika = Button(ramka_pracownicy_formularz, text='Dodaj pracownika', command=dodaj_pracownika)
            button_pracownicy_dodaj_pracownika.grid(row=6, column=0, columnspan=2)

            # ---------------------------------------
            # ramka pracownicy_szczegoly
            # ---------------------------------------
            label_pracownicy_opis_obiektu = Label(ramka_pracownicy_szczegoly, text='Szczegóły pracowników:', font=('Arial', 10))
            label_pracownicy_imie_szczegoly = Label(ramka_pracownicy_szczegoly, text='Imię')
            label_pracownicy_imie_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text='...', width=20) # trzy kropki będą zmieniane przez cechy danego pracownika

            label_pracownicy_nazwisko_szczegoly = Label(ramka_pracownicy_szczegoly, text='Nazwisko')
            label_pracownicy_nazwisko_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text='...', width=20)

            label_pracownicy_zamieszkanie_szczegoly = Label(ramka_pracownicy_szczegoly, text='Zamieszkały/a')
            label_pracownicy_zamieszkanie_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text='...', width=20)

            label_pracownicy_zlobek_szczegoly = Label(ramka_pracownicy_szczegoly, text='Przynależność')
            label_pracownicy_zlobek_szczegoly_wartosc = Label(ramka_pracownicy_szczegoly, text='...', width=20)

            label_pracownicy_opis_obiektu.grid(row=0, column=0, columnspan=5, pady=10)

            label_pracownicy_imie_szczegoly.grid(row=1, column=0)
            label_pracownicy_imie_szczegoly_wartosc.grid(row=2, column=0)

            label_pracownicy_nazwisko_szczegoly.grid(row=1, column=1)
            label_pracownicy_nazwisko_szczegoly_wartosc.grid(row=2, column=1)

            label_pracownicy_zamieszkanie_szczegoly.grid(row=1, column=2)
            label_pracownicy_zamieszkanie_szczegoly_wartosc.grid(row=2, column=2)

            label_pracownicy_zlobek_szczegoly.grid(row=1, column=3)
            label_pracownicy_zlobek_szczegoly_wartosc.grid(row=2, column=3)

            root_pracownicy.mainloop() # całość w pętli, jak wcześniej
        

        # okno dotyczące dzieci
        def dzieci(): # WSZYSTKIE FUNKCJONALNOŚCI TAKIE SAME JAK DLA PRACOWNIKÓW

            def center_widgets_dzieci(event=None):
                window_width = root_dzieci_all.winfo_width()
                frame_height=root_dzieci.winfo_height()
                root_dzieci.place(x=window_width // 2, y=frame_height/2, anchor='center')

            def pokaz_wszystko_dzieci():
                radiobutton_all.select()
                listbox_dzieci.delete(0, END)
                for idx, object in enumerate(dzieci_list):
                    listbox_dzieci.insert(idx, f'Dziecko {object.name} {object.surname}')

            def pokaz_zaznaczone_dzieci():
                if var.get()==1:
                    pokaz_wszystko_dzieci()
                elif var.get()==2:
                    zlobek=entry_start_zlobek.get()
                    listbox_dzieci.delete(0, END)
                    for idx, object in enumerate(dzieci_list):
                        if object.nursery==zlobek:
                            listbox_dzieci.insert(idx, f'Dziecko {object.name} {object.surname}')
                        else:
                            pass

            def dodaj_dziecko():
                imie=entry_dzieci_imie.get()
                nazwisko=entry_dzieci_nazwisko.get()
                zamieszkanie=entry_dzieci_zamieszkanie.get()
                zlobek=entry_dzieci_zlobek.get()

                dzieci_list.append(Child(name=imie, surname=nazwisko, location=zamieszkanie, nursery=zlobek))

                entry_dzieci_imie.delete(0, END)
                entry_dzieci_nazwisko.delete(0, END)
                entry_dzieci_zamieszkanie.delete(0, END)
                entry_dzieci_zlobek.delete(0, END)

                pokaz_zaznaczone_dzieci()

            def edytuj_dziecko():
                global lista_dziec
                if var.get()==1:
                    lista_dziec=dzieci_list

                elif var.get()==2:
                    zlobek=entry_start_zlobek.get()
                    lista_dziec=[]
                    do_usuniecia = []
                    for object in dzieci_list:
                        if object.nursery == zlobek:
                            lista_dziec.append(object)
                            do_usuniecia.append(object)
                    for obj in do_usuniecia:
                        dzieci_list.remove(obj)

                i=listbox_dzieci.index(ACTIVE)

                entry_dzieci_imie.delete(0, END)
                entry_dzieci_nazwisko.delete(0, END)
                entry_dzieci_zamieszkanie.delete(0, END)
                entry_dzieci_zlobek.delete(0, END)

                entry_dzieci_imie.insert(0, lista_dziec[i].name)
                entry_dzieci_nazwisko.insert(0, lista_dziec[i].surname)
                entry_dzieci_zamieszkanie.insert(0, lista_dziec[i].location)
                entry_dzieci_zlobek.insert(0, lista_dziec[i].nursery)

                button_dzieci_dodaj_dziecko.config(text='Zapisz zmiany', command=lambda: aktualizuj_dziecko(i))

            def aktualizuj_dziecko(i):
                global dzieci_list
                imie=entry_dzieci_imie.get()
                nazwisko=entry_dzieci_nazwisko.get()
                zamieszkanie=entry_dzieci_zamieszkanie.get()
                zlobek=entry_dzieci_zlobek.get()

                if var.get() == 1:
                    lista_dziec[i].name=imie
                    lista_dziec[i].surname=nazwisko
                    lista_dziec[i].location=zamieszkanie
                    lista_dziec[i].nursery=zlobek
                    dzieci_list=lista_dziec

                elif var.get()==2:
                    lista_dziec[i].name=imie
                    lista_dziec[i].surname=nazwisko
                    lista_dziec[i].location=zamieszkanie
                    lista_dziec[i].nursery=zlobek
                    for object in lista_dziec:
                        dzieci_list.append(object)

                button_dzieci_dodaj_dziecko.config(text='Dodaj dziecko', command=dodaj_dziecko)

                entry_dzieci_imie.delete(0, END)
                entry_dzieci_nazwisko.delete(0, END)
                entry_dzieci_zamieszkanie.delete(0, END)
                entry_dzieci_zlobek.delete(0, END)

                pokaz_zaznaczone_dzieci()

            def usun_dziecko():
                i = listbox_dzieci.index(ACTIVE)

                if var.get()==1:
                    dzieci_list.pop(i)

                elif var.get()==2:
                    zlobek=entry_start_zlobek.get()
                    removal_list=[]
                    do_usuniecia = []
                    for object in dzieci_list[:]:
                        if object.nursery == zlobek:
                            removal_list.append(object)
                            do_usuniecia.append(object)
                    for obj in do_usuniecia:
                        dzieci_list.remove(obj)
                    removal_list.pop(i)
                    for object in removal_list:
                        dzieci_list.append(object)

                pokaz_zaznaczone_dzieci()

            def pokaz_dziecko():
                i = listbox_dzieci.index(ACTIVE)
                if var.get()==1:
                    imie=dzieci_list[i].name
                    nazwisko=dzieci_list[i].surname
                    zamieszkanie=dzieci_list[i].location
                    zlobek=dzieci_list[i].nursery

                elif var.get()==2:
                    zlobek=entry_start_zlobek.get()
                    show_list=[]
                    do_usuniecia = []
                    for object in dzieci_list[:]:
                        if object.nursery == zlobek:
                            show_list.append(object)
                            do_usuniecia.append(object)
                    for obj in do_usuniecia:
                        dzieci_list.remove(obj)
                    imie=show_list[i].name
                    nazwisko=show_list[i].surname
                    zamieszkanie=show_list[i].location
                    zlobek=show_list[i].nursery

                label_dzieci_imie_szczegoly_wartosc.config(text=imie)
                label_dzieci_nazwisko_szczegoly_wartosc.config(text=nazwisko)
                label_dzieci_zamieszkanie_szczegoly_wartosc.config(text=zamieszkanie)
                label_dzieci_zlobek_szczegoly_wartosc.config(text=zlobek)

            root_dzieci_all = Toplevel(root_choice)
            root_dzieci_all.title('System żłobków')
            szer = 690
            wys = 490
            root_dzieci_all.geometry(f'{szer}x{wys}')
            root_dzieci_all.bind('<Configure>', center_widgets_dzieci)

            root_dzieci=Frame(root_dzieci_all)
            root_dzieci.grid(row=0, column=0)

            ramka_dzieci_start = Frame(root_dzieci)
            ramka_dzieci_lista = Frame(root_dzieci)
            ramka_dzieci_formularz = Frame(root_dzieci)
            ramka_dzieci_szczegoly = Frame(root_dzieci)

            ramka_dzieci_start.grid(row=0, column=0, columnspan=2)
            ramka_dzieci_lista.grid(row=1, column=1)
            ramka_dzieci_formularz.grid(row=1, column=0)
            ramka_dzieci_szczegoly.grid(row=2, column=0, columnspan=2)

            # ---------------------------------------
            # ramka dzieci_start
            # ---------------------------------------
            label_dzieci_lista = Label(ramka_dzieci_start, text='Lista dzieci w żłobkach', font=('Arial', 12, 'bold'))
            button_dzieci_pokaz_liste = Button(ramka_dzieci_start, text='Pokaż wszystko', command=pokaz_wszystko_dzieci)
            label_dzieci_wybor = Label(ramka_dzieci_start, text='Wybierz formułę wyświetlania dzieci')
            var = IntVar()
            radiobutton_all = Radiobutton(ramka_dzieci_start, text='Wszystkie dzieci', variable=var, value=1)
            radiobutton_some = Radiobutton(ramka_dzieci_start, text='Dzieci z danego żłobka (nazwa)', variable=var, value=2)
            entry_start_zlobek = Entry(ramka_dzieci_start)
            button_dzieci_pokaz_wybrane = Button(ramka_dzieci_start, text='Pokaż zaznaczone', command=pokaz_zaznaczone_dzieci)

            label_dzieci_lista.grid(row=0, column=0, columnspan=3, padx=(szer / 2 - label_dzieci_lista.winfo_reqwidth() / 2), pady=(10, 0))
            button_dzieci_pokaz_liste.grid(row=1, column=0, columnspan=3)
            label_dzieci_wybor.grid(row=2, column=0, pady=(10, 0), columnspan=3)
            radiobutton_all.grid(row=3, column=0, columnspan=3)
            radiobutton_some.grid(row=4, column=0, columnspan=3)
            entry_start_zlobek.grid(row=5, column=0, columnspan=3)
            button_dzieci_pokaz_wybrane.grid(row=6, column=0, columnspan=3)

            # ---------------------------------------
            # ramka dzieci_lista
            # ---------------------------------------
            listbox_dzieci = Listbox(ramka_dzieci_lista, width=50)
            button_dzieci_pokaz_szczegoly = Button(ramka_dzieci_lista, text='Pokaż dane dziecka', command=pokaz_dziecko)
            button_dzieci_usun = Button(ramka_dzieci_lista, text='Usuń dziecko', command=usun_dziecko)
            button_dzieci_edytuj = Button(ramka_dzieci_lista, text='Edytuj dziecko', command=edytuj_dziecko)

            listbox_dzieci.grid(row=0, column=0, columnspan=3, pady=(10, 0))
            button_dzieci_pokaz_szczegoly.grid(row=1, column=0)
            button_dzieci_usun.grid(row=1, column=1)
            button_dzieci_edytuj.grid(row=1, column=2)

            # ---------------------------------------
            # ramka dzieci_formularz
            # ---------------------------------------
            label_dzieci_nowy_obiekt = Label(ramka_dzieci_formularz, text='Formularz edycji i dodawania:', font=('Arial', 10))
            label_dzieci_imie = Label(ramka_dzieci_formularz, text='Imię')
            label_dzieci_nazwisko = Label(ramka_dzieci_formularz, text='Nazwisko')
            label_dzieci_zamieszkanie = Label(ramka_dzieci_formularz, text='Zamieszkały/a')
            label_dzieci_zlobek = Label(ramka_dzieci_formularz, text='Prznależność')

            entry_dzieci_imie = Entry(ramka_dzieci_formularz)
            entry_dzieci_nazwisko = Entry(ramka_dzieci_formularz)
            entry_dzieci_zamieszkanie = Entry(ramka_dzieci_formularz)
            entry_dzieci_zlobek = Entry(ramka_dzieci_formularz)

            label_dzieci_nowy_obiekt.grid(row=0, column=0, columnspan=2)
            label_dzieci_imie.grid(row=1, column=0, sticky=W)
            label_dzieci_nazwisko.grid(row=2, column=0, sticky=W)
            label_dzieci_zamieszkanie.grid(row=3, column=0, sticky=W)
            label_dzieci_zlobek.grid(row=4, column=0, sticky=W)

            entry_dzieci_imie.grid(row=1, column=1, sticky=W)
            entry_dzieci_nazwisko.grid(row=2, column=1, sticky=W)
            entry_dzieci_zamieszkanie.grid(row=3, column=1, sticky=W)
            entry_dzieci_zlobek.grid(row=4, column=1, sticky=W)

            button_dzieci_dodaj_dziecko = Button(ramka_dzieci_formularz, text='Dodaj dziecko', command=dodaj_dziecko)
            button_dzieci_dodaj_dziecko.grid(row=6, column=0, columnspan=2)

            # ---------------------------------------
            # ramka dzieci_szczegoly
            # ---------------------------------------
            label_dzieci_opis_obiektu = Label(ramka_dzieci_szczegoly, text='Szczegóły dzieci:', font=('Arial', 10))
            label_dzieci_imie_szczegoly = Label(ramka_dzieci_szczegoly, text='Imię')
            label_dzieci_imie_szczegoly_wartosc = Label(ramka_dzieci_szczegoly, text='...', width=20)

            label_dzieci_nazwisko_szczegoly = Label(ramka_dzieci_szczegoly, text='Nazwisko')
            label_dzieci_nazwisko_szczegoly_wartosc = Label(ramka_dzieci_szczegoly, text='...', width=20)

            label_dzieci_zamieszkanie_szczegoly = Label(ramka_dzieci_szczegoly, text='Zamieszkały/a')
            label_dzieci_zamieszkanie_szczegoly_wartosc = Label(ramka_dzieci_szczegoly, text='...', width=20)

            label_dzieci_zlobek_szczegoly = Label(ramka_dzieci_szczegoly, text='Przynależność')
            label_dzieci_zlobek_szczegoly_wartosc = Label(ramka_dzieci_szczegoly, text='...', width=20)

            label_dzieci_opis_obiektu.grid(row=0, column=0, columnspan=5, pady=10)

            label_dzieci_imie_szczegoly.grid(row=1, column=0)
            label_dzieci_imie_szczegoly_wartosc.grid(row=2, column=0)

            label_dzieci_nazwisko_szczegoly.grid(row=1, column=1)
            label_dzieci_nazwisko_szczegoly_wartosc.grid(row=2, column=1)

            label_dzieci_zamieszkanie_szczegoly.grid(row=1, column=2)
            label_dzieci_zamieszkanie_szczegoly_wartosc.grid(row=2, column=2)

            label_dzieci_zlobek_szczegoly.grid(row=1, column=3)
            label_dzieci_zlobek_szczegoly_wartosc.grid(row=2, column=3)

            root_dzieci.mainloop()


        # okno dotyczące mapy
        def mapa():

            def center_widgets_mapa(event=None): # centruje widżety
                window_width = root_mapa_all.winfo_width()
                frame_height=root_mapa.winfo_height()
                root_mapa.place(x=window_width // 2, y=frame_height/2, anchor='center')

            def center_map_zlobki(lista_mapa_z:list): # centruje widok mapy na podstawie listy współrzędnych żłobków
                lats=[]
                lons=[]

                for coords in lista_mapa_z:
                    lats.append(coords[0])
                    lons.append(coords[1])

                min_lat = min(lat for lat in lats) # zasięgi
                max_lat = max(lat for lat in lats)
                min_lon = min(lon for lon in lons)
                max_lon = max(lon for lon in lons)

                center_lat = (float(min_lat) + float(max_lat)) / 2 # średnie współrzędne
                center_lon = (float(min_lon) + float(max_lon)) / 2

                return (center_lat, center_lon)

            def extent_zoom_zlobki(lista_mapa_z:list): # określa zoom w zależności od zasięgu na podstawie żłobków
                lats=[]
                lons=[]

                for coords in lista_mapa_z:
                    lats.append(coords[0])
                    lons.append(coords[1])

                min_lat = min(lat for lat in lats) # zasięgi
                max_lat = max(lat for lat in lats)
                min_lon = min(lon for lon in lons)
                max_lon = max(lon for lon in lons)

                extent_width=float(max_lat) - float(min_lat) # średnie współrzędne
                extent_height=float(max_lon) - float(min_lon)

                extent_width_zoom=math.log(extent_width / 1155) / (-0.716) # wzór znaleziony w internecie do określania optymalnego zasięgu
                extent_height_zoom=math.log(extent_height / 260) / (-0.69)

                if extent_height_zoom<extent_width_zoom:
                    return int(round(extent_height_zoom,0)) # zaokrągla do całości
                else:
                    return int(round(extent_width_zoom,0))

            def center_map_pracownicy(lista_mapa_p: list): # centruje mapę pracowników (tak samo jak dla żłobków)
                lats = []
                lons = []

                for coords in lista_mapa_p:
                    lats.append(coords[0])
                    lons.append(coords[1])

                min_lat = min(lat for lat in lats)
                max_lat = max(lat for lat in lats)
                min_lon = min(lon for lon in lons)
                max_lon = max(lon for lon in lons)

                center_lat = (float(min_lat) + float(max_lat)) / 2
                center_lon = (float(min_lon) + float(max_lon)) / 2

                return (center_lat, center_lon)

            def extent_zoom_pracownicy(lista_mapa_p: list): # określa zoom mapy dla pracowników (tak samo jak dla żłobków)
                lats = []
                lons = []

                for coords in lista_mapa_p:
                    lats.append(coords[0])
                    lons.append(coords[1])

                min_lat = min(lat for lat in lats)
                max_lat = max(lat for lat in lats)
                min_lon = min(lon for lon in lons)
                max_lon = max(lon for lon in lons)

                extent_width = float(max_lat) - float(min_lat)
                extent_height = float(max_lon) - float(min_lon)

                extent_width_zoom = math.log(extent_width / 1155) / (-0.716)
                extent_height_zoom = math.log(extent_height / 260) / (-0.69)

                if extent_height_zoom < extent_width_zoom:
                    return int(round(extent_height_zoom, 0))
                else:
                    return int(round(extent_width_zoom, 0))
                
            def center_map_dzieci(lista_mapa_d: list): # centruje mapę dla dzieci (tak samo jak dla żłobków)
                lats = []
                lons = []

                for coords in lista_mapa_d:
                    lats.append(coords[0])
                    lons.append(coords[1])

                min_lat = min(lat for lat in lats)
                max_lat = max(lat for lat in lats)
                min_lon = min(lon for lon in lons)
                max_lon = max(lon for lon in lons)

                center_lat = (float(min_lat) + float(max_lat)) / 2
                center_lon = (float(min_lon) + float(max_lon)) / 2

                return (center_lat, center_lon)

            def extent_zoom_dzieci(lista_mapa_d: list): # określa zoom mapy dla dzieci (tak samo jak dla żłobków)
                lats = []
                lons = []

                for coords in lista_mapa_d:
                    lats.append(coords[0])
                    lons.append(coords[1])

                min_lat = min(lat for lat in lats)
                max_lat = max(lat for lat in lats)
                min_lon = min(lon for lon in lons)
                max_lon = max(lon for lon in lons)

                extent_width = float(max_lat) - float(min_lat)
                extent_height = float(max_lon) - float(min_lon)

                extent_width_zoom = math.log(extent_width / 1155) / (-0.716)
                extent_height_zoom = math.log(extent_height / 260) / (-0.69)

                if extent_height_zoom < extent_width_zoom:
                    return int(round(extent_height_zoom, 0))
                else:
                    return int(round(extent_width_zoom, 0))

            def mapa_zlobki(): # funkcja mapy dla żłobków
                coords_for_map=[]
                for object in zlobki_list:
                    zlobek=object.coordinates
                    coords_for_map.append(zlobek) # lista współrzędnych dla żłobków

                mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0) # inicjalizacja mapy
                mapa.set_position(center_map_zlobki(coords_for_map)[0], center_map_zlobki(coords_for_map)[1]) # centrowanie mapy
                mapa.set_zoom(extent_zoom_zlobki(coords_for_map)) # określanie zoomu mapy
                mapa.grid(row=9, column=0, columnspan=3, pady=(10,0)) # pozycja mapy

                tuples_coords = []
                for object in zlobki_list:
                    zlobek=object.coordinates
                    tuples_coords.append(zlobek)
                    mapa.set_marker(zlobek[0], zlobek[1], text=f'{object.name}', font=('Arial', 10, 'bold'), text_color='black') # wstawianie markerów w miejsca żłobków z odpowiednim opisem

            def mapa_pracowicy(): # funkcja mapy dla pracowników (to samo co dla żłobków)
                coords_for_map=[]
                for object in pracownicy_list:
                    zamieszkanie=object.coordinates
                    coords_for_map.append(zamieszkanie)

                mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
                mapa.set_position(center_map_pracownicy(coords_for_map)[0], center_map_pracownicy(coords_for_map)[1])
                mapa.set_zoom(extent_zoom_pracownicy(coords_for_map))
                mapa.grid(row=9, column=0, columnspan=3, pady=(10,0))

                for object in pracownicy_list:
                    zamieszkanie=object.coordinates
                    mapa.set_marker(zamieszkanie[0], zamieszkanie[1], text=f'{object.name} {object.surname}', font=('Arial', 8), text_color='black')

            def mapa_pracowicy_ze_zlobka(): # funkcja mapy dla pracowników z konkretnego żłobka (to samo co dla żłobków)
                zlobek=entry_mapa_zlobek_prac.get() # pobieranie nazwy żłobka z pola wpisywania
                chosen_list=[]
                for object in pracownicy_list:
                    if object.nursery==zlobek:
                        chosen_list.append(object)

                coords_for_map=[]
                for object in chosen_list:
                    zamieszkanie=object.coordinates
                    coords_for_map.append(zamieszkanie) # jeśli nazwa żłobka zgadza się z wprowadzonym

                mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
                mapa.set_position(center_map_pracownicy(coords_for_map)[0], center_map_pracownicy(coords_for_map)[1])
                mapa.set_zoom(extent_zoom_pracownicy(coords_for_map))
                mapa.grid(row=9, column=0, columnspan=3, pady=(10,0))

                for object in chosen_list:
                    zamieszkanie=object.coordinates
                    mapa.set_marker(zamieszkanie[0], zamieszkanie[1], text=f'{object.name} {object.surname}', font=('Arial', 8), text_color='black')

            def mapa_dzieci():  # funkcja mapy dla dzieci (to samo co dla żłobków)
                coords_for_map=[]
                for object in dzieci_list:
                    zamieszkanie=object.coordinates
                    coords_for_map.append(zamieszkanie)

                mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
                mapa.set_position(center_map_dzieci(coords_for_map)[0], center_map_dzieci(coords_for_map)[1])
                mapa.set_zoom(extent_zoom_dzieci(coords_for_map))
                mapa.grid(row=9, column=0, columnspan=3, pady=(10,0))

                for object in dzieci_list:
                    zamieszkanie=object.coordinates
                    mapa.set_marker(zamieszkanie[0], zamieszkanie[1], text=f'{object.name} {object.surname}', font=('Arial', 8), text_color='black')

            def mapa_dzieci_ze_zlobka():  # funkcja mapy dla dzieci z konkretnego żłobka (to samo co dla żłobków)
                zlobek=entry_mapa_zlobek_dziec.get() # pobieranie nazwy żłobka z pola wpisywania
                chosen_list=[]
                for object in dzieci_list:
                    if object.nursery==zlobek:
                        chosen_list.append(object)

                coords_for_map=[]
                for object in chosen_list:
                    zamieszkanie=object.coordinates
                    coords_for_map.append(zamieszkanie) # jeśli nazwa żłobka zgadza się z wprowadzonym

                mapa = TkinterMapView(ramka_mapa, width=700, height=300, corner_radius=0)
                mapa.set_position(center_map_dzieci(coords_for_map)[0], center_map_dzieci(coords_for_map)[1])
                mapa.set_zoom(extent_zoom_dzieci(coords_for_map))
                mapa.grid(row=9, column=0, columnspan=3, pady=(10,0))

                for object in chosen_list:
                    zamieszkanie=object.coordinates
                    mapa.set_marker(zamieszkanie[0], zamieszkanie[1], text=f'{object.name} {object.surname}', font=('Arial', 8), text_color='black')

            root_mapa_all = Toplevel(root_choice) # okienko mapy podrzędne do okna wyboru
            root_mapa_all.title('System żłobków')
            szer = 800
            wys = 600
            root_mapa_all.geometry(f'{szer}x{wys}')
            root_mapa_all.bind('<Configure>', center_widgets_mapa) # centrowanie widżetów

            root_mapa=Frame(root_mapa_all) # główna ramka
            root_mapa.grid(row=0, column=0)

            ramka_mapa = Frame(root_mapa)
            ramka_mapa.grid(row=0, column=3, columnspan=2)

            # ---------------------------------------
            # ramka mapa
            # ---------------------------------------
            label_mapa_start = Label(ramka_mapa, text='Portal mapowy', font=('Arial', 12, 'bold')) # poszczególne napisy, pola wprowadzania i przyciski
            label_mapa_wybor = Label(ramka_mapa, text='Wybierz mapę do wyświetlenia:')
            label_mapa_zlobki = Label(ramka_mapa, text='Mapa wszystkich żłobków')
            button_mapa_zlobki = Button(ramka_mapa, text='Wyświetl', command=mapa_zlobki)
            label_mapa_pracownicy = Label(ramka_mapa, text='Mapa wszystkich pracowników')
            button_mapa_pracownicy = Button(ramka_mapa, text='Wyświetl', command=mapa_pracowicy)
            label_mapa_dzieci = Label(ramka_mapa, text='Mapa wszystkich dzieci')
            button_mapa_dzieci = Button(ramka_mapa, text='Wyświetl', command=mapa_dzieci)
            label_mapa_pracownicy_zlobka = Label(ramka_mapa, text='Mapa pracowników wybranego żłobka')
            label_mapa_zlobek_prac = Label(ramka_mapa, text='Żłobek')
            entry_mapa_zlobek_prac = Entry(ramka_mapa)
            button_mapa_pracownicy_zlobka = Button(ramka_mapa, text='Wyświetl', command=mapa_pracowicy_ze_zlobka)
            label_mapa_dzieci_zlobka = Label(ramka_mapa, text='Mapa dzieci wybranego żłobka')
            label_mapa_zlobek_dziec = Label(ramka_mapa, text='Żłobek')
            entry_mapa_zlobek_dziec = Entry(ramka_mapa)
            button_mapa_dzieci_zlobka = Button(ramka_mapa, text='Wyświetl', command=mapa_dzieci_ze_zlobka)

            label_mapa_start.grid(row=0, column=0, columnspan=3, pady=(10, 0)) # umiejscowienie napisów, pól wprowadzania i przycisków
            label_mapa_wybor.grid(row=1, column=0, columnspan=3)
            label_mapa_zlobki.grid(row=2, column=0, sticky=W)
            button_mapa_zlobki.grid(row=2, column=1, sticky=E)
            label_mapa_pracownicy.grid(row=3, column=0, sticky=W)
            button_mapa_pracownicy.grid(row=3, column=1, sticky=E)
            label_mapa_dzieci.grid(row=4, column=0, sticky=W)
            button_mapa_dzieci.grid(row=4, column=1, sticky=E)
            label_mapa_pracownicy_zlobka.grid(row=5, column=0, sticky=W)
            label_mapa_zlobek_prac.grid(row=6, column=0, sticky=W)
            entry_mapa_zlobek_prac.grid(row=6, column=0, padx=50, sticky=W)
            button_mapa_pracownicy_zlobka.grid(row=6, column=1, sticky=E)
            label_mapa_dzieci_zlobka.grid(row=7, column=0, sticky=W)
            label_mapa_zlobek_dziec.grid(row=8, column=0, sticky=W)
            entry_mapa_zlobek_dziec.grid(row=8, column=0, padx=50, sticky=W)
            button_mapa_dzieci_zlobka.grid(row=8, column=1, sticky=E)

            root_mapa.mainloop() # okienko w pętli żeby się nie zamykało


        def center_widgets_choice(event=None): # centrowanie widżetów okna wyboru
            window_width = root_choice.winfo_width()
            frame_height = ramka_wybor.winfo_height()

            ramka_wybor.place(x=window_width // 2, y=frame_height / 2, anchor='center')

        root_pass.withdraw() # wyjście z okna logowania

        root_choice=Toplevel() # okienko wyboru funkcjonalności
        root_choice.title('Wybór funkcjonalności')
        root_choice.geometry('270x130')

        root_choice.bind('<Configure>', center_widgets_choice) # centrowanie widżetów okna wyboru

        ramka_wybor=Frame(root_choice) # główna ramka
        ramka_wybor.grid(row=0, column=0)

        label_wybor_opcje=Label(ramka_wybor,text='Wybierz funkcjonalność do uruchomienia') # napisy i przyciski okna wyboru
        label_wybor_zlobki=Label(ramka_wybor, text='Lista żłobków')
        label_wybor_pracownicy=Label(ramka_wybor, text='Lista pracowników żłobków')
        label_wybor_dzieci=Label(ramka_wybor, text='Lista podopiecznych żłobków')
        label_wybor_mapa=Label(ramka_wybor, text='Portal mapowy')
        button_wybor_remonty=Button(ramka_wybor,text='Wybierz', command=zlobki)
        button_wybor_pracownicy=Button(ramka_wybor,text='Wybierz', command=pracownicy)
        button_wybor_dzieci=Button(ramka_wybor,text='Wybierz', command=dzieci)
        button_wybor_mapa=Button(ramka_wybor,text='Wybierz', command=mapa)

        label_wybor_opcje.grid(row=0, column=0, columnspan=2) # umiejscowienie wyżej określonych elementów
        label_wybor_zlobki.grid(row=1, column=0, sticky=W)
        label_wybor_pracownicy.grid(row=2, column=0, sticky=W)
        label_wybor_dzieci.grid(row=3, column=0, sticky=W)
        label_wybor_mapa.grid(row=4, column=0, sticky=W)
        button_wybor_remonty.grid(row=1, column=1, sticky=E)
        button_wybor_pracownicy.grid(row=2, column=1, sticky=E)
        button_wybor_dzieci.grid(row=3, column=1, sticky=E)
        button_wybor_mapa.grid(row=4, column=1, sticky=E)

        root_choice.mainloop() # okienko w pętli żeby się nie zamykało

    else:
        wrong_label=Label(ramka_logowanie,text='Błędne hasło, spróbuj jeszcze raz') # jeśli hasło jest błędne
        wrong_label.grid(row=2, column=0, columnspan=2, padx=3)
        logowanie_entry.delete(0, END) # czyści okeienko wprowadzania
        logowanie_entry.focus() # wprowadza kursor do pola wprowadzania


def center_widgets_pass(event=None): # centrowanie widżetów okna logowania
    window_width = root_pass.winfo_width()
    frame_height = ramka_logowanie.winfo_height()

    ramka_logowanie.place(x=window_width // 2, y=frame_height / 2, anchor='center')

root_pass=Tk() # podstawowe okno programu - logowanie
root_pass.title('System żłobków - logowanie')
root_pass.geometry('195x70')

root_pass.bind('<Configure>', center_widgets_pass)  # centrowanie widżetów okna logowania

ramka_logowanie=Frame(root_pass) # główna ramka
ramka_logowanie.grid(row=0, column=0)

logowanie_napis=Label(ramka_logowanie, text='Podaj hasło dostępu') # napis, okienko wprowadzania i przycisk
logowanie_entry=Entry(ramka_logowanie, width=20, show='•') # show powoduje że hasło jest zakryte
logowanie_entry.bind('<Return>', logowanie) # pozwala na zatwierdzanie przez wciśnięcie Enter na klawiaturze
logowanie_button=Button(ramka_logowanie, text='Enter', command=logowanie)

logowanie_napis.grid(row=0, column=0, columnspan=2)
logowanie_entry.grid(row=1, column=0, padx=(3,0))
logowanie_button.grid(row=1, column=1, columnspan=2)

root_pass.mainloop() # całe okienko w pętli żeby się nie zamykało