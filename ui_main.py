from utils.QtCore import *
from utils.settings import Settings

from widgets.CustomTitleBar.CustomTitleBar import CustomTitleBar
from page.CustomPage import CustomPage


class UI_MainWindow (object):
    def setup_ui (self, parent):

        self.app_settings = Settings().app_settings
        self.title_bar_settings = Settings().title_bar_settings

        parent.setObjectName('Main_Window')
        parent.resize(self.app_settings['start_width'], self.app_settings['start_height'])
        parent.setMinimumSize(self.app_settings['minimum_width'], self.app_settings['minimum_height'])

        # CENTRAL WIDGET AND LAYOUT
        self.central_widget = QWidget()
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        self.central_widget_layout.setContentsMargins(10,10,10,10)

        # MAIN FRAME
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet(f'background-color: transparent;')
        self.main_layout = QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        self.central_widget_layout.addWidget(self.main_frame)

        # TITLE BAR
        self.title_bar_frame = QFrame()
        self.title_bar_frame.setMaximumHeight(self.title_bar_settings['tb_height'])
        self.title_bar_frame.setMinimumHeight(self.title_bar_settings['tb_height'])
        self.title_bar_layout = QVBoxLayout(self.title_bar_frame)
        self.title_bar_layout.setContentsMargins(0,0,0,0)
        self.custom_title_bar = CustomTitleBar(parent, self.central_widget)
        self.title_bar_layout.addWidget(self.custom_title_bar)

        # PAGE
        self.main_page = CustomPage()
        
        self.main_layout.addWidget(self.title_bar_frame)
        self.main_layout.addWidget(self.main_page)

        # SET CENTRAL WIDGET
        parent.setCentralWidget(self.central_widget)
