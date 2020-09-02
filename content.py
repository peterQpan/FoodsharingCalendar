def fistWindowText():
    return '''
    Foodsharing-GoogleCalendar
Bei Fragen, Anregungen, Ideen,
oder (hoffentlich nicht) Problemen:

sebmueller.sb@gmail.com

Dank an Kirsten,
die die Idee für dieses Projekt hatte.
Als freiwillige und engagiert
Betatesterin hat sie wirklich 
Nerven und Durchhaltevermögen bewiesen!!!

Bitte stelle sicher, dass du dir selbst das Original-Programm
entweder von GitHub oder SourceForge heruntergeladen hast.
Dort kann man auch den SourceCode einsehen.

Achtung!!!
Mit Windows Betriebssystem benötigst du außerdem: 
"Microsoft Visual Studio Redistributable Runtime",
Kostenlos erhältlich beim MicrosoftSupport, unter:

"https://support.microsoft.com/de-de/help/2977003/the-latest-supported-visual-c-downloads"

Alles Weitere findest du in der README.txt
Viel Spaß'''

#
# Hallo und Willkommen
# in meinem
# Foodsharing-GoogleCalendar
# Programm!!!!
# für Fragen, Anregungen, Ideen,
# oder (hoffentlich nicht) Problemen:
#
# sebmueller.sb@gmail.com
#
#
# Dank an Kirsten,
# die die Idee für dieses Projekt hatte.
# Als freiwillige und engagiert
# Betatesterin hat sie wirklich
# Nerven und Durchhaltevermögen bewiesen!!!
#
#
# Dieses Programm dient dazu, Termine auf Foodsharing.de
# mit deinem GoogleCalendar abzugleichen.
# Bitte stelle sicher, dass du dir selbst das Original-Programm,
# entweder von GitHub oder SourceForge heruntergeladen hast.
# Denn du musst dich sowohl auf deinem GoogleCalendar einloggen,
# als auch deine Zugangsdaten für Foodsharing eingeben.
# Damit jeder sehen kann dass ich es nicht auf deine Anmeldedaten
# abgesehen habe, habe ich den Quellcode dieses Programms auf
# Github zur Einsicht freigegeben.
#
# Achtung!!!
# Solltest du ein Windows Betriebssystem verwenden,
# so ist es erforderlich, dass das
# "Microsoft Visual Studio Redistributable Runtime",
# kostenlos erhältlich vom MicrosoftSupport unter:
#
# "https://support.microsoft.com/de-de/help/2977003/the-latest-supported-visual-c-downloads"
#
# auf deinem Rechner installiert ist,
# es wird benötigt um den "Scanner" für die
# Foodsharing-Webseite, die fast ausschlieslich
# auf JavaScript basiert, laufen zu lassen,
# ebenfalls und aus dem selben Grund benötigst du den
# Geckodriver für Mozilla Firefox. Ich habe ihn da,
# er GNU lizensiert ist dem Package mit hinzugefügt,
# er ist, falls nötig ebenfalls hier auf GitHub
# auf folgender Seite (ganz unten) herunterladen.
#
# https://github.com/mozilla/geckodriver/releases/tag/v0.26.0
#
# Bitte nutze die hier im Package vorgegebene
# Ordnerstrucktur, oder passe den Code entsprechend an.
#
#
# Das Progamm läuft vollkommen selbstständig,
# lässt dich aber in einem Logging-Fenster
# immer genau wissen was es gerade tut.
# Es besitzt keinerlei Befehlsstruckturen,
# die ein Löschen im GoogleCalendar vorsehen!!!
# Es gleicht bestehende Termine mit neuen Terminen
# von Foodsharing ab und warnt am Ende in einer
# kurzen Zusammenfassung, wenn sich Termine
# überschneiden, oder enger aneinander liegen
# als 45 Minuten, wobei es davon ausgeht dass
# neue FS-Termine ebenfalls 45Minuten dauern.
# Es kann normale Termine, ganztägige Termine und
# wiederkehrende Termine vergleichen,
# Aufgaben und Erinnerungen sind im genutzten
# Google-Event-Interface nicht mit enthalten
# und werden deshalb nicht berücksichtigt.
#
# Solltest du die Option Passwort merken wählen,
# so wird dein Passwort und dein Login-Name,
# verschlüsselt und in einer Datein im
# Programmordner auf deinem Gerät gespeichert.
# Das von mir gewählte Verschlüsselungsverfahren
# ist so sicher, dass ich mit Sicherheit sagen kann:
# Sollte tatsächlich jemand den Aufwand betreiben,
# die Resorcen besitzen und auch noch
# entsprechenden Zugriff auf deien Rechner
# erlangt haben um an dieses Passwort zu kommen,
# dann hast du ganz, ganz andere Probleme als ein
# gehacktes Foodsharing-Passwort.
#
# Da fühlt man sich doch gleich besser^^
# nicht wahr?!? :D :'D ':)
#
# Dann wünsche ich dir viel Vergnügen mit dieser
# Arbeitserleichterung, wenn du weniger mit
# Terminen verwalten beschäftigt bist kannst du
# vielleicht mehr Termine wahrnehmen?!?! Ich
# bin jetzt schon ganz geflasht wieviel
# Mehr-Zeit ich FS mit diesem Engagement
# hier vielleicht beschert habe!!! :D
# Es hat richtig Spaß gemacht, das hier mal
# außer der Reihe zusammen zu basteln
# GLG
#
# PS: Wenn du mein Programm benutzt wird es
# bei FS auf mein Profil gehen und
# "Ich kenne Sebastian" klicken, da es keine
# Freundeslisten hat die man einsehen könnte
# oder etwas Ähnliches in der Art, gibt es somit
# auch keinerlei Implikationen, weshalb ich
# dies als den adäquaten  Weg gewählt habe
# um ungefähr nachvollziehen zu können,
# wie viele Leute denn in etwa mein Programm
# verwenden. Schließlich möchte ich wisse
# ob weitere Verbesserungen wirklich benötigt
# werden, oder ob ich die ganze Anstrengung
# nur für eine Hand voll Leute unternehme.
# PPS: Ich hasse es grafische Benutzeroberflächen
# programmieren zu müssen!!!
# Ich komme aus einer völlig anderen Ecke,
# die nicht mal zur Anwendungsentwicklung gehört,
# also sehe mir meinem Minimalismus diesbezüglich bitte nach!!! :D ;)
#
#
#
# '''

def cancel():
    return "Nichts wie weg hier"