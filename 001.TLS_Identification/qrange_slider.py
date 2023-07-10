from PySide2 import QtWidgets, QtCore, QtGui


class QRangeSlider(QtWidgets.QWidget):
    startValueChanged = QtCore.Signal(float)
    endValueChanged = QtCore.Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._start = 0
        self._end = 100
        self._handleSize = 20
        self._handleHovered = None
        self._handlePressed = None
        self._rangeRect = QtCore.QRect()
        self._handleRects = {}

        self.setMinimumSize(100, 40)
        self.setMouseTracking(True)

    def setRange(self, start, end):
        if start < end:
            self._start = start
            self._end = end
        else:
            self._start = end
            self._end = start

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Draw background and range
        bgRect = self.rect().adjusted(0, self._handleSize // 2, 0, -self._handleSize // 2)
        painter.fillRect(bgRect, QtGui.QColor(180, 180, 180))

        self._rangeRect = QtCore.QRect(
            self._valueToPos(self._start), self._handleSize // 2,
            self._valueToPos(self._end) - self._valueToPos(self._start), self.height() - self._handleSize
        )
        painter.fillRect(self._rangeRect, QtGui.QColor(100, 184, 255))

        # Draw handles
        self._handleRects = {
            "start": QtCore.QRect(self._valueToPos(self._start), 0, self._handleSize, self.height()),
            "end": QtCore.QRect(self._valueToPos(self._end) - self._handleSize, 0, self._handleSize, self.height())
        }

        for handle, rect in self._handleRects.items():
            if handle == self._handleHovered or handle == self._handlePressed:
                color = QtGui.QColor(32, 124, 202)
            else:
                color = QtGui.QColor(0, 96, 160)

            painter.setBrush(color)
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 32), 1))
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            for handle, rect in self._handleRects.items():
                if rect.contains(event.pos()):
                    self._handlePressed = handle
                    break

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._handlePressed = None

    def mouseMoveEvent(self, event):
        hoveredHandle = None

        for handle, rect in self._handleRects.items():
            if rect.contains(event.pos()):
                hoveredHandle = handle
                break

        if hoveredHandle != self._handleHovered:
            self._handleHovered = hoveredHandle
            self.setCursor(QtCore.Qt.SizeHorCursor if hoveredHandle else QtCore.Qt.ArrowCursor)

        if self._handlePressed:
            pos = event.pos().x()
            pos = max(pos, self._handleSize // 2)
            pos = min(pos, self.width() - self._handleSize // 2)

            if self._handlePressed == "start":
                pos = min(pos, self._valueToPos(self._end) - self._handleSize)
                self._start = self._posToValue(pos)
                self.startValueChanged.emit(self._start)
            elif self._handlePressed == "end":
                pos = max(pos, self._valueToPos(self._start) + self._handleSize)
                self._end = self._posToValue(pos)
                self.endValueChanged.emit(self._end)

            self.update()

    def _valueToPos(self, value):
        return (value - 0) / (100 - 0) * (self.width() - self._handleSize) + self._handleSize // 2

    def _posToValue(self, pos):
        return (pos - self._handleSize // 2) / (self.width() - self._handleSize) * (100 - 0) + 0
