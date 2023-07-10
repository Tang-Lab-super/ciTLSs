from PySide2.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsItemGroup, QGraphicsRectItem
from PySide2.QtGui import QPixmap, QImage, QColor
from PySide2.QtCore import Qt
import numpy as np
from matplotlib import colors as mcolors
import cv2
from sklearn.cluster import OPTICS

class QGraphicsPixmapItemManager:
    def __init__(self, input_array: np.array, image_width_height: list):
        self.data = input_array
        self.image_width = image_width_height[0]
        self.image_height = image_width_height[1]
        self.opacity = 0.5
        self.image_data = None
        self.image_bool = None
        self.clone_items = {}
        self.original_item = QGraphicsPixmapItem(self.make_pixmap())
        self.original_item.setOpacity(self.opacity)

    def make_pixmap(self):
        self.data2image()
        return self.image2pixmap()

    def data2image(self):
        self.image_data = np.zeros((self.image_height, self.image_width, 4), dtype=np.uint8)
        self.image_data[self.data[:, 0].astype(int), self.data[:, 1].astype(int), :] = [255, 0, 0, 255]
        self.image_bool = np.where(self.image_data > 0, 1, 0)

    def image2pixmap(self):
        qimage = QImage(self.image_data.data, self.image_width, self.image_height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap

    def clone(self, name):
        clone_item = QGraphicsPixmapItem(self.original_item.pixmap())
        clone_item.setOpacity(self.opacity)
        self.clone_items[name] = clone_item

    def delete(self, name):
        del self.clone_items[name]

    def update(self, df_new):
        self.data = df_new
        self._update(self.make_pixmap())

    def _update(self, pixmap):
        self.original_item.setPixmap(pixmap)
        for clone_item in self.clone_items.values():
            clone_item.setPixmap(pixmap)


class OpticsPixmapItem(QGraphicsPixmapItemManager):
    def __init__(self, eps_samples: list, colors=None, **kwargs):
        self.colors_list = colors
        self.max_eps = eps_samples[0]
        self.min_samples = eps_samples[1]
        self.label_data = None
        self.label_num = None
        self.kernel_size = 3
        super().__init__(**kwargs)
        self.opacity = 1

    def data2image(self):
        self.image_data = np.zeros((self.image_height, self.image_width, 4), dtype=np.uint8)
        optics = OPTICS(max_eps=self.max_eps, min_samples=self.min_samples, algorithm='auto', n_jobs=1)
        optics.fit(self.data)
        labels = optics.labels_
        self.label_num = np.max(labels) + 1
        colors = np.array([self.colors_list[label] if label != -1 else (0, 0, 0, 0) for label in labels])
        self.image_data[self.data[:, 0], self.data[:, 1]] = colors
        self.image_bool = np.where(self.image_data > 0, 1, 0)
        labels += 1
        self.label_data = np.zeros((530, 530), dtype=int)
        self.label_data[self.data[:, 0], self.data[:, 1]] = labels

    def closing_operation(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.kernel_size, self.kernel_size))
        image_result = np.zeros_like(self.image_data, dtype='uint8')
        label_result = np.zeros_like(self.label_data, dtype='uint8')
        for n_cluster in range(1, self.label_num+1):
            cluster_img = np.zeros_like(self.label_data, dtype='uint8')
            cluster_img[np.where(self.label_data == n_cluster)] = 255
            cluster_img_close = cv2.morphologyEx(np.uint8(cluster_img), cv2.MORPH_CLOSE, kernel)
            contours, hierarchy = cv2.findContours(cluster_img_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            label_rst = cv2.drawContours(np.zeros_like(self.label_data, dtype='uint8'), contours, -1, int(n_cluster), -1)
            image_rst = np.zeros_like(self.image_data, dtype='uint8')
            image_rst[np.nonzero(label_rst)] = self.colors_list[n_cluster-1]
            image_result += image_rst
            label_result += label_rst
        self.image_data = image_result
        self.label_data = label_result

    def update(self, eps_samples_new):
        self.max_eps = eps_samples_new[0]
        self.min_samples = eps_samples_new[1]
        self._update(self.make_pixmap())

    def points_update(self, points: dict):
        for key, value in points.items():
            if value['value'] == 0:
                self.label_data[key] = 0
                self.image_data[key] = (0, 0, 0, 0)
                self.image_bool[key] = 0
            else:
                self.label_data[key] = value['value']
                self.image_data[key] = value['color']
                self.image_bool[key] = 1
        self._update(self.image2pixmap())

    def close_update(self):
        self.closing_operation()
        self._update(self.image2pixmap())


class ContinuousPixmapItem(QGraphicsPixmapItemManager):
    def __init__(self, truncation_range: list, color_gradient: list, **kwargs):
        self.lower_threshold = truncation_range[0]
        self.upper_threshold = truncation_range[1]
        self.color_gradient = color_gradient
        self.cmap_range = mcolors.LinearSegmentedColormap.from_list('score_cmap', self.color_gradient)
        super().__init__(**kwargs)

    def data2image(self):
        data = self.data.copy()
        self.image_data = np.zeros((self.image_height, self.image_width, 4), dtype=np.uint8)
        min_value, max_value = np.percentile(data[:, 2], [self.lower_threshold, self.upper_threshold])
        data = data[data[:, 2] > min_value]
        data[:, 2] = np.clip(data[:, 2], None, max_value)
        norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
        rgba_color = (self.cmap_range(norm(data[:, 2])) * 255).astype('uint8')
        self.image_data[data[:, 0].astype(int), data[:, 1].astype(int), :] = rgba_color
        self.image_bool = np.where(self.image_data > 0, 1, 0)

    def update(self, truncation_range_new):
        self.lower_threshold = truncation_range_new[0]
        self.upper_threshold = truncation_range_new[1]
        self._update(self.make_pixmap())


class UniformPixmapItem(QGraphicsPixmapItemManager):
    pass


class MergePixmapItem(QGraphicsPixmapItemManager):
    def __init__(self, color_gradient: list, **kwargs):
        self.color_gradient = color_gradient
        self.cmap_range = mcolors.LinearSegmentedColormap.from_list('score_cmap', self.color_gradient)
        super().__init__(**kwargs)
        self.opacity = 0.8

    def data2image(self):
        data = self.data.copy()
        non_zero_indices = np.nonzero(data)
        data[non_zero_indices] /= np.max(data[non_zero_indices])
        color_mapped_data = self.cmap_range(data[non_zero_indices])
        self.image_data = np.zeros((self.image_width, self.image_height, 4))
        self.image_data[non_zero_indices[0], non_zero_indices[1], :] = color_mapped_data
        self.image_data *= (255.0 / np.max(self.image_data))
        self.image_data = self.image_data.astype('uint8')


class MainScene(QGraphicsScene):
    def __init__(self, image_width_height: list, colors=None):
        super(MainScene, self).__init__()
        self.setSceneRect(0, 0, image_width_height[0], image_width_height[1])
        self.colors = colors
        self.previousPos = None
        self.currentGroup = None
        self.current_color = None
        self.points = {}
        self.current_property = {}
        self.draw_enabled = True
        self.show_optics = False
        self.label_data = None
        self.currentPenColorIndex = 1
        self.get_color()

    def mousePressEvent(self, event):
        if self.draw_enabled and event.button() == Qt.LeftButton and self.show_optics:
            self.current_property = {'value': self.currentPenColorIndex,
                                     'color': self.colors[self.currentPenColorIndex - 1]}
            self.previousPos = event.scenePos()
            self.currentGroup = QGraphicsItemGroup()
            self.addItem(self.currentGroup)
            # 绘制初始矩形
            rect = QGraphicsRectItem(int(self.previousPos.x()), int(self.previousPos.y()), 1, 1)
            rect.setPen(Qt.NoPen)
            rect.setBrush(self.current_color)
            self.currentGroup.addToGroup(rect)
            self.points[(int(self.previousPos.y()), int(self.previousPos.x()))] = self.current_property

    def mouseMoveEvent(self, event):
        if self.show_optics:
            currentPos = event.scenePos()
            label = self.label_data[int(currentPos.y()), int(currentPos.x())]
            self.views()[0].optics_label.setText(f"Label: {label}")
            if self.draw_enabled and event.buttons() & Qt.LeftButton:
                if self.previousPos:
                    x1, y1 = int(self.previousPos.x()), int(self.previousPos.y())
                    x2, y2 = int(currentPos.x()), int(currentPos.y())

                    dx = abs(x2 - x1)
                    dy = abs(y2 - y1)
                    sx = -1 if x1 > x2 else 1
                    sy = -1 if y1 > y2 else 1
                    err = dx - dy

                    while x1 != x2 or y1 != y2:
                        self.points[(y1, x1)] = self.current_property
                        rect = QGraphicsRectItem(x1, y1, 1, 1)
                        rect.setPen(Qt.NoPen)
                        rect.setBrush(self.current_color)
                        self.currentGroup.addToGroup(rect)

                        err2 = 2 * err
                        if err2 > -dy:
                            err -= dy
                            x1 += sx
                        if err2 < dx:
                            err += dx
                            y1 += sy

                    self.previousPos = currentPos

    def mouseReleaseEvent(self, event):
        if self.draw_enabled and event.button() == Qt.LeftButton and self.show_optics:
            self.removeItem(self.currentGroup)
            self.previousPos = None
            self.currentGroup = None

    def get_color(self):
        if self.currentPenColorIndex == 0:
            self.current_color = QColor(255, 255, 255, 200)
        else:
            self.current_color = QColor(*self.colors[self.currentPenColorIndex - 1])


