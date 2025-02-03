

from PyQt6 import QtCore, QtGui, QtWidgets

### 2tes Window: (wenn Eingaben beim ersten Window bestätigt)
class AusgabeWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.language = self.main_window.get_selected_language()  # Get the current language
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Produkt Ausgeben")
        # Speichern des übergebenen MainWindow-Objekts
        self.main_window = main_window

### Logo-SBS oben links Logo
        # Label Logo SBS
        self.Label_SBSlogo = QtWidgets.QLabel(self)
        self.Label_SBSlogo.setGeometry(QtCore.QRect(220, 12, 150, 150))
        self.Label_SBSlogo.setObjectName("label_6")

        # Lade das Bild und skaliere es
        pixmap = QtGui.QPixmap("SBSlogo.jpeg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(230, 130, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.Label_SBSlogo.setPixmap(pixmap)
            self.Label_SBSlogo.setScaledContents(False)
        else:
            print("Fehler: Bild 'SBSlogo.jpeg' konnte nicht geladen werden.")

### Logo-Quickload oben links Logo
        # Label Logo QuickLoad
        self.Label_QuickLoad = QtWidgets.QLabel(self)
        self.Label_QuickLoad.setGeometry(QtCore.QRect(12, 12, 150, 150))
        self.Label_QuickLoad.setObjectName("label_7")

        # Lade das Bild und skaliere es
        pixmap = QtGui.QPixmap("QuickLoad.jpg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(230, 130, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.Label_QuickLoad.setPixmap(pixmap)
            self.Label_QuickLoad.setScaledContents(False)
        else:
            print("Fehler: Bild 'QuickLoad.jpg' konnte nicht geladen werden.")

### Schriftzug (mitte) erst nach ablauf progressbar(Ladezeile) sichtbar
        # Label für das neue Fenster
        self.label = QtWidgets.QLabel("Das Produkt wurde erfolgreich erstellt!", self)
        self.label.setGeometry(150, 200, 1100, 100)  # Label positionieren und Größe festlegen
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; color: transparent; background-color: white;")

### Kästchen (mitte) mit Schriftinhalt (Beschreibung Ordner)
        # QTextBrowser hinzufügen
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(240, 450, 980, 106))
        self.textBrowser.setStyleSheet("font-size: 20px;")
        self.textBrowser.setText("Die Datei: ... befindet sich im Ordner ... diese musst du in die Industrie 4.0 Anlage einpflegen. Danach kannst es dann unter den Produktnamen den du deinen Produkt gegeben hast im System der Industrie 4.0 Anlage aufrufen.")

### Zurück-Button (unten)
        # Zurück-Button hinzufügen
        self.backButton = QtWidgets.QPushButton("Zurück zum Hauptfenster", self)
        self.backButton.setGeometry(500, 720, 400, 40)
        self.backButton.clicked.connect(self.on_back_button_clicked)

### Ladezeile (mitte) läuft nach öffnen dieses Windows durch
        # ProgressBar hinzufügen
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(480, 300, 500, 60))
        self.progressBar.setMaximum(100)  # Maximaler Wert 100%
        self.progressBar.setValue(0)      # Startwert 0%

        # ProgressBar Einstellungen (in Millisekunden)
        self.progress_duration = 1600  # Gesamtzeit für den Fortschritt (z.B. 5000 ms = 5 Sekunden)
        self.progress_speed = 13      # Zeit in ms für jedes Schritt der ProgressBar (50ms für jedes Inkrement)

        # Timer
        self.progress_timer = QtCore.QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress_bar)

        # Den Timer direkt beim Erstellen starten
        self.start_progress_bar()

        # Texte basierend auf der ausgewählten Sprache festlegen
        self.set_language_text()

### für Sprachausgabe (Text ändern in ausgewählte Sprache vom Window davor)
    def set_language_text(self):
        """Setzt die Texte für die Benutzeroberfläche basierend auf der Sprache."""
        # Übernehmen der Spracheinstellung aus dem main_window
        language = self.main_window.get_selected_language()  # Beispielmethode, um die ausgewählte Sprache zu holen

        if language == 'de':  # Deutsch
            self.setWindowTitle("Produkt Ausgeben")
            self.label.setText("Das Produkt wurde erfolgreich erstellt!")
            self.textBrowser.setText(
                "Die Datei: ... befindet sich im Ordner ... diese musst du in die Industrie 4.0 Anlage einpflegen. "
                "Danach kannst es dann unter den Produktnamen, den du deinem Produkt gegeben hast, im System der Industrie 4.0 Anlage aufrufen."
            )
            self.backButton.setText("Zurück zum Hauptfenster")
        else:  # Fallback auf Englisch
            self.setWindowTitle("Product Output")
            self.label.setText("The product has been successfully created!")
            self.textBrowser.setText(
                "The file: ... is located in the folder ... you need to upload this to the Industry 4.0 system. "
                "After that, you can call it under the product name you have given to your product in the Industry 4.0 system."
            )
            self.backButton.setText("Back to Main Window")

    def on_back_button_clicked(self):
        """Wird ausgeführt, wenn der 'Zurück'-Button gedrückt wird."""
        # Schließe das AusgabeWindow
        self.close()

        # "Zurücksetzen" des MainWindow: Setze Felder und Zustände zurück
        self.main_window.reset_main_window()

        # Zeige das MainWindow erneut
        self.main_window.show()

### Ladezeile start
    def start_progress_bar(self):
        """Startet die ProgressBar und setzt den Timer"""
        self.progressBar.setValue(0)      # Setze den Fortschritt auf 0
        self.progress_timer.start(self.progress_speed)  # Timer mit der festgelegten Geschwindigkeit starten

    def update_progress_bar(self):
        """Aktualisiert die Fortschrittsanzeige"""
        current_value = self.progressBar.value()
        if current_value < 100:
            self.progressBar.setValue(current_value + 1)  # Erhöhe den Fortschritt
        else:
            self.progress_timer.stop()  # Stoppe den Timer, wenn 100 erreicht wurde
            self.progressBar.setVisible(False)  # Mache die ProgressBar unsichtbar

            # Ändere die Schriftfarbe des Labels zu grün
            self.label.setStyleSheet("font-size: 30px; color: green; background-color: white;")


### Hauptfenster (Start Window)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Produkt Industrie 4.0 Anlage erstellen")
        self.setGeometry(100, 100, 1284, 451)

        # Sprachdaten als Wörterbuch
        self.translations = {
            "de": {
                "window_title": "Produkt Industrie 4.0 Anlage erstellen",
                "produkt_erstellen": "Produkt Industrie 4.0 Anlage erstellen:",
                "produktname": "Produktname:",
                "sprachauswahl": "Language selection",
                "produktbeschreibung": "Produktbeschreibung:",
                "werkstückauswahl": "Werkstückauswahl",
                "zusatzauswahl": "Zusatzauswahl",
                "sortierungsauswahl": "Sortierungsauswahl",
                "produkt_anzeige": "Produkt :",
                "button_fertig": "Produkt fertig",
                "button_ausgeben": "Produkt ausgeben",
                "button_verbessern": "Eingaben nochmal verbessern",
                "combo_auswählen": "auswählen",
                "combo_werkstück_rot": "Werkstück rot",
                "combo_werkstück_schwarz": "Werkstück schwarz",
                "combo_werkstück_silber": "Werkstück silber",
                "combo_kappe": "Kappe montieren",
                "combo_kontrolle": "Farbe kontrollieren",
                "combo_vertrieb_national": "nationaler Vertrieb",
                "combo_vertrieb_international": "internationaler Vertrieb",
            },
            "en": {
                "window_title": "Create Product Industry 4.0 System",
                "produkt_erstellen": "Create Product Industry 4.0 System:",
                "produktname": "Product Name:",
                "sprachauswahl": "Language selection",
                "produktbeschreibung": "Product Description:",
                "werkstückauswahl": "Workpiece Selection",
                "zusatzauswahl": "Additional Selection",
                "sortierungsauswahl": "Sorting Selection",
                "produkt_anzeige": "Product:",
                "button_fertig": "Finish Product",
                "button_ausgeben": "Output Product",
                "button_verbessern": "Edit Inputs Again",
                "combo_auswählen": "select",
                "combo_werkstück_rot": "Red Workpiece",
                "combo_werkstück_schwarz": "Black Workpiece",
                "combo_werkstück_silber": "Silver Workpiece",
                "combo_kappe": "Mount Cap",
                "combo_kontrolle": "Check Color",
                "combo_vertrieb_national": "National Distribution",
                "combo_vertrieb_international": "International Distribution",
            }
        }
        self.language = "de"  # Standard-Sprache: Deutsch

### Ausgabe am Ende (für XML)
        # Wörterbuch für vordefinierte Begriffe
        self.predefined_words = {
            "Werkstück rot": "release red workpiece",
            "Red Workpiece": "release red workpiece",
            "Werkstück schwarz": "release black workpiece",
            "Black Workpiece": "release black workpiece",
            "Werkstück silber": "release silver workpiece",
            "Silver Workpiece": "release silver workpiece",
            "Kappe montieren": "mount cap",
            "Mount Cap": "mount cap",
            "Farbe kontrollieren": "check colour",
            "Check Color": "check colour",
            "nationaler Vertrieb": "national distribution",
            "National Distribution": "national distribution",
            "internationaler Vertrieb": "international distribution",
            "International Distribution": "international distribution",
        }

### Sprachauswahl Combobox (rechts oben)
        # Sprachwechsel-ComboBox
        self.languageComboBox = QtWidgets.QComboBox(self)
        self.languageComboBox.setGeometry(QtCore.QRect(1120, 50, 120, 30))
        self.languageComboBox.addItem("Deutsch")
        self.languageComboBox.addItem("English")
        self.languageComboBox.currentIndexChanged.connect(self.change_language)

        # Initialisierung der GUI-Komponenten
        self.setup_ui()
        self.apply_translations()

    def setup_ui(self):
        self.selected_language = self.language

### Die Überschriften die über den dazugehörigen Feldern stehen
        # Labels
        # Produkt erstellen
        self.label_produkt_erstellen = QtWidgets.QLabel(self)
        self.label_produkt_erstellen.setGeometry(QtCore.QRect(500, 10, 550, 16))
        self.label_produkt_erstellen.setObjectName("Produkt-erstellen")
        self.label_produkt_erstellen.setStyleSheet("""font-size: 30px;  /* Größere Schrift *""")
        # Produktname
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setGeometry(QtCore.QRect(500, 100, 89, 16))
        self.label_name.setObjectName("label")
        # Produkt
        self.label_produkt_anzeige = QtWidgets.QLabel(self)
        self.label_produkt_anzeige.setGeometry(QtCore.QRect(320, 500, 89, 16))
        self.label_produkt_anzeige.setObjectName("Produkt :")
        # Produkt Beschreibung
        self.label_produkt_beschreibung = QtWidgets.QLabel(self)
        self.label_produkt_beschreibung.setGeometry(QtCore.QRect(810, 100, 137, 16))
        self.label_produkt_beschreibung.setObjectName("label_2")
        # Spracheauswahl
        self.label_spracheauswahl = QtWidgets.QLabel(self)
        self.label_spracheauswahl.setGeometry(QtCore.QRect(1140, 30, 89, 16))
        self.label_spracheauswahl.setObjectName("spracheauswahl")
        # Werkstückauswahl
        self.label_stack_magazine = QtWidgets.QLabel(self)
        self.label_stack_magazine.setGeometry(QtCore.QRect(310, 300, 95, 16))
        self.label_stack_magazine.setObjectName("label_3")
        # Zusatzauswahl
        self.label_joining = QtWidgets.QLabel(self)
        self.label_joining.setGeometry(QtCore.QRect(660, 300, 44, 16))
        self.label_joining.setObjectName("label_4")
        # Sortierungsauswahl
        self.label_sorting = QtWidgets.QLabel(self)
        self.label_sorting.setGeometry(QtCore.QRect(960, 300, 44, 16))
        self.label_sorting.setObjectName("label_5")
### Kästchen (mitte) anzeige ausgewählte
        # TextBrowser
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(260, 550, 980, 106))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet("""font-size: 20px;""")
        # Ursprüngliche Größe und Schriftgröße speichern
        self.original_textBrowser_geometry = QtCore.QRect(260, 550, 980, 106)  # Ursprüngliche Geometrie
        self.original_font_size = 20  # Ursprüngliche Schriftgröße


### PushButtons
        # PushButton Produkt fertig
        self.pushButtonProduktFertig = QtWidgets.QPushButton(self)
        self.pushButtonProduktFertig.setGeometry(QtCore.QRect(540, 720, 400, 30))
        self.pushButtonProduktFertig.setObjectName("pushButtonProduktFertig")
        self.pushButtonProduktFertig.clicked.connect(self.on_pushButtonProduktFertig_clicked)
        # PushButton Eingaben verbessern (erst sichtbar wenn Produkt fertig gedrückt)
        self.pushButtonEingabeVerbessern = QtWidgets.QPushButton(self)
        self.pushButtonEingabeVerbessern.setGeometry(QtCore.QRect(420, 720, 221, 51))
        self.pushButtonEingabeVerbessern.setObjectName("pushButtonEingabenVerbessern")
        self.pushButtonEingabeVerbessern.setVisible(False)
        self.pushButtonEingabeVerbessern.clicked.connect(self.on_pushButtonEingabeVerbessern_clicked)
        # PushButton Produkt ausgeben (erst sichtbar wenn Produkt fertig gedrückt)
        self.pushButtonProduktAusgeben = QtWidgets.QPushButton(self)
        self.pushButtonProduktAusgeben.setGeometry(QtCore.QRect(780, 720, 100, 30))
        self.pushButtonProduktAusgeben.setObjectName("pushButtonProduktAusgeben")
        self.pushButtonProduktAusgeben.setVisible(False)
        self.pushButtonProduktAusgeben.clicked.connect(self.on_pushButtonProduktAusgeben_clicked)
        # Button hintergrund Farben setzen
        self.setButtonColors(
            fertig_color="lightgreen",
            verbessern_color="lightcoral",
            ausgeben_color="lightgreen"
        )

### Logo-SBS oben links Logo
        # Label Logo SBS
        self.Label_SBSlogo = QtWidgets.QLabel(self)
        self.Label_SBSlogo.setGeometry(QtCore.QRect(220, 12, 150, 150))
        self.Label_SBSlogo.setObjectName("label_6")

        # Lade das Bild und skaliere es
        pixmap = QtGui.QPixmap("SBSlogo.jpeg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(230, 130, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.Label_SBSlogo.setPixmap(pixmap)
            self.Label_SBSlogo.setScaledContents(False)
        else:
            print("Fehler: Bild 'SBSlogo.jpeg' konnte nicht geladen werden.")

### Logo-Quickload oben links Logo
        # Label Logo QuickLoad
        self.Label_QuickLoad = QtWidgets.QLabel(self)
        self.Label_QuickLoad.setGeometry(QtCore.QRect(12, 12, 150, 150))
        self.Label_QuickLoad.setObjectName("label_7")

        # Lade das Bild und skaliere es
        pixmap = QtGui.QPixmap("QuickLoad.jpg")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(230, 130, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.Label_QuickLoad.setPixmap(pixmap)
            self.Label_QuickLoad.setScaledContents(False)
        else:
            print("Fehler: Bild 'QuickLoad.jpg' konnte nicht geladen werden.")

### Eingabekästchen für Produkt name
        # LineEdit
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(490, 160, 200, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("""font-size: 16px;""")

### Eingabefeld für Produkt Beschreibung
        # TextEdit
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(800, 160, 270, 77))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("""font-size: 16px;""")

### Die Auswahl Comboboxen
        # ComboBox1 Werkstückauswahl (workpiece)
        self.comboBox_workpiece = QtWidgets.QComboBox(self)
        self.comboBox_workpiece.setGeometry(QtCore.QRect(270, 330, 250, 32))
        self.comboBox_workpiece.setObjectName("comboBox_3")
        self.comboBox_workpiece.addItem("auswählen")
        self.comboBox_workpiece.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)
        self.comboBox_workpiece.addItem("Werkstück rot")  # release red workpiece
        self.comboBox_workpiece.addItem("Werkstück schwarz") # release black workpiece
        self.comboBox_workpiece.addItem("Werkstück silber") # release silver workpiece
        # ComboBox2 Kappe montieren (mount cap)
        self.comboBox_mountCap = QtWidgets.QComboBox(self)
        self.comboBox_mountCap.setGeometry(QtCore.QRect(610, 330, 180, 32))
        self.comboBox_mountCap.setObjectName("comboBox_2")
        self.comboBox_mountCap.addItem("auswählen")
        self.comboBox_mountCap.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)
        self.comboBox_mountCap.addItem("-")
        self.comboBox_mountCap.addItem("Kappe montieren") # mount cap
        # ComboBox3 Farbe kontrollieren (checkColour)
        self.comboBox_checkColour = QtWidgets.QComboBox(self)
        self.comboBox_checkColour.setGeometry(QtCore.QRect(610, 390, 180, 50))
        self.comboBox_checkColour.setObjectName("comboBox_4")
        self.comboBox_checkColour.addItem("auswählen")
        self.comboBox_checkColour.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)
        self.comboBox_checkColour.addItem("-")
        self.comboBox_checkColour.addItem("Farbe kontrollieren") # check colour
        # ComboBox 4 Sortierungsauswahl (Sorting)
        self.comboBox_distribution = QtWidgets.QComboBox(self)
        self.comboBox_distribution.setGeometry(QtCore.QRect(920, 330, 250, 32))
        self.comboBox_distribution.setObjectName("comboBox")
        self.comboBox_distribution.addItem("auswählen")
        self.comboBox_distribution.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)  # Deaktiviert die Auswahl
        self.comboBox_distribution.addItem("nationaler Vertrieb") # national distribution
        self.comboBox_distribution.addItem("internationaler Vertrieb") # international distribution

### Textzfeld (unten) die eingegebenen, ausgewählten Werte darstellen in der ausgewählten Sprache
        # Verbinde das TextChanged-Signal des lineEdit mit der Funktion
        self.lineEdit.textChanged.connect(self.update_textBrowser)
        self.textEdit.textChanged.connect(self.update_textBrowser)
        self.comboBox_distribution.currentTextChanged.connect(self.update_textBrowser)
        self.comboBox_workpiece.currentTextChanged.connect(self.update_textBrowser)
        self.comboBox_mountCap.currentTextChanged.connect(self.update_textBrowser)
        self.comboBox_checkColour.currentTextChanged.connect(self.update_textBrowser)

### Rote linien unter nicht ausgefüllten Eingaben/Auswahl bei Weiter(Produkt fertig) klickt
        # Rote Linie Produktname
        self.line_red_Produktname = QtWidgets.QFrame(self)
        self.line_red_Produktname.setGeometry(490, 190, 200, 3)
        self.line_red_Produktname.setStyleSheet("background-color: red;")
        self.line_red_Produktname.setVisible(False)  # Zunächst nicht sichtbar
        # Rote Linie Produkbeschreibung
        self.line_red_Produktbeschreibung = QtWidgets.QFrame(self)
        self.line_red_Produktbeschreibung.setGeometry(800, 240, 270, 3)
        self.line_red_Produktbeschreibung.setStyleSheet("background-color: red;")
        self.line_red_Produktbeschreibung.setVisible(False)  # Zunächst nicht sichtbar
        # Rote Linie Werkstückauswahl
        self.line_red_workpiece = QtWidgets.QFrame(self)
        self.line_red_workpiece.setGeometry(280, 383, 230, 3)
        self.line_red_workpiece.setStyleSheet("background-color: red;")
        self.line_red_workpiece.setVisible(False)  # Zunächst nicht sichtbar
        # Rote Linie Sortierungsauswahl
        self.line_red_distributation = QtWidgets.QFrame(self)
        self.line_red_distributation.setGeometry(930, 383, 230, 3)
        self.line_red_distributation.setStyleSheet("background-color: red;")
        self.line_red_distributation.setVisible(False)  # Zunächst nicht sichtbar
        # Rote Linie Kappe montieren
        self.line_red_mountCap = QtWidgets.QFrame(self)
        self.line_red_mountCap.setGeometry(620, 383, 210, 3)
        self.line_red_mountCap.setStyleSheet("background-color: red;")
        self.line_red_mountCap.setVisible(False)  # Zunächst nicht sichtbar
        # Rote Linie Farbe kontrollieren
        self.line_red_checkColour = QtWidgets.QFrame(self)
        self.line_red_checkColour.setGeometry(620, 443, 210, 3)
        self.line_red_checkColour.setStyleSheet("background-color: red;")
        self.line_red_checkColour.setVisible(False)  # Zunächst nicht sichtbar

    ### Sprach änderung (Deutsch, Englisch)
    def change_language(self):
        """Wechselt die Sprache der Anwendung."""
        selected_language = self.languageComboBox.currentText()
        self.language = "en" if selected_language == "English" else "de"
        self.selected_language = self.language  # Update the selected_language attribute
        self.apply_translations()

    def get_selected_language(self):
        """Gibt die aktuell ausgewählte Sprache zurück."""
        return self.selected_language

    def apply_translations(self):
        """Setzt die Übersetzungen auf alle UI-Komponenten."""
        t = self.translations[self.language]
        self.setWindowTitle(t["window_title"])
        self.label_produkt_erstellen.setText(t["produkt_erstellen"])
        self.label_name.setText(t["produktname"])
        self.label_spracheauswahl.setText(t["sprachauswahl"])
        self.label_produkt_beschreibung.setText(t["produktbeschreibung"])
        self.label_stack_magazine.setText(t["werkstückauswahl"])
        self.label_joining.setText(t["zusatzauswahl"])
        self.label_sorting.setText(t["sortierungsauswahl"])
        self.label_produkt_anzeige.setText(t["produkt_anzeige"])
        self.pushButtonProduktFertig.setText(t["button_fertig"])
        self.pushButtonProduktAusgeben.setText(t["button_ausgeben"])
        self.pushButtonEingabeVerbessern.setText(t["button_verbessern"])

        # ComboBox-Inhalte aktualisieren
        self.comboBox_workpiece.clear()
        self.comboBox_workpiece.addItems([
            t["combo_auswählen"], t["combo_werkstück_rot"],
            t["combo_werkstück_schwarz"], t["combo_werkstück_silber"]
        ])

        self.comboBox_mountCap.clear()
        self.comboBox_mountCap.addItems([t["combo_auswählen"], "-", t["combo_kappe"]])

        self.comboBox_checkColour.clear()
        self.comboBox_checkColour.addItems([t["combo_auswählen"], "-", t["combo_kontrolle"]])

        self.comboBox_distribution.clear()
        self.comboBox_distribution.addItems([
            t["combo_auswählen"], t["combo_vertrieb_national"], t["combo_vertrieb_international"]
        ])

### Hauptwindow zurücksetzten wenn Produktauswahl abgeschlossen ist (in Start zustand)
    def reset_main_window(self):
        """Setzt alle Felder und Widgets im MainWindow zurück."""
        # Setze alle Eingabefelder zurück
        self.lineEdit.clear()  # Beispiel für ein LineEdit zurücksetzen
        self.textEdit.clear()  # Beispiel für ein TextEdit zurücksetzen
        self.comboBox_workpiece.setCurrentIndex(0)  # Setze ComboBox zurück (erste Option)
        self.comboBox_mountCap.setCurrentIndex(0)
        self.comboBox_checkColour.setCurrentIndex(0)
        self.comboBox_distribution.setCurrentIndex(0)

        # Setze alle Buttons und andere Widgets zurück
        self.pushButtonProduktFertig.setVisible(True)
        self.pushButtonEingabeVerbessern.setVisible(False)
        self.pushButtonProduktAusgeben.setVisible(False)

        # Optional: Setze den Text im TextBrowser zurück
        self.textBrowser.clear()

        # Stelle sicher, dass alle Eingabefelder wieder aktiviert sind
        widgets_to_enable = [
            self.comboBox_distribution,
            self.comboBox_workpiece,
            self.comboBox_mountCap,
            self.comboBox_checkColour,
            self.lineEdit,
            self.textEdit,
        ]
        for widget in widgets_to_enable:
            widget.setEnabled(True)

        # Setze den TextBrowser auf die ursprüngliche Größe und Schriftgröße zurück
        self.textBrowser.setGeometry(self.original_textBrowser_geometry)  # Setze die ursprüngliche Geometrie
        self.textBrowser.setStyleSheet(f"font-size: {self.original_font_size}px;")  # Setze die ursprüngliche Schriftgröße

    def setButtonColors(self, fertig_color, verbessern_color, ausgeben_color):
        """Setzt die Hintergrundfarben der Buttons."""
        self.pushButtonProduktFertig.setStyleSheet(f"background-color: {fertig_color};")
        self.pushButtonEingabeVerbessern.setStyleSheet(f"background-color: {verbessern_color};")
        self.pushButtonProduktAusgeben.setStyleSheet(f"background-color: {ausgeben_color};")

### In das Textfeld (unten) die eingegebenen, ausgewählten Werte darstellen in der ausgewählten Sprache
    def update_textBrowser(self):
        """Aktualisiert den Inhalt des TextBrowsers mit den aktuellen Werten."""
        name = self.lineEdit.text().strip()
        beschreibung = self.textEdit.toPlainText().strip()

        # Hole die aktuellen ComboBox-Werte
        workpiece = self.comboBox_workpiece.currentText()
        mountCap = self.comboBox_mountCap.currentText()
        checkColour = self.comboBox_checkColour.currentText()
        distribution = self.comboBox_distribution.currentText()

        # Definiere Platzhalterwerte, die ignoriert werden sollen
        placeholders = {"auswählen", "-", "select"}

        # Bereite den Anzeigetext vor
        display_text = []

        if name:
            display_text.append(f"{name}: ")
        if workpiece not in placeholders:
            display_text.append(f"  {workpiece},")
        if mountCap not in placeholders:
            display_text.append(f"  {mountCap},")
        if checkColour not in placeholders:
            display_text.append(f"  {checkColour},")
        if distribution not in placeholders:
            display_text.append(f"  {distribution}")

        # Beschreibung in einer neuen Zeile hinzufügen
        if beschreibung:
            display_text.append(f"\n ")
            display_text.append(f"\n{beschreibung}")

        # Setze den Text im TextBrowser
        self.textBrowser.setText("".join(display_text))

        # Setze die Schriftfarbe der ComboBoxes
        self.set_combobox_color(self.comboBox_workpiece)
        self.set_combobox_color(self.comboBox_mountCap)
        self.set_combobox_color(self.comboBox_checkColour)
        self.set_combobox_color(self.comboBox_distribution)

        # Sichtbarkeit der roten Linien basierend auf Eingabewerten aktualisieren
        self.update_error_lines()

### Funktion: Rote linien unter nicht ausgefüllten Eingaben/Auswahl bei Weiter(Produkt fertig) klickt
    def set_combobox_color(self, comboBox):
        """Setzt die Schriftfarbe für bestimmte Einträge in der ComboBox."""
        # Stelle sicher, dass die ComboBox die richtigen Einträge hat
        for index in range(comboBox.count()):
            item_text = comboBox.itemText(index)
            # Überprüfe, ob der Text "auswählen" oder "select" ist
            if item_text in ["auswählen", "select"]:
                comboBox.setItemData(index, QtGui.QColor("red"), QtCore.Qt.ItemDataRole.ForegroundRole)  # Setzt die Schriftfarbe auf rot
            else:
                comboBox.setItemData(index, QtGui.QColor("black"), QtCore.Qt.ItemDataRole.ForegroundRole)  # Setzt die Schriftfarbe auf schwarz

    def update_error_lines(self):
        """Aktualisiert die Sichtbarkeit der roten Linien."""
        unselected_texts = ["auswählen", "select"]  # Füge hier weitere Sprachen hinzu, falls nötig

        # Sichtbarkeit der roten Linien basierend auf den Eingabewerten steuern
        if self.lineEdit.text().strip() != "":
            self.line_red_Produktname.setVisible(False)  # Unsichtbar machen, wenn gültig

        if self.textEdit.toPlainText().strip() != "":
            self.line_red_Produktbeschreibung.setVisible(False)  # Unsichtbar machen, wenn gültig

        if self.comboBox_workpiece.currentText().strip().lower() not in unselected_texts:
            self.line_red_workpiece.setVisible(False)  # Unsichtbar machen, wenn gültig

        if self.comboBox_distribution.currentText().strip().lower() not in unselected_texts:
            self.line_red_distributation.setVisible(False)  # Unsichtbar machen, wenn gültig

        if self.comboBox_mountCap.currentText().strip().lower() not in unselected_texts:
            self.line_red_mountCap.setVisible(False)  # Unsichtbar machen, wenn gültig

        if self.comboBox_checkColour.currentText().strip().lower() not in unselected_texts:
            self.line_red_checkColour.setVisible(False)  # Unsichtbar machen, wenn gültig

    def on_pushButtonProduktFertig_clicked(self):
        # Texte, die "auswählen" bedeuten, in verschiedenen Sprachen
        unselected_texts = ["auswählen", "select"]  # Füge hier weitere Sprachen hinzu, falls nötig

        # Überprüfen der ausgewählten Sprache
        selected_language = self.languageComboBox.currentText().strip().lower()  # Hier wird die ausgewählte Sprache ermittelt
        # Fehlernachricht basierend auf der Sprache
        if selected_language == "english":
            error_message = "All fields must be filled out first!"
        else:  # Standardmäßig Deutsch
            error_message = "Alle Angaben müssen zuerst ausgefüllt werden!"

        # Wenn 'Produkt fertig' gedrückt wird:
        # Wenn 'Produkt fertig' gedrückt wird:
        # Überprüfen, ob alle Felder ausgefüllt sind
        error_found = False

        if self.lineEdit.text().strip() == "":
            self.line_red_Produktname.setVisible(True)
            error_found = True
        else:
            self.line_red_Produktname.setVisible(False)

        if self.textEdit.toPlainText().strip() == "":
            self.line_red_Produktbeschreibung.setVisible(True)
            error_found = True
        else:
            self.line_red_Produktbeschreibung.setVisible(False)

        if self.comboBox_workpiece.currentText().strip().lower() in unselected_texts:
            self.line_red_workpiece.setVisible(True)
            error_found = True
        else:
            self.line_red_workpiece.setVisible(False)


        if self.comboBox_distribution.currentText().strip().lower() in unselected_texts:
            self.line_red_distributation.setVisible(True)
            error_found = True
        else:
            self.line_red_distributation.setVisible(False)

        if self.comboBox_mountCap.currentText().strip().lower() in unselected_texts:
            self.line_red_mountCap.setVisible(True)
            error_found = True
        else:
            self.line_red_mountCap.setVisible(False)

        if self.comboBox_checkColour.currentText().strip().lower() in unselected_texts:
            self.line_red_checkColour.setVisible(True)
            error_found = True
        else:
            self.line_red_checkColour.setVisible(False)

        if error_found:
            # Fehlermeldung anzeigen
            QtWidgets.QMessageBox.warning(
                None, "Fehler", error_message  # Verwenden Sie die dynamisch festgelegte Fehlermeldung
            )
        else:
            # Wenn alle Felder ausgefüllt sind, gehe weiter
            self.pushButtonProduktFertig.setVisible(False)
            self.pushButtonEingabeVerbessern.setVisible(True)
            self.pushButtonProduktAusgeben.setVisible(True)

            # Deaktivieren der Widgets
            widgets_to_disable = [
                self.comboBox_distribution,
                self.comboBox_workpiece,
                self.comboBox_mountCap,
                self.comboBox_checkColour,
                self.lineEdit,
                self.textEdit,
            ]
            for widget in widgets_to_disable:
                widget.setEnabled(False)

            self.pushButtonEingabeVerbessern.setEnabled(True)
            self.pushButtonProduktAusgeben.setEnabled(True)
            self.textBrowser.setEnabled(True)

            self.textBrowser.setGeometry(QtCore.QRect(180, 450, 1080, 230))
            self.textBrowser.setStyleSheet("""font-size: 30px;  /* Größere Schrift */""")

### Verbessern Button (zurück kann man nochmal Werte ändern)
    def on_pushButtonEingabeVerbessern_clicked(self):
        self.pushButtonProduktFertig.setVisible(True)

        self.pushButtonEingabeVerbessern.setVisible(False)
        self.pushButtonProduktAusgeben.setVisible(False)

        widgets_to_enable = [
            self.comboBox_distribution,
            self.comboBox_workpiece,
            self.comboBox_mountCap,
            self.comboBox_checkColour,
            self.lineEdit,
            self.textEdit,
        ]
        for widget in widgets_to_enable:
            widget.setEnabled(True)


        self.textBrowser.setGeometry(self.original_textBrowser_geometry)  # Ursprüngliche Geometrie wiederherstellen
        self.textBrowser.setStyleSheet(f"font-size: {self.original_font_size}px;")

### Produkt ausgeben (geht weiter auf das Zweite Window und gibt ausgewählte Daten mit (Code dazu am Anfang oben))
    def on_pushButtonProduktAusgeben_clicked(self):
        """Wird ausgeführt, wenn der Button 'Produkt ausgeben' geklickt wird."""

        # Hole die aktuellen Werte der Eingabefelder
        name = self.lineEdit.text().strip()
        beschreibung = self.textEdit.toPlainText().strip()

        # Hole die aktuellen ComboBox-Werte
        workpiece = self.comboBox_workpiece.currentText()
        mountCap = self.comboBox_mountCap.currentText()
        checkColour = self.comboBox_checkColour.currentText()
        distribution = self.comboBox_distribution.currentText()

### Gibt die Ausgewählten Werte aus (Feste Wörter pro Gegenstand egal welche Sprache ausgewählt ist für XML-Handling)
        # Ausgabe der vordefinierten Begriffe
        print(f"Produktname: {name}")
        print(f"Produktbeschreibung: {beschreibung}")

        # Ausgeben der vordefinierten Begriffe für jede Auswahl
        wp = self.predefined_words.get(workpiece, workpiece)
        print(f"Werkstück: {wp}")

        mc = self.predefined_words.get(mountCap, mountCap)
        print(f"Kappe montieren: {mc}")

        cc = self.predefined_words.get(checkColour, checkColour)
        print(f"Farbe kontrollieren: {cc}")

        dist = self.predefined_words.get(distribution, distribution)
        print(f"Vertrieb: {dist}")
        
        #########                     #######
        #########                     #######
        ######### ausgabe in XML Code #######
        ########                      #######

        # Öffne das neue Fenster (AusgabeWindow) und übergebe das MainWindow
        self.newWindow = AusgabeWindow(self)  # MainWindow wird übergeben
        self.newWindow.showFullScreen()  # Zeigt das Fenster im Vollbildmodus

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Stylesheet für die gesamte Anwendung anwenden
    app.setStyleSheet("""
        QLabel {
            font-size: 20px;
            min-height: 50px;
            min-width: 400px;
        }
        QPushButton {
            font-size: 20px;
            min-width: 300px;
            min-height: 100px;
        }
        QComboBox {
            font-size: 20px;
            min-width: 230px;
            min-height: 80px;
        }
    """)

    main_window = MainWindow()
    main_window.showFullScreen()
    sys.exit(app.exec())
