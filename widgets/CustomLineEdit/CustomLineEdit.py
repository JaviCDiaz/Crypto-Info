from utils.QtCore import *
from utils.functions import get_icon_path
from utils.settings import Settings

class CustomLineEdit(QLineEdit):
    def __init__(
        self,
        placeholder_text,
        font={'weight': 600, 'size': 12, 'family': 'Segoe UI'}
    ):
        super().__init__()

        self.settigns = Settings().custom_line_edit_settings

        self.setMinimumHeight(40)
        self.setMaximumHeight(40)

        self._placeholder_text = placeholder_text

        # BG COLORS
        self._unfocus_bg_color = self.settigns['le_bg_unfocus_color']
        self._focus_bg_color = self.settigns['le_bg_focus_color']

        # TEXT COLORS
        self._unfocus_text_color = self.settigns['le_txt_unfocus_color']
        self._focus_text_color = self.settigns['le_txt_focus_color']
        self._uncofus_placeholder_text_color = self.settigns['le_txt_unfocus_placeholder_color']
        self._focus_placeholder_text_color = self.settigns['le_txt_focus_placeholder_color']

        # FONT
        self._font_weight = font['weight']
        self._font_size = font['size']
        self._font_family = font['family']

        # ICON
        self._icon_color = self.settigns['le_search_icon_color']
        self._icon_name = self.settigns['le_search_icon_name']

        # BORDER SETTINGS
        self._unfocus_border_color = self.settigns['le_unfocus_border_color']
        self._focus_border_color = self.settigns['le_focus_border_color']
        self._border_radius = self.settigns['le_border_radius']

        self.setPlaceholderText(self._placeholder_text)

        self.p = self.palette()
        self.set_placeholder_color()

        self.setStyleSheet(f"""
            QLineEdit{{
                background-color:{self._unfocus_bg_color};
                border-radius:{self._border_radius}px;
                border: 1px solid {self._unfocus_border_color};
                padding-left:40px;
                padding-right:15px;
                font: {self._font_weight} {self._font_size}pt "{self._font_family}"
            }}
            
            QLineEdit:focus{{
                border: 1px solid {self._focus_border_color};
                background-color: {self._focus_bg_color};
                color:{self._focus_text_color}
            }}

            QLineEdit:hover{{
                border: 1px solid {self._focus_border_color};
                color:{self._focus_text_color}
            }}
        """)


    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if len(self.text()) > 0:
            rect = QRect(5,
                self.cursorRect().y()-7,
                self.width() - 10,
                self.completer().widget().height())
            self.completer().complete(rect)


    def set_placeholder_color(self):
        self.p.setColor(QPalette.PlaceholderText, QColor(self._uncofus_placeholder_text_color))
        self.p.setColor(QPalette.Text, QColor(self._unfocus_text_color))
        self.setPalette(self.p)


    def focusInEvent(self, arg__1: QFocusEvent) -> None:
        self.p.setColor(QPalette.PlaceholderText, QColor(self._focus_placeholder_text_color))
        self.setPalette(self.p)
        return super().focusInEvent(arg__1)


    def focusOutEvent(self, arg__1: QFocusEvent) -> None:
        self.p.setColor(QPalette.PlaceholderText, QColor(self._uncofus_placeholder_text_color))
        self.setPalette(self.p)
        return super().focusOutEvent(arg__1)


    def paintEvent(self, arg__1: QPaintEvent) -> None:
        super().paintEvent(arg__1)
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRect(0, 0, 40, self.height())
        icon = QPixmap(get_icon_path(self._icon_name))
        self.icon_paint(p, icon, rect)

        p.end()


    def icon_paint(self, qp, icon, rect):
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), self._icon_color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2, 
            (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()
