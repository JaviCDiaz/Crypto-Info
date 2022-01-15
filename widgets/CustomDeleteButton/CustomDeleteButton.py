import sqlite3
from sqlite3 import Error

from utils.QtCore import *
from utils.functions import get_icon_path
from utils.settings import Settings


class CustomDeleteButton (QPushButton):
    def __init__(
        self,
        parent,
        btn_id = ''
    ):
        super().__init__()
        
        self._coins_db_settings = Settings().coins_database_settings

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(40, 40)
        self.setMaximumSize(40, 40)
        self.setObjectName(btn_id)

        self._parent = parent

        self._icon_inactive_color = '#777777'
        self._icon_hover_color = '#ed2f2f'
        self._icon_pressed_color = '#c92828'

        self._icon_path = get_icon_path('icon_bin.png')
        self._icon_color = self._icon_inactive_color

        self.clicked.connect(self.delete_coin)

    
    def delete_coin (self):
        button = self.sender()
        if button is not None:
            row = self._parent.indexAt(button.pos()).row()

            row_coin = self._parent.item(row, 0).text()
            row_exchange = self._parent.item(row, 1).text()

            conn = None
            try:
                conn = sqlite3.connect(self._coins_db_settings['db_file_name'])

                conn.cursor().execute(f'''
                    DELETE FROM {self._coins_db_settings['db_table_name']}
                    WHERE
                        coin = "{row_coin}" AND exchange = "{row_exchange}"
                ''')

                conn.commit()

            except Error as e:
                print(e)

            finally:
                if conn:
                    conn.close()

        self._parent.load_table_data()


    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.NoPen)

        icon = QPixmap(self._icon_path)
        rect_icon = QRect(0, 10, icon.width(), 40)
        self.icon_paint(p, icon, rect_icon, self._icon_color) 
    
        p.end()


    def icon_paint(self, qp, icon, rect, color):
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2, 
            rect.y() + (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()


    def enterEvent(self, event):
        self._icon_color = self._icon_hover_color
        self.repaint()

    def leaveEvent(self, event):
        self._icon_color = self._icon_inactive_color
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._icon_color = self._icon_pressed_color
            self.repaint()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._icon_color = self._icon_inactive_color
            self.repaint()
            return self.released.emit()
        