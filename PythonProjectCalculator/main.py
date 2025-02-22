import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout

class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 400, 500)  #Dimensiuni fereastra mai mari

        #Seteaza fundalul ferestrei principale pe un gri deschis
        self.setStyleSheet("background-color: #f5f5f5;")  # Fundal gri deschis pentru întreaga fereastra

        #Layout principal
        self.main_layout = QVBoxLayout()

        #Layout pentru butoanele de sus (Resetare si Inchidere)
        self.top_layout = QHBoxLayout()

        #Butonul de resetare C - coltul din dreapta sus
        self.reset_button = QPushButton("C", self)
        self.reset_button.setFixedSize(60, 60)
        self.reset_button.setStyleSheet("font-size: 20px; background-color: #4A90E2; color: white;")
        self.reset_button.clicked.connect(self.on_reset_click)

        #Butonul de închidere "Turn Off" - coltul din stânga sus
        self.close_button = QPushButton("Turn Off", self)
        self.close_button.setFixedSize(80, 60)
        self.close_button.setStyleSheet("font-size: 16px; background-color: #4A90E2; color: white;")
        self.close_button.clicked.connect(self.close)

        #AAdauga butoanele in layout-ul de sus
        self.top_layout.addWidget(self.close_button)
        self.top_layout.addStretch(1)  #Pune un spatiu între butonul de închidere si butonul de resetare
        self.top_layout.addWidget(self.reset_button)

        #Layout pentru butoane de calcul
        self.grid_layout = QGridLayout()

        #Ecranul digital care va afisa rezultatele
        self.viewer = QLineEdit(self)
        self.viewer.setReadOnly(True)  # Ecranul este doar în citire
        self.viewer.setPlaceholderText("0")
        self.viewer.setFixedHeight(60)  # Mareste înaltimea display-ului
        self.viewer.setStyleSheet("font-size: 24px; background-color: #f0f0f0; color: black;")  #Mareste fontul

        #Variabile pentru a stoca valorile curente si operatiile
        self.current_value = ""
        self.first_number = None
        self.operator = None

        #Creaza butoanele pentru cifre si operatii
        self.create_buttons()

        #Adauga layout-ul de sus (cu butoanele Reset si Turn Off) si restul la main_layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.viewer)
        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)

    def create_buttons(self):
        """Creaza butoanele pentru cifre si operatii si le adauga la layout-ul grid."""

        #Butoane pentru cifre (0-9)
        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', '*',
            '0', '.', '=', '/'
        ]

        # Adauga butoanele intr-un QGridLayout
        row = 0
        col = 0
        for button in buttons:
            btn = QPushButton(button, self)
            btn.setFixedSize(80, 80)  # Mareste butoanele
            btn.setStyleSheet("font-size: 20px; background-color: #4A90E2; color: white;")  #Stilul pentru butoane
            btn.clicked.connect(self.on_button_click)
            self.grid_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_button_click(self):
        """Gestioneaza apasarea unui buton (cifra sau operator)."""
        clicked_button = self.sender()
        text = clicked_button.text()

        if text in '0123456789.':
            #Adauga cifre si punctul la valoarea curenta
            self.current_value += text
            self.viewer.setText(self.current_value)
        elif text in '+-*/':
            # Salveaza primul numar si operatorul ales
            if self.first_number is None:
                self.first_number = float(self.current_value) if self.current_value else 0
                self.operator = text
                self.current_value = ""
        elif text == '=':
            #Executa operatia si arata rezultatul
            if self.first_number is not None and self.operator and self.current_value:
                second_number = float(self.current_value)
                result = self.calculate(self.first_number, second_number, self.operator)
                self.viewer.setText(str(result))
                self.first_number = None
                self.operator = None
                self.current_value = ""
        elif text == 'C':
            #Reseteaza tot
            self.first_number = None
            self.operator = None
            self.current_value = ""
            self.viewer.setText("0")

    def on_reset_click(self):
        """Reseteaza tot la valorile initiale."""
        self.first_number = None
        self.operator = None
        self.current_value = ""
        self.viewer.setText("0")

    def calculate(self, num1, num2, operator):
        """Executa operatia aritmetica pe cele doua numere."""
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Error"
            return num1 / num2
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec_())