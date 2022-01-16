from utils.QtCore import *
from utils.functions import get_coin_icon, get_coin_list, get_icon_path
from utils.settings import Settings

from widgets.CustomAddCoinBtn.CustomAddCoinBtn import CustomAddCoinBtn
from widgets.CustomCoinsNumberLabel.CustomCoinsNumberLabel import CustomCoinsNumberLabel
from widgets.CustomComboBox.CustomComboBox import CustomComboBox
from widgets.CustomCompleter.CustomCompleter import CustomCompleter
from widgets.CustomInfoBox.CustomInfoBox import CustomInfoBox
from widgets.CustomLineEdit.CustomLineEdit import CustomLineEdit
from widgets.CustomTable.CustomTable import CustomTable


class CustomPage (QWidget):
    # SIGNALS
    clicked = Signal()
    released = Signal()

    def __init__(self):
        super().__init__()

        self.settings = Settings().app_settings

        self._exchange_list = self.settings['exchange_list']
        self._exchange_coins_list = []

        self.setup_ui()

        # INITIALIZE COIN LIST, COMPLETER MODEL AND LABEL INFO
        self._exchange_coins_list = get_coin_list(self.select_exchange.currentText())
        self.search_coin_completer.model().setStringList(self._exchange_coins_list)
        self.label_coins_number.update_info(self.select_exchange.currentText(), len(self._exchange_coins_list))

        self.setStyleSheet(f'''
            background-color: #eeeeee; 
            border: none;
        ''')

        self.select_exchange.currentTextChanged.connect(self.update_exchange_coin_info)

        self.add_coin_btn.clicked.connect(self.btn_clicked)
        self.add_coin_btn.released.connect(self.btn_released)


    def btn_clicked (self):
        self.clicked.emit()


    def btn_released (self):
        self.released.emit()

    
    def get_coins_list (self):
        return self._exchange_coins_list

    
    def update_exchange_coin_info (self):
        # UPDATE COIN LIST, COMPLETER MODEL AND LABEL INFO
        self.label_coins_number.update_info(loading=True)
        self._exchange_coins_list = get_coin_list(self.select_exchange.currentText())
        self.search_coin_completer.model().setStringList(self._exchange_coins_list)
        self.label_coins_number.update_info(self.select_exchange.currentText(), len(self._exchange_coins_list))


    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        # TOP LAYOUT
        self.top_frame = QFrame()
        self.top_frame.setMinimumHeight(60)
        self.top_frame.setMaximumHeight(60)
        self.top_frame.setStyleSheet('background-color: #dddddd; border-radius:0px;')
        self.top_layout = QHBoxLayout(self.top_frame)
        self.top_layout.setContentsMargins(30,10,30,10)
        self.top_layout.setSpacing(10)

        self.select_exchange = CustomComboBox()
        self.select_exchange.setMinimumWidth(250)
        self.select_exchange.setMaximumWidth(250)
        self.select_exchange.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.select_exchange.addItems(self._exchange_list)

        self.search_coin = CustomLineEdit('Search coin')
        self.search_coin.setMinimumWidth(250)
        self.search_coin.setMaximumWidth(250)

        self.search_coin_completer = CustomCompleter()
        self.search_coin.setCompleter(self.search_coin_completer)

        self.label_coins_number = CustomCoinsNumberLabel()

        self.add_coin_btn = CustomAddCoinBtn()

        # INFO BOXES
        self.info_boxes = QFrame()
        self.info_boxes.setMinimumHeight(150)
        self.info_boxes.setMaximumHeight(150)
        self.info_boxes_layout = QHBoxLayout(self.info_boxes)

        self.info_box_1 = CustomInfoBox(
            title='Top Gainer Coin',
            is_percentage=True
        )
        self.info_box_2 = CustomInfoBox(
            title='Top Loser Coin',
            is_percentage=True
        )
        self.info_box_3 = CustomInfoBox(
            title='Top Volume Coin',
            is_percentage=False
        )

        self.info_boxes_layout.addWidget(self.info_box_1)
        self.info_boxes_layout.addWidget(self.info_box_2)
        self.info_boxes_layout.addWidget(self.info_box_3)

        # TABLE INFO LAYOUT
        self.table_info_frame = QFrame()
        self.table_info_layout = QVBoxLayout(self.table_info_frame)
        self.table_info_layout.setContentsMargins(50,10,50,10)
        self.table_info_layout.setSpacing(0)

        self.table_coins = CustomTable(self)

        # SET WIDGETS TO LAYOUT
        self.top_layout.addWidget(self.select_exchange)
        self.top_layout.addWidget(self.label_coins_number)
        self.top_layout.addWidget(self.search_coin)
        self.top_layout.addWidget(self.add_coin_btn)

        self.table_info_layout.addWidget(self.info_boxes)
        self.table_info_layout.addWidget(self.table_coins)

        self.main_layout.addWidget(self.top_frame, alignment=Qt.AlignTop)
        self.main_layout.addWidget(self.table_info_frame)
