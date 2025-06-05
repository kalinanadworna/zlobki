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
class Nursery:
    def __init__(self, location, workers, children):
        self.location = location
        self.workers = workers
        self.children = children
        self.coordinates = self.coordinates()
        self.marker = mapa.set_marker(self.coordinates[0], self.coordinates[1])

class Worker:
    def __init__(self, name, surname, location, nursery):
        self.name = name
        self.surname = surname
        self.location = location
        self.nursery = nursery
        self.coordinates = self.coordinates()
        self.marker = mapa.set_marker(self.coordinates[0], self.coordinates[1])

class Child:
    def __init__(self, name, surname, location, nursery):
        self.name = name
        self.surname = surname
        self.location = location
        self.nursery = nursery
        self.coordinates = self.coordinates()
        self.marker = mapa.set_marker(self.coordinates[0], self.coordinates[1])