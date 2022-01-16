import os
from typing import Union

from utils.QtCore import *
from utils.settings import Settings
from utils.functions import get_coin_icon, get_icon_path


class CustomCompleter (QCompleter):
    def __init__(
        self
    ):
        super().__init__()

        self.settings = Settings().coin_completer_settings

        self._list_bg_color = self.settings['coin_comp_list_bg_color']
        self._list_item_height = self.settings['coin_comp_list_item_height']

        self._scrollbar_width = self.settings['coin_comp_scroll_width']
        self._scrollbar_radius = self._scrollbar_width // 2
        self._scrollbar_handler_color = self.settings['coin_comp_scroll_handler_color']

        self.setModel(QStringListModel())
        self.setCaseSensitivity(Qt.CaseInsensitive)

        self.popup().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.popup().setStyleSheet(f'''
            QListView{{
                background-color: {self._list_bg_color};
                border-radius: 0px;
                outline: 0px;
                padding: 3px 0 3px 0;
            }}
            QListView::item{{
                min-height: {self._list_item_height}px;
                max-height: {self._list_item_height}px;
            }}

            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: {self._scrollbar_width}px;
                border-radius: {self._scrollbar_radius}px;
                margin: 5px 0 5px 0;
            }}
            QScrollBar::handle:vertical {{	
                background: {self._scrollbar_handler_color};
                min-height: 25px;
                border-radius: 5px
            }}
            QScrollBar::add-line:vertical {{
                height: 0px;
            }}
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        ''')

        self.popup().setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.popup().setItemDelegate(CompleterDelegate())


class CompleterDelegate (QStyledItemDelegate):
    def __init__(
        self
    ):
        super(CompleterDelegate, self).__init__()

        self.settings = Settings().coin_completer_settings

        self._bg_color_hover = self.settings['coin_comp_item_bg_color_hover']
        self._default_icon_name = self.settings['coin_comp_item_default_icon_name']
        self._item_text_color = self.settings['coin_comp_item_text_color']


    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        item_text = index.model().index(index.row(), index.column()).data()

        icon = QPixmap(get_coin_icon(item_text, size=16))

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
