from utils.QtCore import *

class CustomAddCoinBtn (QPushButton):
    def __init__(
        self
    ):
        super().__init__()

        self.setCursor(Qt.PointingHandCursor)
        self.setText('Add coin')
        self.setObjectName('add_coin_btn')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.setStyleSheet(f'''
            QPushButton {{
                margin-left: 20px;
                color: #777777;
                font: 600 12pt "Segoe UI";
            }}
            QPushButton:hover {{
                color: #252525;
            }}
        ''')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            return self.released.emit()