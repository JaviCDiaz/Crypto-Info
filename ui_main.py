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

        # CREDITS BAR
        self.credits_bar = QFrame()
        self.credits_bar.setStyleSheet(f'''
            background-color:#dddddd;
            padding: 0 15px 0 15px;
            border-bottom-left-radius: {self.app_settings['app_corner_radius']}px;
            border-bottom-right-radius: {self.app_settings['app_corner_radius']}px;
        ''')
        self.credits_bar.setMaximumHeight(self.title_bar_settings['tb_height'])
        self.credits_bar.setMinimumHeight(self.title_bar_settings['tb_height'])
        self.credits_layout = QHBoxLayout(self.credits_bar)
        self.credits_layout.setContentsMargins(0,0,0,0)

        self.credits_author = QLabel()
        self.credits_author.setText('Created By:    Javier C. Diaz')
        self.credits_author.setStyleSheet('''
            color: #888888;
            font: 600 8pt "Segoe UI";
        ''')
        
        self.credits_version = QLabel()
        self.credits_version.setText('Version 1.0.0')
        self.credits_version.setStyleSheet('''
            color: #888888;
            font: 600 8pt "Segoe UI";
        ''')

        self.credits_layout.addWidget(self.credits_author)
        self.credits_layout.addWidget(self.credits_version, alignment=Qt.AlignRight)

        # PAGE
        self.main_page = CustomPage(parent)
        
        # ADD WIDGETS TO LAYOUTS
        self.main_layout.addWidget(self.title_bar_frame)
        self.main_layout.addWidget(self.main_page)
        self.main_layout.addWidget(self.credits_bar)

        # SET CENTRAL WIDGET
        parent.setCentralWidget(self.central_widget)
