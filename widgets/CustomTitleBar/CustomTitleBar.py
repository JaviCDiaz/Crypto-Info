from utils.QtCore import *
from utils.settings import Settings
from utils.functions import get_icon_path

from widgets.CustomTitleBar.CustomAppButton import CustomAppButton


_is_maximized = False
_old_size = QSize()


class CustomTitleBar (QWidget):
    def __init__(
        self,
        parent,
        app_parent,
    ):
        super().__init__()

        self.app_settings = Settings().app_settings
        self.title_bar_settings = Settings().title_bar_settings

        self._parent = parent
        self._app_parent = app_parent

        self._radius = self.app_settings['app_corner_radius']

        self._bg_color = self.title_bar_settings['tb_bg_color']
        self._logo_size = self.title_bar_settings['tb_logo_size']
        self._logo_image = get_icon_path(self.title_bar_settings['tb_logo_name'])
        
        self._title = self.title_bar_settings['tb_title']
        self._title_font_weight = self.title_bar_settings['tb_title_font_weight']
        self._title_font_size = self.title_bar_settings['tb_title_font_size']
        self._title_font_family = self.title_bar_settings['tb_title_font_family']
        self._title_color = self.title_bar_settings['tb_title_color']

        self._btn_bg_color_hover = self.title_bar_settings['tb_btn_bg_color_hover']
        self._btn_bg_color_pressed = self.title_bar_settings['tb_btn_bg_color_pressed']
        self._btn_close_bg_color_hover = self.title_bar_settings['tb_btn_close_bg_color_hover']
        self._btn_close_bg_color_pressed = self.title_bar_settings['tb_btn_close_bg_color_pressed']

        self._btn_minimize_icon = get_icon_path(self.title_bar_settings['tb_minimize_btn_icon_path'])
        self._btn_maximize_icon = get_icon_path(self.title_bar_settings['tb_maximize_btn_icon_path'])
        self._btn_restore_icon = get_icon_path(self.title_bar_settings['tb_maximize_btn_restore_icon_path'])
        self._btn_close_icon = get_icon_path(self.title_bar_settings['tb_close_btn_icon_path'])
        
        self.setup_ui()

        # MOVE WINDOW EVENT
        def moveWindow(event):
            if parent.isMaximized():
                self.maximize_restore()
                curso_x = parent.pos().x()
                curso_y = event.globalPosition().toPoint().y() - QCursor.pos().y()
                parent.move(curso_x, curso_y)

            if event.buttons() == Qt.LeftButton:
                parent.move(parent.pos() + event.globalPosition().toPoint() - parent.dragPos)
                parent.dragPos = event.globalPosition().toPoint()
                event.accept()
        
        # SIGNALS
        self.logo.mouseMoveEvent = moveWindow
        self.title_label.mouseMoveEvent = moveWindow

        self.logo.mouseDoubleClickEvent = self.maximize_restore
        self.title_label.mouseDoubleClickEvent = self.maximize_restore

        self.minimize_button.released.connect(lambda: parent.showMinimized())
        self.maximize_restore_button.released.connect(lambda: self.maximize_restore())
        self.close_button.released.connect(lambda: parent.close())


    # MAXIMIZE / RESTORE
    def maximize_restore(self, e=None):
        global _is_maximized
        global _old_size

        def remove_grips():
            self._parent.left_grip.setGeometry(0,0,0,0)
            self._parent.right_grip.setGeometry(0,0,0,0)
            self._parent.top_grip.setGeometry(0,0,0,0)
            self._parent.bottom_grip.setGeometry(0,0,0,0)
            self._parent.top_left_grip.setGeometry(0,0,0,0)
            self._parent.top_right_grip.setGeometry(0,0,0,0)
            self._parent.bottom_left_grip.setGeometry(0,0,0,0)
            self._parent.bottom_right_grip.setGeometry(0,0,0,0)
        
        def change_ui():
            if _is_maximized:
                self._parent.ui.central_widget_layout.setContentsMargins(0,0,0,0)
                self.main_bg.setStyleSheet(f'background-color:{self._bg_color}; border-top-right-radius:0px; border-top-left-radius:0px')
                self._parent.ui.credits_bar.setStyleSheet(f'''
                    background-color:#dddddd;
                    padding: 0 15px 0 15px;
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                ''')
                self.maximize_restore_button.set_icon(self._btn_restore_icon)
                self.maximize_restore_button._tooltip.setText(self.title_bar_settings['tb_maximize_btn_restore_tooltip_text'])
                self.maximize_restore_button._tooltip.adjustSize()
                remove_grips()
                
            else:
                self._parent.ui.central_widget_layout.setContentsMargins(10,10,10,10)
                self.main_bg.setStyleSheet(f'background-color:{self._bg_color}; border-top-right-radius:{self._radius}px; border-top-left-radius:{self._radius}px')
                self._parent.ui.credits_bar.setStyleSheet(f'''
                    background-color:#dddddd;
                    padding: 0 15px 0 15px;
                    border-bottom-left-radius: {self.app_settings['app_corner_radius']}px;
                    border-bottom-right-radius: {self.app_settings['app_corner_radius']}px;
                ''')
                self.maximize_restore_button.set_icon(get_icon_path(self.title_bar_settings['tb_maximize_btn_icon_path']))
                self.maximize_restore_button._tooltip.setText(self.title_bar_settings['tb_maximize_btn_tooltip_text'])
                self.maximize_restore_button._tooltip.adjustSize()
                
        if self._parent.isMaximized():
            _is_maximized = False
            self._parent.showNormal()
            change_ui()
        else:
            _is_maximized = True
            _old_size = QSize(self._parent.width(), self._parent.height())
            self._parent.showMaximized()
            change_ui()


    def setup_ui(self):
        # MAIN LAYOUT
        self.title_bar_main_layout = QVBoxLayout(self)
        self.title_bar_main_layout.setContentsMargins(0,0,0,0)

        # BG
        self.main_bg = QFrame()
        self.main_bg.setStyleSheet(f"background-color: {self._bg_color}; border-top-right-radius: {self._radius}px; border-top-left-radius: {self._radius}px")
        self.main_bg_layout = QHBoxLayout(self.main_bg)
        self.main_bg_layout.setContentsMargins(20,0,10,0)
        self.main_bg_layout.setSpacing(20)

        # LOGO
        self.logo = QLabel()
        self.logo.setText('')
        self.logo.setMaximumWidth(self._logo_size)
        self.logo.setMinimumWidth(self._logo_size)
        self.logo.setStyleSheet(f"image: url({self._logo_image})")

        # TITLE
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.title_label.setText(f'{self._title}')
        self.title_label.setStyleSheet(f"""font: {self._title_font_weight} {self._title_font_size}pt "{self._title_font_family}";
                                        color: {self._title_color}""")

        # MINIMIZE BUTTON
        self.minimize_button = CustomAppButton(
            self._parent,
            self._app_parent,
            tooltip_text = self.title_bar_settings['tb_minimize_btn_tooltip_text'],
            bg_color_hover = self._btn_bg_color_hover,
            bg_color_pressed = self._btn_bg_color_pressed,
            icon_path = self._btn_minimize_icon,
        )

        # MAXIMIZE / RESTORE BUTTON
        self.maximize_restore_button = CustomAppButton(
            self._parent,
            self._app_parent,
            tooltip_text = self.title_bar_settings['tb_maximize_btn_tooltip_text'],
            bg_color_hover = self._btn_bg_color_hover,
            bg_color_pressed = self._btn_bg_color_pressed,
            icon_path = self._btn_maximize_icon,
        )

        # CLOSE BUTTON
        self.close_button = CustomAppButton(
            self._parent,
            self._app_parent,
            tooltip_text = self.title_bar_settings['tb_close_btn_tooltip_text'],
            bg_color_hover = self._btn_close_bg_color_hover,
            bg_color_pressed = self._btn_close_bg_color_pressed,
            icon_path = self._btn_close_icon,
        )

        # ADD WIDGETS TO LAYOUTS
        self.main_bg_layout.addWidget(self.logo)
        self.main_bg_layout.addWidget(self.title_label)

        self.main_bg_layout.addWidget(self.minimize_button)
        self.main_bg_layout.addWidget(self.maximize_restore_button)
        self.main_bg_layout.addWidget(self.close_button)

        self.title_bar_main_layout.addWidget(self.main_bg)
