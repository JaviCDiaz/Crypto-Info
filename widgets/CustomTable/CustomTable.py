import json
import sqlite3
import pandas as pd
from typing import Union

from utils.QtCore import *
from utils.settings import Settings
from utils.functions import get_coin_icon, get_exchange_icon, get_icon_path

from widgets.CustomDeleteButton.CustomDeleteButton import CustomDeleteButton
from widgets.CustomTableChart.CustomTableChart import CustomTableChart


class CustomTable (QTableWidget):
    def __init__(
        self,
        parent
    ):
        super().__init__()

        self.setWordWrap(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self._parent = parent

        self.settings = Settings().table_settings
        self.coins_db_settings = Settings().coins_database_settings

        self._data = None

        self._text_color = self.settings['table_text_color']
        
        self._header_text_color = self.settings['table_header_text_color']
        self._header_font_weight = self.settings['table_header_font_weight']
        self._header_font_size = self.settings['table_header_font_size']
        self._header_font_family = self.settings['table_header_font_family']

        self._Vscrollbar_bg_color = self.settings['table_Vscrollbar_bg_color']
        self._Vscrollbar_width = self.settings['table_Vscrollbar_width']
        self._Vscrollbar_radius = self._Vscrollbar_width // 2
        self._Vscrollbar_handle_bar_color = self.settings['table_Vscrollbar_handle_bar_color']

        self._positive_chart_change = '#03a66d'
        self._negative_chart_change = '#cf304a'
        
        self.setColumnCount(7)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.Interactive)
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.Interactive)
        self.horizontalHeader().resizeSection(5, 180)  # WIDTH = CHART_WIDTH + PADDING_LEFT + PADDING_RIGHT
        self.horizontalHeader().resizeSection(6, 0)
        self.verticalHeader().hide()

        self.column_0 = QTableWidgetItem()
        self.column_0.setTextAlignment(Qt.AlignLeft)
        self.column_0.setText("Coin")

        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignLeft)
        self.column_1.setText("Exchange")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignLeft)
        self.column_2.setText("Price")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignLeft)
        self.column_3.setText("24h volume")

        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignLeft)
        self.column_4.setText("24h change")

        self.column_5 = QTableWidgetItem()

        self.column_6 = QTableWidgetItem()

        self.setHorizontalHeaderItem(0, self.column_0)
        self.setHorizontalHeaderItem(1, self.column_1)
        self.setHorizontalHeaderItem(2, self.column_2)
        self.setHorizontalHeaderItem(3, self.column_3)
        self.setHorizontalHeaderItem(4, self.column_4)
        self.setHorizontalHeaderItem(5, self.column_5)
        self.setHorizontalHeaderItem(6, self.column_6)

        self.setStyleSheet(f'''
            QTableWidget {{	
                gridline-color: transparent;
                color: {self._text_color};
                padding: 20px 20px 0px 20px;
            }}
            QTableWidget::item{{
                border-color: none;
                padding-left: 10px;
                padding-right: 15px;
            }}

            QHeaderView::section:horizontal{{
                background-color: transparent;
                color: {self._header_text_color};
                padding-left: 15px;
                padding-right: 15px;
                font: {self._header_font_weight} {self._header_font_size}pt "{self._header_font_family}";
            }}

            QScrollBar:vertical {{
                border: none;
                background: {self._Vscrollbar_bg_color};
                width: {self._Vscrollbar_width}px;
                border-radius: {self._Vscrollbar_radius}px;
                margin: 70px 0 20px 0;
            }}
            QScrollBar::handle:vertical {{	
                background: {self._Vscrollbar_handle_bar_color};
                min-height: 25px;
                border-radius: {self._Vscrollbar_radius}px
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

        self.setItemDelegate(CustomTableItemDelegate())

        # LOADING DATA
        self.load_table_data()


    def load_table_data (self):
        self.setRowCount(0)
        
        conn = sqlite3.connect(self.coins_db_settings['db_file_name'])
        self._data = pd.read_sql_query(f"SELECT * from {self.coins_db_settings['db_table_name']}", conn)

        if not self._data.empty:
            for index, row_info in self._data.iterrows():
                row_number = index

                column_0_item = QTableWidgetItem()
                column_0_item.setText(str(row_info['coin']))

                column_1_item = QTableWidgetItem()
                column_1_item.setText(str(row_info['exchange']))

                column_2_item = QTableWidgetItem()
                column_2_item.setText('$' + str(round(row_info['price'], 3)))

                column_3_item = QTableWidgetItem()
                column_3_item.setText(str(round(row_info['quote_volume_24h'], 2)) + '_' + str(round(row_info['volume_24h'], 3)))
                
                column_4_item = QTableWidgetItem()
                column_4_item.setText(str(round(row_info['change_24h'], 3)) + '%')

                column_5_chart_data = QSplineSeries()
                chart_7d_info = json.loads(row_info['chart_7d'])
                for idx, close_price in enumerate(chart_7d_info):
                    column_5_chart_data.append(idx, close_price)

                if chart_7d_info[-1] >= chart_7d_info[0]:
                    line_color = self._positive_chart_change
                else:
                    line_color = self._negative_chart_change

                self.column_5_chart = CustomTableChart(
                    data=column_5_chart_data,
                    max_value=max(chart_7d_info) * 1.01,
                    min_value=min(chart_7d_info) * 0.99,
                    line_color=line_color
                )

                self.column_6_btn = CustomDeleteButton(
                    parent = self,
                    btn_id = 'delete_btn_' + str(row_number)
                )
                
                self.insertRow(row_number)
                self.setItem(row_number, 0, column_0_item)
                self.setItem(row_number, 1, column_1_item)
                self.setItem(row_number, 2, column_2_item)
                self.setItem(row_number, 3, column_3_item)
                self.setItem(row_number, 4, column_4_item)
                self.setCellWidget(row_number, 5, self.column_5_chart)
                self.setCellWidget(row_number, 6, self.column_6_btn)
                self.setRowHeight(row_number, 60)

            # TOP GAINER COIN
            gainer_coin_name, gainer_price, gainer_data = self.get_gainer_coin()
            self._parent.info_box_1.load_info_box_data(gainer_coin_name, gainer_price, gainer_data)

            # TOP LOSSER COIN
            losser_coin_name, losser_price, losser_data = self.get_losser_coin()
            self._parent.info_box_2.load_info_box_data(losser_coin_name, losser_price, losser_data)

            # TOP VOLUME COIN
            top_volume_coin_name, top_volume_price, top_volume_data = self.get_top_volume_coin()
            self._parent.info_box_3.load_info_box_data(top_volume_coin_name, top_volume_price, top_volume_data)


    def get_gainer_coin (self):
        coin_name = self._data['coin'][self._data['change_24h'].idxmax()]
        price = round(self._data['price'][self._data['change_24h'].idxmax()], 3)
        data = str(round(self._data['change_24h'][self._data['change_24h'].idxmax()], 3)) + '%'
        return coin_name, price, data


    def get_losser_coin (self):
        coin_name = self._data['coin'][self._data['change_24h'].idxmin()]
        price = round(self._data['price'][self._data['change_24h'].idxmin()], 3)
        data = str(round(self._data['change_24h'][self._data['change_24h'].idxmin()], 3)) + '%'
        return coin_name, price, data
        

    def get_top_volume_coin (self):
        coin_name = self._data['coin'][self._data['quote_volume_24h'].idxmax()]
        price = round(self._data['price'][self._data['quote_volume_24h'].idxmax()], 3)
        data = '$ ' + str(round(self._data['quote_volume_24h'][self._data['quote_volume_24h'].idxmax()], 2))
        return coin_name, price, data


class CustomTableItemDelegate (QStyledItemDelegate):
    def __init__(
        self
    ):
        super(CustomTableItemDelegate, self).__init__()

        self.settings = Settings().table_settings

        self._pen_color = self.settings['table_item_pen_color']
        self._positive_ticker_change = '#03a66d'
        self._neutral_ticker_change = '#252525'
        self._negative_ticker_change = '#cf304a'

    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        item_index = index.model().index(index.row(),index.column())
        item_data = index.model().data(item_index)

        pen_text = QPen(QColor('#252525'))
        painter.setFont(QFont('Segoe UI', 10, 400))

        # HORIZONTAL DIV LINE
        pen_div = QPen(QColor(self._pen_color))
        pen_div.setWidth(1)
        path = QPainterPath()

        if index.row() != (index.model().rowCount() - 1):
            if index.column() != (index.model().columnCount() - 1):
                path.moveTo(option.rect.x(), option.rect.y() + option.rect.height())
                path.lineTo(option.rect.x() + option.rect.width(), option.rect.y() + option.rect.height())

        painter.setPen(pen_div)
        painter.drawPath(path)

        # COIN COLUMN
        if index.column() == 0:
            rect_text = QRect(option.rect.x() + 62, option.rect.y(), option.rect.width() - 62, option.rect.height())
            icon = QPixmap(get_coin_icon(item_data, size=32))
            self.icon_coin_paint(painter, icon, option.rect)

            painter.setPen(pen_text)
            painter.drawText(rect_text, Qt.AlignVCenter, item_data)

        # EXCHANGE COLUMN
        elif index.column() == 1:
            rect_text = QRect(option.rect.x() + 54, option.rect.y(), option.rect.width() - 54, option.rect.height())
            icon = QPixmap(get_exchange_icon(item_data, size=24))
            self.icon_coin_paint(painter, icon, option.rect)

            painter.setPen(pen_text)
            painter.drawText(rect_text, Qt.AlignVCenter, item_data)

        # VOLUME COLUMN
        elif index.column() == 3:
            row_coin = index.model().data(index.model().index(index.row(),0))
            
            quote_vol = item_data.split('_')[0]
            base_vol = item_data.split('_')[1]

            quote_vol_text = '--' if quote_vol == '-1.0' else '$ ' + quote_vol
            base_vol_text = '--' if base_vol == '-1.0' else row_coin + ' ' + base_vol

            quote_rect_text = QRect(option.rect.x() + 15, option.rect.y() + 5, option.rect.width() - 15, option.rect.height() - 35)
            base_rect_text = QRect(option.rect.x() + 15, option.rect.y() + 30, option.rect.width() - 15, option.rect.height() - 35)
            
            painter.setPen(pen_text)
            painter.drawText(quote_rect_text, Qt.AlignVCenter, quote_vol_text)
            painter.drawText(base_rect_text, Qt.AlignVCenter, base_vol_text)

        # 24 CHANGE COLUMN
        elif index.column() == 4:
            rect_text = QRect(option.rect.x() + 33, option.rect.y(), option.rect.width() - 33, option.rect.height())

            if float(item_data[:-1]) > 0:
                option.palette.setColor(QPalette.Text, self._positive_ticker_change)
                icon = QPixmap(get_icon_path('icon_price_up.png'))
                self.icon_paint(painter, icon, option.rect, self._positive_ticker_change)
                pen_text = QPen(QColor(self._positive_ticker_change))
            elif float(item_data[:-1]) == 0:
                option.palette.setColor(QPalette.Text, self._neutral_ticker_change)
                icon = QPixmap(get_icon_path('icon_dash.png'))
                self.icon_paint(painter, icon, option.rect, self._neutral_ticker_change)
                pen_text = QPen(QColor(self._neutral_ticker_change))
            else:
                option.palette.setColor(QPalette.Text, self._negative_ticker_change)
                icon = QPixmap(get_icon_path('icon_price_down.png'))
                self.icon_paint(painter, icon, option.rect, self._negative_ticker_change)
                pen_text = QPen(QColor(self._negative_ticker_change))

            painter.setPen(pen_text)
            painter.drawText(rect_text, Qt.AlignVCenter, item_data)

        else:
            rect_text = QRect(option.rect.x() + 15, option.rect.y(), option.rect.width() - 15, option.rect.height())

            painter.setPen(pen_text)
            painter.drawText(rect_text, Qt.AlignVCenter, item_data)


    def icon_coin_paint(self, qp, icon, rect):
        painter = QPainter(icon)
        qp.drawPixmap(
            rect.x() + 15, 
            rect.y() + (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()


    def icon_paint(self, qp, icon, rect, color):
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap(
            rect.x() + 15, 
            rect.y() + (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()

