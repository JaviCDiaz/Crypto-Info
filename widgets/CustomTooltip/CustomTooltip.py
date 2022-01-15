from utils.QtCore import *


class CustomTooltip(QLabel):
    def __init__(
        self,
        parent,
        tooltip_text,
        tooltip_bg_color,
        tooltip_text_color,
        tooltip_border_color
    ):
        super().__init__()

        self.setParent(parent)
        self.setObjectName(u"label_tooltip")
        self.setMinimumHeight(34)
        
        self.setText(tooltip_text)

        self.setStyleSheet(f""" 
            QLabel {{		
                background-color: {tooltip_bg_color};	
                color: {tooltip_text_color};
                padding-left: 10px;
                padding-right: 10px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                border-bottom: 3px solid {tooltip_border_color};
                font: 800 9pt "Segoe UI";
            }}
        """)
        
        self.adjustSize()