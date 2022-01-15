import os
from typing import Union

from utils.QtCore import *
from utils.functions import get_exchange_icon, get_icon_path
from utils.settings import Settings


class CustomComboBox (QComboBox):
    def __init__(
        self
    ):
        super().__init__()

        self.settings = Settings().combobox_settings

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)

        # BG COLORS
        self._unfocus_bg_color = self.settings['cbox_unfocus_bg_color']
        self._focus_bg_color = self.settings['cbox_focus_bg_color']

        # BORDER SETTINGS
        self._unfocus_border_color = self.settings['cbox_unfocus_border_color']
        self._focus_border_color = self.settings['cbox_focus_border_color']
        self._border_radius = self.settings['cbox_border_radius']

        # TEXT
        self._unfocus_text_color = self.settings['cbox_txt_unfocus_color']
        self._focus_text_color = self.settings['cbox_txt_focus_color']
        self._font_weight = self.settings['cbox_font_weight']
        self._font_size = self.settings['cbox_font_size']
        self._font_family = self.settings['cbox_font_family']

        # POPUP SETTINGS
        self._popup_bg_color = self.settings['cbox_popup_bg_color']
        self._popup_item_height = self.settings['cbox_popup_item_height']

        # DROPDOWN ICON
        self._unfocus_icon_color = self.settings['cbox_icon_unfocus_color']
        self._unfocus_icon = get_icon_path(self.settings['cbox_icon_unfocus'])
        self._focus_icon_color = self.settings['cbox_icon_focus_color']
        self._focus_icon = get_icon_path(self.settings['cbox_icon_focus'])

        # SET DEFAULT PARAMETERS
        self._dropdown_icon = self._unfocus_icon
        self._dropdown_icon_color = self._unfocus_icon_color

        self.setStyleSheet(f'''
            QComboBox{{
                background-color:{self._unfocus_bg_color};
                border-radius:{self._border_radius}px;
                border: 1px solid {self._unfocus_border_color};
                padding-left:54px;
                padding-right:15px;
                font: {self._font_weight} {self._font_size}pt "{self._font_family}";
                color: {self._unfocus_text_color};
            }}
            
            QComboBox:focus{{
                border: 1px solid {self._focus_border_color};
                background-color: {self._focus_bg_color};
                color:{self._focus_text_color}
            }}

            QComboBox:hover{{
                border: 1px solid {self._focus_border_color};
                color:{self._focus_text_color}
            }}
            
            QListView{{
                background-color: {self._popup_bg_color};
                border-radius: 0px;
                outline: 0px;
                padding: 3px 0 3px 0;
            }}
            QListView::item{{
                min-height: {self._popup_item_height}px;
                max-height: {self._popup_item_height}px;
            }}

            QComboBox::drop-down{{
                border: 0px;
            }}
        ''')

        self.setItemDelegate(ComboBoxDelegate())


    def showPopup(self) -> None:
        super().showPopup()

        popup: QWidget = self.findChild(QFrame)
        popup.setMaximumWidth(self.width() - 10)
        popup.move(popup.x() + 5, popup.y() + 4)

        self._dropdown_icon = self._focus_icon
        self._dropdown_icon_color = self._focus_icon_color


    def hidePopup(self) -> None:
        self._dropdown_icon = self._unfocus_icon
        self._dropdown_icon_color = self._unfocus_icon_color
        self.clearFocus()
        return super().hidePopup()


    def paintEvent(self, arg__1: QPaintEvent) -> None:
        super().paintEvent(arg__1)

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        dropdown_icon = QPixmap(self._dropdown_icon)
        self.dropdown_icon_paint(p, dropdown_icon, self.rect())
        
        icon = QPixmap(get_exchange_icon(self.currentText().lower(), size=24))
        icon_rect = QRect(15, 0, icon.width(), self.height())
        self.icon_paint(p, icon, icon_rect)

        p.end()


    def dropdown_icon_paint(self, qp, icon, rect):
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), self._dropdown_icon_color)
        qp.drawPixmap(
            (rect.width() - 2*icon.width()), 
            (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()


    def icon_paint(self, qp, icon, rect):
        painter = QPainter(icon)
        qp.drawPixmap(
            rect.left() + (rect.width() - icon.width()) / 2, 
            (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()


class ComboBoxDelegate (QStyledItemDelegate):
    def __init__(
        self
    ):
        super(ComboBoxDelegate, self).__init__()
        
        self.settings = Settings().combobox_settings

        # ITEM DELEGATE
        self._bg_color_hover = self.settings['cbox_item_bg_color_hover']
        self._item_text_color = self.settings['cbox_item_text_color']


    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        item_text = index.model().index(index.row(), index.column()).data()
        icon = QPixmap(get_exchange_icon(item_text.lower(), size=16))

        if option.state & QStyle.State_MouseOver:
            rect_text = QRect(option.rect.left() + 40 + icon.width(), option.rect.top(), option.rect.width() - 40 - icon.width(), option.rect.height())
            rect_icon = QRect(option.rect.left() + 25, option.rect.top(), icon.width(), option.rect.height())
            painter.setBrush(QColor(self._bg_color_hover))
            painter.setPen(Qt.NoPen)
            painter.drawRect(option.rect)
        
        else:
            rect_text = QRect(option.rect.left() + 30 + icon.width(), option.rect.top(), option.rect.width() - 30 - icon.width(), option.rect.height())
            rect_icon = QRect(option.rect.left() + 15, option.rect.top(), icon.width(), option.rect.height())

        pen = QPen(QColor(self._item_text_color))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setFont(QFont("Segoe UI", 9, 400))

        painter.drawText(rect_text, Qt.AlignVCenter, item_text)
        self.icon_paint(painter, icon, rect_icon)


    def icon_paint(self, qp, icon, rect):
        painter = QPainter(icon)
        qp.drawPixmap(
            rect.left() + (rect.width() - icon.width()) / 2, 
            rect.y() + (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()
