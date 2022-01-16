# *************************************************************
#
#   BY: JAVIER C. DIAZ
#   VERSION: 1.0.0
#   DESCRIPTION: An application to get and compare information
#                about cryptos from several exchanges
#
# *************************************************************

import sys
import sqlite3
import pandas as pd

from utils.QtCore import *
from utils.functions import add_coin_to_db, get_coin_info, refresh_coin_info
from utils.settings import Settings

from ui_main import UI_MainWindow
from widgets.CustomComboBox.CustomComboBox import CustomComboBox
from widgets.CustomGrips.CustomGrips import CustomGrip
from widgets.CustomLineEdit.CustomLineEdit import CustomLineEdit


class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_settings = Settings().app_settings
        self.coins_db_settings = Settings().coins_database_settings

        # UPDATE DATA WHEN OPEN THE APP, BEFORE LOADING GUI
        #refresh_coin_info(self.coins_db_settings['db_file_name'], self.coins_db_settings['db_table_name'])

        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        self.app_config()

        self.show()

    
    def setup_btns (self):
        if self.ui.main_page.sender() != None:
            return self.ui.main_page.sender()


    def app_config (self):
        self.setWindowTitle(self.app_settings['window_title'])
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # GRIPS
        self.left_grip = CustomGrip(self, "left")
        self.right_grip = CustomGrip(self, "right")
        self.top_grip = CustomGrip(self, "top")
        self.bottom_grip = CustomGrip(self, "bottom")
        self.top_left_grip = CustomGrip(self, "top_left")
        self.top_right_grip = CustomGrip(self, "top_right")
        self.bottom_left_grip = CustomGrip(self, "bottom_left")
        self.bottom_right_grip = CustomGrip(self, "bottom_right")

        # BTN CONNECTIONS
        self.ui.main_page.clicked.connect(self.btn_clicked)
        self.ui.main_page.released.connect(self.btn_released)


    def btn_clicked (self):
        btn = self.setup_btns()

        if btn.objectName() == 'add_coin_btn':
            exchange = self.ui.main_page.select_exchange.currentText()
            coin = self.ui.main_page.search_coin.text()
            coin_list = self.ui.main_page.get_coins_list()

            if coin in coin_list:
                coin_info = get_coin_info(exchange, coin)
                info = {
                    'coin': coin,
                    'exchange': exchange,
                    'price': coin_info['price'],
                    'volume_24h': coin_info['volume_24h'],
                    'quote_volume_24h': coin_info['quote_volume_24h'],
                    'change_24h': coin_info['change_24h'],
                    'chart_24h': coin_info['chart_24h']
                }
                if add_coin_to_db(self.coins_db_settings['db_file_name'], self.coins_db_settings['db_table_name'], info):
                    self.ui.main_page.table_coins.load_table_data()
                else:
                    print('coin can not added correctly')
            else:
                print('Select a valid coin.')

        # DEBUG
        print(f"Button {btn.objectName()} clicked")

    
    def btn_released (self):
        btn = self.setup_btns()

        # DEBUG
        print(f"Button {btn.objectName()} released")


    def resize_grips(self):
        self.left_grip.setGeometry(5, 10, 10, self.height())
        self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
        self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
        self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
        self.top_left_grip.setGeometry(5, 5, 15, 15)
        self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
        self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
        self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)


    def resizeEvent(self, event):
        self.resize_grips()
        

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, (CustomLineEdit, CustomComboBox)):
            focused_widget.clearFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_window = MainWindow()

    sys.exit(app.exec())