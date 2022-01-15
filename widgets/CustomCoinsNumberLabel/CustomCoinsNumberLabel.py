from utils.QtCore import *
from utils.functions import get_exchange_icon


class CustomCoinsNumberLabel (QLabel):
    def __init__(
        self
    ):
        super().__init__()

        self._coins_number = 0
        self._text_prefix = 'Number of coins listed:   '
        self._exchange = 'binance'
        self._loading = False

        self.setStyleSheet('''
            color: #404040;
            font: 600 12pt "Segoe UI";
            padding-left: 36px;
        ''')


    def update_info (self, exchange=None, coins_number=None, loading=False):
        self._exchange = exchange
        self._coins_number = coins_number
        self._loading = loading
        if loading:
            self.setText('Loading...')
            self.repaint()
        else:
            self.setText(self._text_prefix + str(self._coins_number))
            self.repaint()


    def paintEvent(self, arg__1: QPaintEvent) -> None:
        super().paintEvent(arg__1)

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if not self._loading:
            icon = QPixmap(get_exchange_icon(self._exchange, size=16))
            rect = QRect(10, 0, icon.width(), self.height())
            self.icon_paint(p, icon, rect)

        p.end()


    def icon_paint(self, qp, icon, rect):
        painter = QPainter(icon)
        qp.drawPixmap(
            rect.left() + (rect.width() - icon.width()) / 2, 
            (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()
