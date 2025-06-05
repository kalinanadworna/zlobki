import requests as rq
from tkinter import *
from tkintermapview import TkinterMapView
import math

# Pobieranie współrzędnych dla adresu
def coordinates(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json"}
    response = rq.get(base_url, params)
    data = response.json()
    lat = data[0]["lat"]
    long = data[0]["lon"]
    return [float(lat), float(long)]

# Klasy reprezentujące żłobki, pracowników i dzieci
zlobki_list=[]
class Nursery:
    def __init__(self, name, location, workers:int, children:int):
        self.name = name
        self.location = location
        self.workers = sum(pracownicy_list)
        self.children = sum(dzieci_list)
        self.coordinates = self.coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

pracownicy_list=[]
class Worker:
    def __init__(self, name, surname, location, nursery):
        self.name = name
        self.surname = surname
        self.location = location
        self.nursery = nursery
        self.coordinates = self.coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

dzieci_list=[]
class Child:
    def __init__(self, name, surname, location, nursery):
        self.name = name
        self.surname = surname
        self.location = location
        self.nursery = nursery
        self.coordinates = self.coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

# ogólna funkcja zawierająca wszystkie okna (zaczyna od pierwszego - logowanie)
def logowanie(event=None):
    haslo=logowanie_entry.get()
    if haslo=='geoinfa_rzadzi':

        # okno dotyczące żłobków
        def zlobki():

            def center_widgets_zlobki(event=None):
                window_width = root_zlobki_all.winfo_width()
                frame_height=root_zlobki.winfo_height()
                root_zlobki.place(x=window_width // 2, y=frame_height/2, anchor='center')

            def pokaz_wszystko_zlobek():
                listbox_zlobki.delete(0, END)
                for idx, object in enumerate(zlobki_list):
                    listbox_zlobki.insert(idx, f'Żłobek {object.name}')

            def dodaj_zlobek():
                nazwa_zlobka=entry_zlobki_nazwa.get()
                miejsce_zlobka=entry_zlobki_miejsce.get()

                zlobki_list.append(Nursery(name=nazwa_zlobka, location=miejsce_zlobka))

                entry_zlobki_nazwa.delete(0, END)
                entry_zlobki_miejsce.delete(0, END)

                pokaz_wszystko_zlobek()

            def edytuj_zlobek():
                i=listbox_zlobki.index(ACTIVE)

                entry_zlobki_nazwa.delete(0, END)
                entry_zlobki_miejsce.delete(0, END)

                entry_zlobki_nazwa.insert(0, zlobki_list[i].name)
                entry_zlobki_miejsce.insert(0, zlobki_list[i].location)

                button_zlobki_dodaj_zlobek.config(text='Zapisz zmiany', command=lambda: aktualizuj_zlobek(i))

            def aktualizuj_zlobek(i):
                nazwa=entry_zlobki_nazwa.get()
                miejsce=entry_zlobki_miejsce.get()

                zlobki_list[i].name=nazwa
                zlobki_list[i].location=miejsce

                button_zlobki_dodaj_zlobek.config(text='Dodaj zlobek', command=dodaj_zlobek)

                zlobki_list[i].marker.delete()
                zlobki_list[i].coordinates=zlobki_list[i].coordinates()
                zlobki_list[i].marker=map_widget.set_marker(zlobki_list[i].coordinates[0], zlobki_list[i].coordinates[1])

                entry_zlobki_nazwa.delete(0, END)
                entry_zlobki_miejsce.delete(0, END)

                pokaz_wszystko_zlobek()

            def usun_zlobek():
                i = listbox_zlobki.index(ACTIVE)

                zlobki_list[i].marker.delete()
                zlobki_list.pop(i)

                pokaz_wszystko_zlobek()

            def pokaz_zlobek():
                i = listbox_zlobki.index(ACTIVE)

                nazwa=zlobki_list[i].name
                pracownicy=zlobki_list[i].workers
                dzieci=zlobki_list[i].children
                miejsce=zlobki_list[i].location

                label_zlobki_nazwa_szczegoly_wartosc.config(text=nazwa)
                label_zlobki_miejsce_szczegoly_wartosc.config(text=miejsce)
                label_zlobki_dzieci_szczegoly_wartosc.config(text=dzieci)
                label_zlobki_pracownicy_szczegoly_wartosc.config(text=pracownicy)

            root_zlobki_all = Toplevel(root_choice)
            root_zlobki_all.title('System żłobków')
            szer = 670
            wys = 360
            root_zlobki_all.geometry(f'{szer}x{wys}')
            root_zlobki_all.bind('<Configure>', center_widgets_zlobki)

            root_zlobki=Frame(root_zlobki_all)
            root_zlobki.grid(row=0, column=0)

            ramka_zlobki_start = Frame(root_zlobki)
            ramka_zlobki_lista = Frame(root_zlobki)
            ramka_zlobki_formularz = Frame(root_zlobki)
            ramka_zlobki_szczegoly = Frame(root_zlobki)

            ramka_zlobki_start.grid(row=0, column=0, columnspan=2)
            ramka_zlobki_lista.grid(row=1, column=0)
            ramka_zlobki_formularz.grid(row=1, column=1)
            ramka_zlobki_szczegoly.grid(row=2, column=0, columnspan=2)

            # ---------------------------------------
            # ramka zlobki_start
            # ---------------------------------------
            label_zlobki_lista = Label(ramka_zlobki_start, text='Lista żłobków', font=('Arial', 12, 'bold'))
            button_pokaz_liste = Button(ramka_zlobki_start, text='Pokaż wszystko', command=pokaz_wszystko_zlobek)

            label_zlobki_lista.grid(row=0, column=0, padx=(szer / 2 - label_zlobki_lista.winfo_reqwidth() / 2), pady=(10, 0))
            button_pokaz_liste.grid(row=1, column=0)

            # ---------------------------------------
            # ramka zlobki_lista
            # ---------------------------------------
            listbox_zlobki = Listbox(ramka_zlobki_lista, width=50)
            button_zlobki_pokaz_szczegoly = Button(ramka_zlobki_lista, text='Pokaż dane żłobka', command=pokaz_zlobek)
            button_zlobki_usun = Button(ramka_zlobki_lista, text='Usuń żłobek', command=usun_zlobek)
            button_zlobki_edytuj = Button(ramka_zlobki_lista, text='Edytuj żłobek', command=edytuj_zlobek)

            listbox_zlobki.grid(row=1, column=0, columnspan=3, pady=(10, 0))
            button_zlobki_pokaz_szczegoly.grid(row=2, column=0)
            button_zlobki_usun.grid(row=2, column=1)
            button_zlobki_edytuj.grid(row=2, column=2)

            # ---------------------------------------
            # ramka zlobki_formularz
            # ---------------------------------------
            label_zlobki_nowy_obiekt = Label(ramka_zlobki_formularz, text='Formularz edycji i dodawania:', font=('Arial', 10))

            label_zlobki_nazwa = Label(ramka_zlobki_formularz, text='Nazwa żłobka')
            label_zlobki_miejsce = Label(ramka_zlobki_formularz, text='Adres żłobka')

            entry_zlobki_nazwa = Entry(ramka_zlobki_formularz)
            entry_zlobki_miejsce = Entry(ramka_zlobki_formularz)

            label_zlobki_nowy_obiekt.grid(row=0, column=0, columnspan=2)
            label_zlobki_nazwa.grid(row=1, column=0, sticky=W)
            label_zlobki_miejsce.grid(row=2, column=0, sticky=W)

            entry_zlobki_nazwa.grid(row=1, column=1, sticky=W)
            entry_zlobki_miejsce.grid(row=2, column=1, sticky=W)

            button_zlobki_dodaj_zlobek = Button(ramka_zlobki_formularz, text='Dodaj żłobek', command=dodaj_zlobek)
            button_zlobki_dodaj_zlobek.grid(row=3, column=0, columnspan=2)

            # ---------------------------------------
            # ramka zlobki_szczegoly
            # ---------------------------------------
            label_zlobki_opis_obiektu = Label(ramka_zlobki_szczegoly, text='Szczegóły zlobeku:', font=('Arial', 10))
            label_zlobki_nazwa_szczegoly = Label(ramka_zlobki_szczegoly, text='Nazwa żłobka')
            label_zlobki_nazwa_szczegoly_wartosc = Label(ramka_zlobki_szczegoly, text='...', width=20)

            label_zlobki_miejsce_szczegoly = Label(ramka_zlobki_szczegoly, text='Adres żłobka')
            label_zlobki_miejsce_szczegoly_wartosc = Label(ramka_zlobki_szczegoly, text='...', width=20)

            label_zlobki_dzieci_szczegoly = Label(ramka_zlobki_szczegoly, text='Liczba podopiecznych')
            label_zlobki_dzieci_szczegoly_wartosc = Label(ramka_zlobki_szczegoly, text='...', width=20)

            label_zlobki_pracownicy_szczegoly = Label(ramka_zlobki_szczegoly, text='Liczba pracowników')
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

            root_zlobki_all.mainloop()

        def center_widgets_choice(event=None):
            window_width = root_choice.winfo_width()
            frame_height = ramka_wybor.winfo_height()

            ramka_wybor.place(x=window_width // 2, y=frame_height / 2, anchor='center')

        root_pass.withdraw()

        root_choice=Toplevel()
        root_choice.title('Wybór funkcjonalności')
        root_choice.geometry('270x110')

        root_choice.bind('<Configure>', center_widgets_choice)

        ramka_wybor=Frame(root_choice)
        ramka_wybor.grid(row=0, column=0)

        label_wybor_opcje=Label(ramka_wybor,text='Wybierz funkcjonalność do uruchomienia')
        label_wybor_zlobki=Label(ramka_wybor, text='Lista żłobków')
        label_wybor_pracownicy=Label(ramka_wybor, text='Lista pracowników żłobków')
        label_wybor_dzieci=Label(ramka_wybor, text='Lista podopiecznych żłobków')
        label_wybor_mapa=Label(ramka_wybor, text='Portal mapowy')
        button_wybor_remonty=Button(ramka_wybor,text='Wybierz', command=zlobki)
        button_wybor_pracownicy=Button(ramka_wybor,text='Wybierz', command=pracownicy)
        button_wybor_dzieci=Button(ramka_wybor,text='Wybierz', command=dzieci)
        button_wybor_mapa=Button(ramka_wybor,text='Wybierz', command=mapa)

        label_wybor_opcje.grid(row=0, column=0, columnspan=2)
        label_wybor_zlobki.grid(row=1, column=0, sticky=W)
        label_wybor_pracownicy.grid(row=2, column=0, sticky=W)
        label_wybor_dzieci.grid(row=3, column=0, sticky=W)
        label_wybor_mapa.grid(row=4, column=0, sticky=W)
        button_wybor_remonty.grid(row=1, column=1, sticky=E)
        button_wybor_pracownicy.grid(row=2, column=1, sticky=E)
        button_wybor_dzieci.grid(row=3, column=1, sticky=E)
        button_wybor_mapa.grid(row=4, column=1, sticky=E)

        root_choice.mainloop()

    else:
        wrong_label=Label(ramka_logowanie,text='Błędne hasło, spróbuj jeszcze raz')
        wrong_label.grid(row=2, column=0, columnspan=2, padx=3)
        logowanie_entry.delete(0, END)
        logowanie_entry.focus()


def center_widgets_pass(event=None):
    window_width = root_pass.winfo_width()
    frame_height = ramka_logowanie.winfo_height()

    ramka_logowanie.place(x=window_width // 2, y=frame_height / 2, anchor='center')

root_pass=Tk()
root_pass.title('System żłobków - logowanie')
root_pass.geometry('195x70')

root_pass.bind('<Configure>', center_widgets_pass)

ramka_logowanie=Frame(root_pass)
ramka_logowanie.grid(row=0, column=0)

logowanie_napis=Label(ramka_logowanie, text='Podaj hasło dostępu')
logowanie_entry=Entry(ramka_logowanie, width=20, show='•')
logowanie_entry.bind('<Return>', logowanie)
logowanie_button=Button(ramka_logowanie, text='Enter', command=logowanie)

logowanie_napis.grid(row=0, column=0, columnspan=2)
logowanie_entry.grid(row=1, column=0, padx=(3,0))
logowanie_button.grid(row=1, column=1, columnspan=2)

root_pass.mainloop()