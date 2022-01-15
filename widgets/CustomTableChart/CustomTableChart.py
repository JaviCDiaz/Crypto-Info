from utils.QtCore import *


class CustomTableChart (QChartView):
    def __init__(
        self,
        data: QSplineSeries(),
        max_value = 0,
        min_value = 0,
        line_color = '#03a66d'
    ):
        super().__init__()

        self.setRenderHint(QPainter.Antialiasing)
        self.setContentsMargins(0,0,0,0)
        self.setMinimumSize(150,50)
        self.setMaximumSize(150,50)

        series = data
        series_pen = QPen(QColor(line_color))
        series_pen.setWidth(2)
        series.setPen(series_pen)

        self.table_chart = QChart()
        self.table_chart.addSeries(series)

        self.table_chart.legend().hide()
        self.table_chart.setPlotArea(QRectF(0,10,150,40))
        self.table_chart.createDefaultAxes()
        self.table_chart.axisY().setRange(min_value,max_value)
        self.table_chart.axisY().hide()
        self.table_chart.axisX().hide()
        self.table_chart.setBackgroundBrush(QColor(Qt.transparent))

        self.setChart(self.table_chart)