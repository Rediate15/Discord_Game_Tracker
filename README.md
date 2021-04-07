# Discord_Game_Tracker
 Ziel dieses Discord Bots ist es, das Verfolgen von Spiel Preisen zu ermöglichen. Hierfür kann mittels ein paar Befehlen, ein Spiel in eine Schleife aufgenommen werden. Alle Spiele in dieser Schleife werden täglich überprüft, ob es ein neues billigeres Angebot für jenes Spiel gibt. Gibt es ein Angebot, wird jedem Nutzer der dieses Spiel verfolgt eine Meldung mit den jeweiligen Angeboten geschickt. Aktuell werden diese Meldungen aus Überwachungsgründen noch in denselben Channel geschickt. Geplant ist, zu einem späteren Zeitpunkt, die Meldungen direkt an den jeweiligen Nutzer zu schicken.

## Befehle
**::info**  Gibt eine Info zum Bot sowie eine Liste aller Befehle

**clean** Löscht alle Nachrichten im Channel

**::track** Fügt ein Spiel zur Verfolgung in die Schleife hinzu

**::trackedGames** Zeigt alle von dir verfolgten Spiele

**::stopTracking** Entfernt Spiel aus den von dir verfolgten Spielen

**::stopAll** Entfernt alle Spiele
  
## Beispiel

Im Folgenden werden die Befehle an folgendem Beispiel demonstriert

![Steamshop Bild](https://raw.githubusercontent.com/Rediate15/Discord_Game_Tracker/main/steamshop.png)

Mit **::track https://store.steampowered.com/app/359550/Tom_Clancys_Rainbow_Six_Siege/** wird der erste Eintrag auf der Seite in die Verfolgung aufgenommen. In diesem Fall wäre es der Eintrag zu "Tom Clancy's Rainbow Six Siege kaufen" für 7,99€

Zur Verfolgung von anderen Einträgen auf dieser Seite genügt es den jeweiligen Titel vor der URL anzugeben. Mit **::track Tom Clancy's Rainbow Six Siege - Deluxe Edition kaufen https://store.steampowered.com/app/359550/Tom_Clancys_Rainbow_Six_Siege/** verfolgt man die Deluxe Edition für 9,89€

Wurde das Spiel in die Verfolgung aufgenommen, sollte **::trackedGames** das Spiel sowie alle anderen von dir verfolgten Spiele auflisten.

Möchte man das Spiel nicht weiter verfolgen, kann mit **::stopTracking Tom Clancy's Rainbow Six Siege kaufen** der jeweilige Eintrag entfernt werden.

Mit **::stopAll** werden alle verfolgten Spiele entfernt.

## Support
Bisher können nur Spiele und Bundles auf Steam verfolgt werden.

Geplant ist aber die Verfolgung auf Origin und Epic Games auszuweiten

## Anmerkung
Der Bot ist noch nicht gründlich getestet. Sollte es also zu irgendwelchen Fehlern kommen, könnt ihr diese gerne [hier](https://github.com/Rediate15/Discord_Game_Tracker/issues) melden. Gebt bitte das Datum und die ungefähre Uhrzeit an, damit ich den jeweiligen Fehler in der Log-Datei nachverfolgen kann.