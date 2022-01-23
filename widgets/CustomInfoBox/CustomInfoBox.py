from utils.QtCore import *
from utils.functions import get_coin_icon, get_icon_path

class CustomInfoBox (QFrame):
    def __init__(
        self,
        title = '',
        is_percentage = False,
    ):
        super().__init__()

        self.setMinimumWidth(250)
        self.setMaximumWidth(250)

        self._title = title
        self._coin_name = '--'
        self._coin_icon = get_coin_icon(self._coin_name, size=32)
        self._price = '$' + str(0.000)
        self._is_percentage = is_percentage
        self._data_info = '--'

        self.setup_ui()

    
    def load_info_box_data (self, coin_name, price, data):
        self.coin_name.setText(coin_name)
        self.coin_icon.setStyleSheet(f'image: url("{get_coin_icon(coin_name, size=32)}")')
        self.coin_price.setText('$' + str(price))

        self.coin_data.load_data(data)


    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        
        self.title = QLabel()
        self.title.setMinimumHeight(20)
        self.title.setMaximumHeight(20)
        self.title.setText(self._title)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(f'''
            padding-left: 10px;
            color: #777777;
            font: 600 10pt "Segoe UI"
        ''')

        self.coin_info = QFrame()
        self.coin_info.setMinimumHeight(40)
        self.coin_info.setMaximumHeight(40)
        self.coin_info_layout = QHBoxLayout(self.coin_info)
        self.coin_info_layout.setContentsMargins(0,0,0,0)
        self.coin_info_layout.setSpacing(10)

        self.coin_icon = QLabel()
        self.coin_icon.setMinimumWidth(40)
        self.coin_icon.setMaximumWidth(40)
        self.coin_icon.setStyleSheet(f'image: url("{self._coin_icon}")')

        self.coin_name = QLabel()
        self.coin_name.setText(self._coin_name)
        self.coin_name.setStyleSheet(f'''
            color: #252525;
            font: 600 12pt "Segoe UI"
        ''')

        self.coin_price = QLabel()
        self.coin_price.setText(self._price)
        self.coin_price.setStyleSheet(f'''
            color: #252525;
            font: 600 12pt "Segoe UI"
        ''')

        self.coin_data = CustomInfoBoxCoinData(
            is_percentage=self._is_percentage,
            data=self._data_info
        )

        self.coin_info_layout.addWidget(self.coin_icon)
        self.coin_info_layout.addWidget(self.coin_name)
        self.coin_info_layout.addWidget(self.coin_price, alignment=Qt.AlignRight)

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.coin_info)
        self.main_layout.addWidget(self.coin_data)


class CustomInfoBoxCoinData (QFrame):
    def __init__(
        self,
        is_percentage = False,
        data = '--'
    ):
        super().__init__()

        self._is_percentage = is_percentage
        self._data = data
        
        self._positive_color = '#03a66d'
        self._neutral_color = '#252525'
        self._negative_color = '#cf304a'
        self._no_data_color = '#777777'


    def load_data (self, data):
        self._data = data
        self.repaint()

    
    def paintEvent(self, arg__1: QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self._data == '--':
            rect_text = QRect(40, 0, self.rect().width(), self.rect().height())
            rect_icon = self.rect()
            pen_text = QPen(QColor(self._no_data_color))
        else:
            if self._is_percentage:
                rect_text = QRect(40, 0, self.rect().width(), self.rect().height())
                rect_icon = self.rect()
                if float(self._data[:-1]) > 0:
                    icon = QPixmap(get_icon_path('icon_info_box_up.png'))
                    color = self._positive_color
                    self.icon_paint(painter, icon, rect_icon, color)
                    pen_text = QPen(QColor(color))
                elif float(self._data[:-1]) == 0:
                    icon = QPixmap(get_icon_path('icon_dash.png'))
                    color = self._neutral_color
                    self.icon_paint(painter, icon, rect_icon, color)
                    pen_text = QPen(QColor(color))
                else:
                    icon = QPixmap(get_icon_path('icon_info_box_down.png'))
                    color = self._negative_color
                    self.icon_paint(painter, icon, rect_icon, color)
                    pen_text = QPen(QColor(color))
            else:
                rect_text = QRect(10, 0, self.rect().width(), self.rect().height())
                pen_text = QPen(QColor(self._neutral_color))
            
        painter.setFont(QFont("Segoe UI", 14, 600))
        painter.setPen(pen_text)
        painter.drawText(rect_text, Qt.AlignVCenter, self._data)
    
        painter.end()

    def icon_paint(self, qp, icon, rect, color):
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap(
            8, 
            rect.y() + (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()