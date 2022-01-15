from utils.QtCore import *
from utils.settings import Settings

from widgets.CustomTooltip.CustomTooltip import CustomTooltip


class CustomAppButton(QPushButton):
    def __init__(
        self,
        parent,
        app_parent = None,
        tooltip_text = "",
        bg_color_hover = "#404040",
        bg_color_pressed = "#353535",
        icon_path = None
    ):
        super().__init__()

        self._parent = parent
        self._app_parent = app_parent

        self.title_bar_settings = Settings().title_bar_settings
        self.tooltip_settings = Settings().tooltip_settings

        # DEFAULT PARAMETERS
        self.setFixedSize(self.title_bar_settings['tb_btn_width'], self.title_bar_settings['tb_btn_height'])
        self.setCursor(Qt.PointingHandCursor)

        self._bg_color_inactive = 'transparent'
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed

        self._icon_color_inactive = self.title_bar_settings['tb_btn_icon_color_inactive']
        self._icon_color_hover = self.title_bar_settings['tb_btn_icon_color_hover']
        self._icon_color_pressed = self.title_bar_settings['tb_btn_icon_color_pressed']

        self._btn_border_radius = self.title_bar_settings['tb_btn_radius']

        # SET PARAMETERS
        self._bg_color = self._bg_color_inactive
        self._icon_path = icon_path
        self._icon_color = self._icon_color_inactive

        # TOOLTIP
        self._top_margin = self.height() + 6
        self._tooltip_bg_color = self.tooltip_settings['tt_bg_color']
        self._tooltip_text_color = self.tooltip_settings['tt_text_color']
        self._tooltip_border_color = self.tooltip_settings['tt_border_color']
        self._tooltip_text = tooltip_text
        self._tooltip = CustomTooltip(
            self._app_parent,
            tooltip_text,
            self._tooltip_bg_color,
            self._tooltip_text_color,
            self._tooltip_border_color
        )
        self._tooltip.hide()


    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        brush = QBrush(QColor(self._bg_color))
        rect = QRect(0, 0, self.width(), self.height())

        p.setPen(Qt.NoPen)
        p.setBrush(brush)
        p.drawRoundedRect(rect, self._btn_border_radius, self._btn_border_radius)

        icon = QPixmap(self._icon_path)
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


    def set_icon(self, icon_path):
        self._icon_path = icon_path
        self.repaint()


    # MOUSE EVENTS
    def enterEvent(self, event):
        self._bg_color = self._bg_color_hover
        self._icon_color = self._icon_color_hover
        self.repaint()     
        self.move_tooltip()
        self._tooltip.show()

    def leaveEvent(self, event):
        self._bg_color = self._bg_color_inactive
        self._icon_color = self._icon_color_inactive
        self.repaint()
        self.move_tooltip()
        self._tooltip.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._bg_color = self._bg_color_pressed
            self._icon_color = self._icon_color_pressed
            self.repaint()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._bg_color = self._bg_color_hover
            self._icon_color = self._icon_color_hover
            self.repaint()
            return self.released.emit()


    # TOOLTIP
    def move_tooltip(self):
        gp = self.mapToGlobal(QPoint(0, 0))

        pos = self._parent.mapFromGlobal(gp)
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self._top_margin

        self._tooltip.move(pos_x, pos_y)
