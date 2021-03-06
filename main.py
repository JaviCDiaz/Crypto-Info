# *************************************************************
#
#   BY: JAVIER C. DIAZ
#   VERSION: 1.0.0
#   DESCRIPTION: An application to get and compare information
#                about cryptos from several exchanges
#
# *************************************************************


# WINDOWS TASKBAR ICON
import ctypes
myappid = 'Crypto Info'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

import sys
import sqlite3
import pandas as pd

from utils.QtCore import *
from utils.db_functions import db_create_table, db_update_table, add_coin_to_db
from utils.functions import format_coin_info, get_all_coin_lists, get_icon_path, get_coins_info, get_coins_info_urls
from utils.settings import Settings

from ui_main import UI_MainWindow
from widgets.CustomComboBox.CustomComboBox import CustomComboBox
from widgets.CustomGrips.CustomGrips import CustomGrip
from widgets.CustomLineEdit.CustomLineEdit import CustomLineEdit


class Splashcreen (QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_settings = Settings().app_settings
        self.coins_db_settings = Settings().coins_database_settings

        self.setWindowTitle(self.app_settings['window_title'])
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(700, 400)
        
        self.app_icon = QIcon()
        self.app_icon.addFile(get_icon_path(self.app_settings['app_logo']))
        self.setWindowIcon(self.app_icon)

        self._splashscreen_logo = get_icon_path('splashscreen_logo.png')

        self.setup_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_app)
        self.timer.start(40)

        self.show()


    def load_app(self):

        conn = sqlite3.connect(self.coins_db_settings['db_file_name'])
        db_create_table(conn, self.coins_db_settings['db_table_name'])

        # LOADING COIN INFO FROM DATABASE
        df_coins = pd.read_sql_query(f"SELECT coin, exchange from {self.coins_db_settings['db_table_name']}", conn).to_dict('records')
        if df_coins:
            urls = get_coins_info_urls(df_coins)
            coin_info_request_results = get_coins_info(urls)

            for idx in range(len(coin_info_request_results[0])):
                coin_updated_info = format_coin_info(coin_info_request_results[0][idx], coin_info_request_results[1][idx], coin_info_request_results[2][2*idx], coin_info_request_results[2][2*idx + 1])
                db_update_table(conn, self.coins_db_settings['db_table_name'], coin_updated_info)
                conn.commit()
            
            self.progress_bar.setValue(50)
        
        else:
            self.progress_bar.setValue(50)
        
        # LOADING COIN LISTS FROM ALL EXCHANGES
        all_coin_lists = get_all_coin_lists()
        self.progress_bar.setValue(100)

        # CLOSE CONNECTION AND FINISH SPLASHSCREEN
        if conn:
            conn.close()

        self.timer.stop()

        self.body = MainWindow(all_coin_lists)
        self.body.show()

        self.close()
        
    
    def setup_ui(self):
        # CENTRAL WIDGET AND LAYOUT
        self.central_widget = QWidget()
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        self.central_widget_layout.setContentsMargins(0,0,0,0)

        # MAIN FRAME
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet('background-color: #202020; border-radius: 10px;')
        self.main_layout = QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(10,50,10,50)

        # LOGO
        self.logo = QLabel()
        self.logo.setMinimumSize(100,100)
        self.logo.setMaximumSize(100,100)
        self.logo.setStyleSheet(f'image: url("{self._splashscreen_logo}")')

        # TITLE
        self.title = QLabel()
        self.title.setMinimumHeight(40)
        self.title.setMaximumHeight(40)
        self.title.setText('Crypto-Info')
        self.title.setStyleSheet('color: #d2d2d2; font: 600 14pt "Segoe UI"')

        # PROGRESS BAR
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumSize(500, 30)
        self.progress_bar.setMaximumSize(500, 30)
        self.progress_bar.setStyleSheet(f'''
            QProgressBar{{
                background-color:#505050;
                border-style:none;
                border-radius:15px;
                color: #242424;
                text-align:center;
            }}
            
            QProgressBar::Chunk{{
                background-color: #ffc50c;
                border-radius:15px;
            }}
        ''')
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progressBar")

        # INFO TEXT
        self.info_text = QLabel()
        self.info_text.setMinimumHeight(30)
        self.info_text.setMaximumHeight(30)
        self.info_text.setText('Loading...')
        self.info_text.setStyleSheet('font: 500 10pt "Segoe UI"; color: #d2d2d2')

        # ADD WIDGETS TO LAYOUTS
        self.main_layout.addWidget(self.logo, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.title, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.info_text, alignment=Qt.AlignCenter)

        self.central_widget_layout.addWidget(self.main_frame)

        self.setCentralWidget(self.central_widget)


class MainWindow (QMainWindow):
    def __init__(
        self,
        all_coin_lists = []
    ):
        super().__init__()

        self.app_settings = Settings().app_settings
        self.coins_db_settings = Settings().coins_database_settings
        self.all_coin_lists = all_coin_lists

        self.app_icon = QIcon()
        self.app_icon.addFile(get_icon_path(self.app_settings['app_logo']))
        self.setWindowIcon(self.app_icon)

        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        self.app_config()

    
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

            coin_info = [{'coin': coin, 'exchange': exchange}]

            if coin in coin_list:
                urls = get_coins_info_urls(coin_info)
                request_results = get_coins_info(urls)

                new_coin_info = format_coin_info(request_results[0][0], request_results[1][0], request_results[2][0], request_results[2][1])

                if add_coin_to_db(self.coins_db_settings['db_file_name'], self.coins_db_settings['db_table_name'], new_coin_info):
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
    app_window = Splashcreen()

    sys.exit(app.exec())