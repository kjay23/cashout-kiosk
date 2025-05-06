import sys
import os
import serial
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer

class KioskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kiosk App")
        self.showFullScreen()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.stackedWidget = QStackedWidget()

        self.selected_amount = None
        self.amount_buttons = {}
        self.qr_code_labels = {
            20: "~/Pictures/qrcode_20.png",
            40: "~/Pictures/qrcode_40.png",
            60: "~/Pictures/qrcode_60.png",
            80: "~/Pictures/qrcode_80.png",
            100: "~/Pictures/qrcode_100.png"
        }

        # Serial connection to the Arduino
        self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Update with your actual Arduino port

        self.create_main_page()
        self.create_page_2()
        self.create_page_3()
        self.create_page_4()

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.stackedWidget)

    def create_main_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Welcome to the Kiosk", page)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("titleLabel")

        next_button = QPushButton("Next", page)
        next_button.setObjectName("navButton")
        next_button.setFixedSize(150, 60)
        next_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        layout.addWidget(label)
        layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(next_button, alignment=Qt.AlignRight)
        layout.addLayout(button_layout)

        self.stackedWidget.addWidget(page)

    def create_page_2(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Select the amount to cash out", page)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("titleLabel")

        amounts = [20, 40, 60, 80, 100]
        for amount in amounts:
            btn = QPushButton(f"{amount} PHP", page)
            btn.setFixedSize(200, 60)
            btn.setObjectName("amountButton")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, amt=amount: self.select_amount(amt))
            layout.addWidget(btn, alignment=Qt.AlignCenter)
            self.amount_buttons[amount] = btn

        layout.addStretch()

        button_layout = QHBoxLayout()

        prev_button = QPushButton("Previous", page)
        prev_button.setFixedSize(150, 60)
        prev_button.setObjectName("navButton")
        prev_button.clicked.connect(self.go_back_to_main)

        next_button = QPushButton("Next", page)
        next_button.setFixedSize(150, 60)
        next_button.setObjectName("navButton")
        next_button.clicked.connect(self.go_to_page_3)

        button_layout.addWidget(prev_button, alignment=Qt.AlignLeft)
        button_layout.addStretch()
        button_layout.addWidget(next_button, alignment=Qt.AlignRight)

        layout.addLayout(button_layout)
        self.stackedWidget.addWidget(page)

    def create_page_3(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.result_label = QLabel("Selected Amount: ", page)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setObjectName("titleLabel")
        layout.addWidget(self.result_label)

        layout.addStretch()

        button_layout = QHBoxLayout()
        prev_button = QPushButton("Previous", page)
        prev_button.setFixedSize(150, 60)
        prev_button.setObjectName("navButton")
        prev_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        next_button = QPushButton("Next", page)
        next_button.setFixedSize(150, 60)
        next_button.setObjectName("navButton")
        next_button.clicked.connect(self.go_to_page_4)

        button_layout.addWidget(prev_button, alignment=Qt.AlignLeft)
        button_layout.addStretch()
        button_layout.addWidget(next_button, alignment=Qt.AlignRight)

        layout.addLayout(button_layout)
        self.stackedWidget.addWidget(page)

    def create_page_4(self):
        page = QWidget()
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(page)

        label = QLabel("Please open GCash and scan the QR code to proceed.", page)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("titleLabel")
        layout.addWidget(label)
        layout.addWidget(self.qr_label)
        layout.addStretch()

        button_layout = QHBoxLayout()
        abort_button = QPushButton("Abort", page)
        abort_button.setFixedSize(150, 60)
        abort_button.setObjectName("abortButton")
        abort_button.clicked.connect(self.abort_transaction)

        button_layout.addWidget(abort_button, alignment=Qt.AlignLeft)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.stackedWidget.addWidget(page)

    def select_amount(self, amount):
        self.selected_amount = amount
        for amt, btn in self.amount_buttons.items():
            btn.setChecked(amt == amount)

    def go_to_page_3(self):
        if self.selected_amount:
            charge = {20: 2, 40: 3, 60: 4, 80: 4, 100: 5}.get(self.selected_amount, 0)
            total = self.selected_amount + charge
            self.result_label.setText(
                f"Selected Amount: {self.selected_amount} PHP\n"
                f"Service Charge: {charge} PHP\n"
                f"Total: {total} PHP"
            )
            self.stackedWidget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Selection Required", "Please choose an amount to continue.")

    def go_to_page_4(self):
        qr_code_path = os.path.expanduser(self.qr_code_labels.get(self.selected_amount, ""))
        if os.path.exists(qr_code_path):
            pixmap = QPixmap(qr_code_path)
            self.qr_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        else:
            self.qr_label.setText("QR code not found!")
        self.stackedWidget.setCurrentIndex(3)

        # Send the dispensing command to Arduino
        if self.selected_amount:
            self.dispense_coins(self.selected_amount)

    def dispense_coins(self, amount):
        coin_map = {20: 1, 40: 2, 60: 3, 80: 4, 100: 5}
        num_coins = coin_map.get(amount, 0)

        # Send the number of coins to Arduino to dispense
        if num_coins > 0:
            self.arduino.write(f"{num_coins}\n".encode())  # Send coin count to Arduino

        # Simulate success for 3 seconds
        QTimer.singleShot(3000, self.go_back_to_main)

    def go_back_to_main(self):
        self.selected_amount = None
        for btn in self.amount_buttons.values():
            btn.setChecked(False)
        self.stackedWidget.setCurrentIndex(0)

    def abort_transaction(self):
        self.go_back_to_main()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ Apply Light Gradient Theme
    app.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                                        stop:0 rgba(255, 255, 255, 1),
                                        stop:1 rgba(200, 230, 255, 1));
        }
        QLabel#titleLabel {
            color: #333;
            font-size: 24px;
            font-weight: bold;
            padding: 15px;
        }
        QLabel#errorLabel {
            color: red;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
        }
        QPushButton#navButton {
            background-color: #0078D7;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 15px;
        }
        QPushButton#navButton:pressed {
            background-color: #005A9C;
        }
        QPushButton#amountButton {
            background-color: #34a853;
            color: white;
            font-size: 20px;
            border-radius: 10px;
            padding: 20px;
        }
        QPushButton#amountButton:checked {
            background-color: #0078D7;
        }
        QPushButton#abortButton {
            background-color: red;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 15px;
        }
        QPushButton#abortButton:pressed {
            background-color: darkred;
        }
    """)

    window = KioskApp()
    window.show()

    sys.exit(app.exec())
