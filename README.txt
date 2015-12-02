v0.2 2015-12-02 ab
#====================================================================================================#
   README - Willkommen zu "Alex' Rigor"
#====================================================================================================#


#-----------------------------------------------------------------------------------------------------
0. Was ist das?

    "Alex' Rigor" ist ein Programm um Vokabeln zu lernen.
    Das können einerseits Sprachen sein (Muttersprache - Fremdsprache), anderseits können mit diesem
    "Karteikasten-System" beliebige Wortpaare gelernt und geübt werden.
    Zur Demonstration sind dem Programm alle Land - Hauptstadt Paare beigegeben.

    
#-----------------------------------------------------------------------------------------------------
I. Inhalt

    1. Wie startet man "Alex' Rigor"?
    
    2. Was benötigt "Alex' Rigor" um zu starten?
    
    3. Übersicht: Ordner- und Dateistruktur
    
    4. Wie übt man eigene Vokabelsätze?


#-----------------------------------------------------------------------------------------------------
1. Wie startet man "Alex' Rigor"?

    * Ein Doppelklick auf die Datei "Rigor_v04.py" ist eine Möglichkeit.
    
    * Unter Punkt 3. findet sich eine Übersicht auf der ersichtlich ist, wo sich diese Datei befindet.


#-----------------------------------------------------------------------------------------------------
2. Was benötigt "Alex' Rigor" um zu starten?

    * Das Programm ist in Python 3 https://de.wikipedia.org/wiki/Python_%28Programmiersprache%29
      geschrieben und benötigt deshalb diese Sprache vor Ort.
    
    * Windows hat diese Sprache nicht vorinstalliert. Apple-Produkte hingegen vermutlich schon.
      Bei Linux ist Python schon mit dabei - evt. aber eine 2.x-Version.
    
    * Falls Python nicht installiert sein sollte, die Sprache ist frei verfügbar: 
        
        1. Download von Python 3.4 oder höher: https://www.python.org/downloads/
        2. Installieren von Python auf dem Computer.
        3. Die Installation sollte so funktionieren. Läuft das Programm aber nicht, so ist Python dem
           Pfad hinzuzufügen. Googeln: "add to path <Betriebssystem>"

           
#-----------------------------------------------------------------------------------------------------
3. Übersicht: Ordner- und Dateistruktur

    /-Rigor_v03-/-+
                  +- README.txt
                  +- README_2.txt
                  +- Rigor_v04.py
                  +
                  +-/-data-/-+
                  +          +- Hauptstädte.korp
                  +
                [ +-/-data_generation-/-+
                  +                     +- ANLEITUNG.txt
                  +                     +- csv2json.py
                  +                     +- DATA.ods
                  +                     +- Hauptstädte.csv ]  # Ordner nicht auf GitHub
                  +
                  +-/-varia-/-+
                              +- options.opt
                              +- rigoricon.ico


#-----------------------------------------------------------------------------------------------------
4. Wie übt man eigene Vokabelsätze?

    * Eine Anleitung zur Erstellung eigener Vokabelsätze liegt dem Programm bei.
    
    * Die Anleitung findet sich im Ordner "data_generation" und nennt sich "ANLEITUNG.txt"
    
    * In der Übersicht unter Punkt 2. ist die Anleitung auch aufgeführt.

