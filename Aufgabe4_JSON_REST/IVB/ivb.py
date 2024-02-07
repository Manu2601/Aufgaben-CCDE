import json
import requests

def getStop(json_data, eingabe):
    matching_stops = []
    for stop in json_data:
        stop_info = stop.get('stop') 
        if eingabe.lower() in stop_info.get('name').lower():
            name = stop_info.get('name')
            url = "https://smartinfo.ivb.at/api/JSON/PASSAGE?stopID=" + stop_info.get("uid")
            detailed_stop_info = requests.get(url).json()
            matching_stops.append((name, detailed_stop_info))
    
    return matching_stops

def addFavorite(eingabe):
    matching_stops = getStop(data, eingabe)
    if matching_stops:
        for name, _ in matching_stops:
            if name in favorites:
                print("Haltestelle '{}' schon in Favoriten!".format(name))
            else:
                printStops(name) 
                confirmation = input("Möchten Sie diese Haltestelle zu Favoriten hinzufügen? (Ja/Nein): ").lower()
                if confirmation == "ja":
                    favorites.append(name)
                    print("Haltestelle '{}' zu Favoriten hinzugefügt!".format(name))
                else:
                    print("Haltestelle '{}' wurde nicht zu Favoriten hinzugefügt.".format(name))
    else:
        print("Haltestelle nicht gefunden.")


def showFavorites():
    if not favorites:
        print("Keine Favoriten vorhanden.")
    else:
        print("Favoriten:")
        for favorite_name in favorites:
            matching_stops = getStop(data, favorite_name)
            if matching_stops:
                name, favorite_info = matching_stops[0]
                print(name)
                for i in range(min(5, len(favorite_info))):  # Zeige maximal die ersten 5 Abfahrtszeiten
                    details = favorite_info[i].get("smartinfo")
                    zeit = details.get("time")
                    direction = details.get("direction")
                    print("{:>7} {}".format(zeit, direction))
                print("-" * 10)
            else:
                print("Fehler beim Abrufen von Abfahrtszeiten für '{}'.".format(favorite_name))

def printStops(eingabe):
    matching_stops = getStop(data, eingabe)
    for name, stop_info in matching_stops:
        print(name)
        for i in range(5):
            details = stop_info[i].get("smartinfo")
            zeit = details.get("time")
            direction = details.get("direction")
            print("{:>7} {}".format(zeit, direction))

favorites = []

response = requests.get("https://smartinfo.ivb.at/api/JSON/STOPS").json()

with open('data.json', 'w') as outfile:
    json.dump(response, outfile)

with open('data.json') as json_file:
    data = json.load(json_file)

while True:
    auswahl_modi = input("Haltestelle suchen (H), Favoriten hinzufügen (F), Favoriten anzeigen (A), Beenden (B): ").lower()

    if auswahl_modi == "h":
        eingabe = input("Haltestellenname eingeben: ")
        printStops(eingabe)
        
    elif auswahl_modi == "f":
        eingabe = input("Haltestellenname zum Favoriten hinzufügen: ")
        addFavorite(eingabe)

    elif auswahl_modi == "a":
        showFavorites()

    elif auswahl_modi == "b":
        print("Programm wird beendet.")
        break

    else:
        print("Ungültige Eingabe. Bitte wählen Sie eine der Optionen (H, F, A, B).")
