import threading
from PyQt5 import QtCore, QtWidgets, QtGui
import autoclicker

class HoverButton(QtWidgets.QPushButton):
    hovered = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enterEvent(self, event):
        self.hovered.emit()
        super().enterEvent(event)

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dragging = False
        self.drag_position = None

    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QtGui.QIcon("logofinal.ico"))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("""
            * {
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QMainWindow {
                background-color: #1e1e2f;
                color: #ffffff;
            }
            QPushButton {
                border-radius: 10px;
                font: bold 11pt "Segoe UI";
                background-color: #4a90e2;
                padding: 10px 15px;
                color: white;
            }
            QPushButton:hover {
                background-color: #3b78c2;
            }
            QPushButton:pressed {
                background-color: #2b5fae;
            }
            QFrame {
                background-color: #25273c;
                border-radius: 10px;
            }
            QLabel {
                font: 11pt "Segoe UI";
                color: #ffffff;
                background-color: transparent;
            }
            QStatusBar {
                background-color: #1e1e2f;
                color: white;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.title_label = QtWidgets.QLabel("Halfmoon v2.0", self.centralwidget)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            border: 1px dashed #4a90e2;
            border-radius: 10px;
        """)
        self.main_layout.addWidget(self.title_label)

        self.body_layout = QtWidgets.QHBoxLayout()
        self.body_layout.setSpacing(15)

        self.left_frame = QtWidgets.QFrame(self.centralwidget)
        self.left_frame.setMinimumWidth(220)
        self.left_frame.setStyleSheet("background-color: #2a2c3f;")
        self.left_layout = QtWidgets.QVBoxLayout(self.left_frame)
        self.left_layout.setContentsMargins(15, 15, 15, 15)
        self.left_layout.setSpacing(15)

        self.autoclickerbtn = HoverButton("Autoclicker", self.left_frame)
        self.autoclickerbtn.clicked.connect(self.autoclicker_run)
        self.left_layout.addWidget(self.autoclickerbtn)

        self.fastplacebtn = HoverButton("Fastplace", self.left_frame)
        self.fastplacebtn.clicked.connect(self.fastplace_run)
        self.left_layout.addWidget(self.fastplacebtn)

        self.autoblockbtn = HoverButton("Autoblock", self.left_frame)
        self.autoblockbtn.clicked.connect(self.autoblock_run)
        self.left_layout.addWidget(self.autoblockbtn)

        self.autoclickerbtn_2 = HoverButton("Clickassist", self.left_frame)
        self.autoclickerbtn_2.clicked.connect(self.clickassist_run)
        self.left_layout.addWidget(self.autoclickerbtn_2)

        self.body_layout.addWidget(self.left_frame)

        self.right_frame = QtWidgets.QFrame(self.centralwidget)
        self.right_layout = QtWidgets.QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(15, 15, 15, 15)
        self.right_layout.setSpacing(15)

        self.description_label = QtWidgets.QLabel("Hover over a button to view its details here.", self.right_frame)
        self.description_label.setAlignment(QtCore.Qt.AlignTop)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("""
            border: 1px solid #4a90e2;
            border-radius: 10px;
            padding: 15px;
            background-color: #1e1e2f;
        """)
        self.right_layout.addWidget(self.description_label)

        # Stylish Slider for Sleep Timer
        self.font_size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.right_frame)
        self.font_size_slider.setMinimum(1)
        self.font_size_slider.setMaximum(100)  # Maximum is now 100 to represent 0.01 - 0.1 second range
        self.font_size_slider.setValue(10)  # Start with 0.1 second
        self.font_size_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.font_size_slider.setTickInterval(1)
        self.font_size_slider.setStyleSheet("""
            QSlider {
                background-color: #2a2c3f;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background-color: #4a90e2;
                border-radius: 10px;
                width: 20px;
                margin: -5px 0;
            }
            QSlider::handle:horizontal:hover {
                background-color: #3b78c2;
            }
        """)
        self.font_size_slider.valueChanged.connect(self.updateSleepTimer)
        self.right_layout.addWidget(self.font_size_slider)

        self.cps_label = QtWidgets.QLabel("Sleep Timer: 0.10 seconds", self.right_frame)
        self.cps_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cps_label.setStyleSheet("""
            color: #ffffff;
            font-size: 14px;
            font-weight: bold;
            background-color: #2a2c3f;
            border: 1px solid #4a90e2;
            border-radius: 10px;
            padding: 5px;
        """)
        self.right_layout.addWidget(self.cps_label)

        self.body_layout.addWidget(self.right_frame)
        self.main_layout.addLayout(self.body_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.setupConnections()
        self.retranslateUi(MainWindow)

    def setupConnections(self):
        self.fastplacebtn.hovered.connect(
            lambda: self.showDescription("Fastplace", "Quickly places blocks faster than normal.\nPress M to turn on and N to turn off.")
        )
        self.autoblockbtn.hovered.connect(
            lambda: self.showDescription("Autoblock", "Automatically places blocks for protection.\nPress T to turn on and Y to turn off.")
        )
        self.autoclickerbtn.hovered.connect(
            lambda: self.showDescription("Autoclicker", "Automates mouse clicks for repetitive tasks.\nPress R to turn on and X to turn off.")
        )
        self.autoclickerbtn_2.hovered.connect(
            lambda: self.showDescription("Clickassist", "Enhances accuracy when clicking.\nPress N to turn on and M to turn off.")
        )

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Halfmoon v2.0")

    def showDescription(self, title, details):
        self.description_label.setText(f"<h2>{title}</h2><p>{details}</p>")

    def updateSleepTimer(self):
        sleep_time = self.font_size_slider.value() / 100  # Convert slider value to seconds
        self.cps_label.setText(f"Sleep Timer: {sleep_time:.2f} seconds")
        print(f"Sleep timer updated to: {sleep_time:.2f} seconds")
        autoclicker.update_sleep_time(sleep_time)  # Update sleep time in the autoclicker module

    def fastplace_run(self):
        threading.Thread(target=autoclicker.fastplace, daemon=True).start()

    def autoblock_run(self):
        threading.Thread(target=autoclicker.autoblock, daemon=True).start()

    def autoclicker_run(self):
        threading.Thread(target=autoclicker.autoclicker, daemon=True).start()

    def clickassist_run(self):
        threading.Thread(target=autoclicker.clickassist, daemon=True).start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
