
from PyQt6 import QtCore, QtGui, QtWidgets

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

        # Label für das neue Fenster
        self.label = QtWidgets.QLabel("Das Produkt wurde erfolgreich erstellt!", self)
        self.label.setGeometry(150, 200, 1100, 100)  # Label positionieren und Größe festlegen
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; color: transparent; background-color: white;")

        # QTextBrowser hinzufügen
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(240, 450, 980, 106))
        self.textBrowser.setStyleSheet("font-size: 20px;")
        self.textBrowser.setText("Die Datei: ... befindet sich im Ordner ... diese musst du in die Industrie 4.0 Anlage einpflegen. Danach kannst es dann unter den Produktnamen den du deinen Produkt gegeben hast im System der Industrie 4.0 Anlage aufrufen.")

        # Zurück-Button hinzufügen
        self.backButton = QtWidgets.QPushButton("Zurück zum Hauptfenster", self)
        self.backButton.setGeometry(500, 720, 400, 40)
        self.backButton.clicked.connect(self.on_back_button_clicked)

        # ProgressBar hinzufügen
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(480, 300, 500, 60))
        self.progressBar.setMaximum(100)  # Maximaler Wert 100%
        self.progressBar.setValue(0)      # Startwert 0%

        # ProgressBar Einstellungen (in Millisekunden)
        self.progress_duration = 2000  # Gesamtzeit für den Fortschritt (z.B. 5000 ms = 5 Sekunden)
        self.progress_speed = 20      # Zeit in ms für jedes Schritt der ProgressBar (50ms für jedes Inkrement)

        # Timer
        self.progress_timer = QtCore.QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress_bar)

        # Den Timer direkt beim Erstellen starten
        self.start_progress_bar()

        # Texte basierend auf der ausgewählten Sprache festlegen
        self.set_language_text()


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

        # Wörterbuch für vordefinierte Begriffe
        self.predefined_words = {
            "Werkstück rot": "Vordefiniertes_Wort_Rot",
            "Workpiece red": "Vordefiniertes_Wort_Rot",
            "Werkstück schwarz": "Vordefiniertes_Wort_Schwarz",
            "Workpiece black": "Vordefiniertes_Wort_Schwarz",
            "Werkstück silber": "Vordefiniertes_Wort_Silber",
            "Workpiece silver": "Vordefiniertes_Wort_Silber",
            "Kappe montieren": "Vordefiniertes_Wort_Kappe",
            "Mount cap": "Vordefiniertes_Wort_Kappe",
            "Farbe kontrollieren": "Vordefiniertes_Wort_Farbe",
            "Check colour": "Vordefiniertes_Wort_Farbe",
            "nationaler Vertrieb": "Vordefiniertes_Wort_National",
            "national distribution": "Vordefiniertes_Wort_National",
            "internationaler Vertrieb": "Vordefiniertes_Wort_International",
            "international distribution": "Vordefiniertes_Wort_International",
        }

        # Sprachwechsel-ComboBox
        self.languageComboBox = QtWidgets.QComboBox(self)
        self.languageComboBox.setGeometry(QtCore.QRect(1150, 10, 120, 30))
        self.languageComboBox.addItem("Deutsch")
        self.languageComboBox.addItem("Englisch")
        self.languageComboBox.currentIndexChanged.connect(self.change_language)

        # Initialisierung der GUI-Komponenten
        self.setup_ui()
        self.apply_translations()

    def setup_ui(self):
        self.selected_language = self.language
        # Labels
        self.label_produkt_erstellen = QtWidgets.QLabel(self)
        self.label_produkt_erstellen.setGeometry(QtCore.QRect(500, 10, 550, 16))
        self.label_produkt_erstellen.setObjectName("Produkt-erstellen")
        self.label_produkt_erstellen.setStyleSheet("""font-size: 30px;  /* Größere Schrift *""")

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setGeometry(QtCore.QRect(500, 100, 89, 16))
        self.label_name.setObjectName("label")

        self.label_produkt_anzeige = QtWidgets.QLabel(self)
        self.label_produkt_anzeige.setGeometry(QtCore.QRect(320, 500, 89, 16))
        self.label_produkt_anzeige.setObjectName("Produkt :")

        self.label_produkt_beschreibung = QtWidgets.QLabel(self)
        self.label_produkt_beschreibung.setGeometry(QtCore.QRect(810, 100, 137, 16))
        self.label_produkt_beschreibung.setObjectName("label_2")

        self.label_stack_magazine = QtWidgets.QLabel(self)
        self.label_stack_magazine.setGeometry(QtCore.QRect(310, 300, 95, 16))
        self.label_stack_magazine.setObjectName("label_3")

        self.label_joining = QtWidgets.QLabel(self)
        self.label_joining.setGeometry(QtCore.QRect(660, 300, 44, 16))
        self.label_joining.setObjectName("label_4")

        self.label_sorting = QtWidgets.QLabel(self)
        self.label_sorting.setGeometry(QtCore.QRect(960, 300, 44, 16))
        self.label_sorting.setObjectName("label_5")

        # TextBrowser
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(260, 550, 980, 106))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet("""font-size: 20px;""")
        # Ursprüngliche Größe und Schriftgröße speichern
        self.original_textBrowser_geometry = QtCore.QRect(260, 550, 980, 106)  # Ursprüngliche Geometrie
        self.original_font_size = 20  # Ursprüngliche Schriftgröße


        # PushButtons
        # PushButton Produkt fertig
        self.pushButtonProduktFertig = QtWidgets.QPushButton(self)
        self.pushButtonProduktFertig.setGeometry(QtCore.QRect(540, 720, 400, 30))
        self.pushButtonProduktFertig.setObjectName("pushButtonProduktFertig")
        self.pushButtonProduktFertig.clicked.connect(self.on_pushButtonProduktFertig_clicked)
        # PushButton Eingaben verbessern
        self.pushButtonEingabeVerbessern = QtWidgets.QPushButton(self)
        self.pushButtonEingabeVerbessern.setGeometry(QtCore.QRect(420, 720, 221, 51))
        self.pushButtonEingabeVerbessern.setObjectName("pushButtonEingabenVerbessern")
        self.pushButtonEingabeVerbessern.setVisible(False)
        self.pushButtonEingabeVerbessern.clicked.connect(self.on_pushButtonEingabeVerbessern_clicked)
        # PushButton Produkt ausgeben
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


        # LineEdit
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(490, 160, 200, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("""font-size: 16px;""")

        # TextEdit
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(800, 160, 270, 77))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("""font-size: 16px;""")

        # ComboBox1 workpiece
        self.comboBox_workpiece = QtWidgets.QComboBox(self)
        self.comboBox_workpiece.setGeometry(QtCore.QRect(270, 330, 250, 32))
        self.comboBox_workpiece.setObjectName("comboBox_3")
        self.comboBox_workpiece.addItem("auswählen")
        self.comboBox_workpiece.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)
        self.comboBox_workpiece.addItem("Werkstück rot")  # release red workpiece
        self.comboBox_workpiece.addItem("Werkstück schwarz") # release black workpiece
        self.comboBox_workpiece.addItem("Werkstück silber") # release silver workpiece
        # ComboBox2 mount cap
        self.comboBox_mountCap = QtWidgets.QComboBox(self)
        self.comboBox_mountCap.setGeometry(QtCore.QRect(610, 330, 180, 32))
        self.comboBox_mountCap.setObjectName("comboBox_2")
        self.comboBox_mountCap.addItem("auswählen")
        self.comboBox_mountCap.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)
        self.comboBox_mountCap.addItem("-")
        self.comboBox_mountCap.addItem("Kappe montieren") # mount cap
        # ComboBox3 checkColour
        self.comboBox_checkColour = QtWidgets.QComboBox(self)
        self.comboBox_checkColour.setGeometry(QtCore.QRect(610, 390, 180, 50))
        self.comboBox_checkColour.setObjectName("comboBox_4")
        self.comboBox_checkColour.addItem("auswählen")
        self.comboBox_checkColour.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)
        self.comboBox_checkColour.addItem("-")
        self.comboBox_checkColour.addItem("Farbe kontrollieren") # check colour
        # ComboBox 4
        self.comboBox_distribution = QtWidgets.QComboBox(self)
        self.comboBox_distribution.setGeometry(QtCore.QRect(920, 330, 250, 32))
        self.comboBox_distribution.setObjectName("comboBox")
        self.comboBox_distribution.addItem("auswählen")
        self.comboBox_distribution.setItemData(0, 0, QtCore.Qt.ItemDataRole.UserRole - 1)  # Deaktiviert die Auswahl
        self.comboBox_distribution.addItem("nationaler Vertrieb") # national distribution
        self.comboBox_distribution.addItem("internationaler Vertrieb") # international distribution

        # Verbinde das TextChanged-Signal des lineEdit mit der Funktion
        self.lineEdit.textChanged.connect(self.update_textBrowser)
        self.textEdit.textChanged.connect(self.update_textBrowser)
        self.comboBox_distribution.currentTextChanged.connect(self.update_textBrowser)
        self.comboBox_workpiece.currentTextChanged.connect(self.update_textBrowser)
        self.comboBox_mountCap.currentTextChanged.connect(self.update_textBrowser)
        self.comboBox_checkColour.currentTextChanged.connect(self.update_textBrowser)

    def change_language(self):
        """Wechselt die Sprache der Anwendung."""
        selected_language = self.languageComboBox.currentText()
        self.language = "en" if selected_language == "Englisch" else "de"
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

    def setButtonColors(self, fertig_color, verbessern_color, ausgeben_color):
        """Setzt die Hintergrundfarben der Buttons."""
        self.pushButtonProduktFertig.setStyleSheet(f"background-color: {fertig_color};")
        self.pushButtonEingabeVerbessern.setStyleSheet(f"background-color: {verbessern_color};")
        self.pushButtonProduktAusgeben.setStyleSheet(f"background-color: {ausgeben_color};")

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

    def on_pushButtonProduktFertig_clicked(self):
        # Wenn 'Produkt fertig' gedrückt wird:
        # Überprüfen, ob alle Felder ausgefüllt sind
        if (self.lineEdit.text().strip() == "" or  # Name ist leer
                self.textEdit.toPlainText().strip() == "" or  # Beschreibung ist leer
                self.comboBox_workpiece.currentText() == "auswählen" or  # Kein Workpiece ausgewählt
                self.comboBox_distribution.currentText() == "auswählen" or  # Keine Distribution ausgewählt
                self.comboBox_mountCap.currentText() == "auswählen" or  # Kein Mount Cap ausgewählt
                self.comboBox_checkColour.currentText() == "auswählen"):  # Keine Farbe ausgewählt

            # Fehlermeldung anzeigen
            QtWidgets.QMessageBox.warning(
                None, "Fehler", "Alle Angaben müssen zuerst ausgefüllt werden!"
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

        # Ausgabe der vordefinierten Begriffe
        print(f"Produktname: {name}")
        print(f"Produktbeschreibung: {beschreibung}")

        # Ausgeben der vordefinierten Begriffe für jede Auswahl
        wp = self.predefined_words.get(workpiece, "Unbekannt")
        print(f"Werkstück: {wp}")

        mc = self.predefined_words.get(mountCap, "Unbekannt")
        print(f"Kappe montieren: {mc}")

        cc = self.predefined_words.get(checkColour, "Unbekannt")
        print(f"Farbe kontrollieren: {cc}")

        dist = self.predefined_words.get(distribution, "Unbekannt")
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

