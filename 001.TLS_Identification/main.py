import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QCheckBox, QSpinBox, QPushButton
from PySide2.QtWidgets import QPinchGesture, QGestureEvent
from basic_class import *
from ui_mainwindow import Ui_MainWindow
from ui_optics_dialog import Ui_Optics_Dialog
from range_slider_dialog import RangeSliderDialog
from ui_change_bg import Change_BG_Dialog
from ui_download_optics import Save_Optics_Dialog
from collections import OrderedDict
import numpy as np
import pandas as pd


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.optics_colors = None
        self.bg_pixmap = None
        self.bg_pixmap_shape = None
        self.data_lists = None
        self.n = None
        self.auxiliary_views = None
        self.key_optics = None
        self.keys_continuous = None
        self.optics_params_dict = None
        self.images = []
        # 获得item列表
        self.bg_pixmap_items = []
        self.auxiliary_items = OrderedDict()
        self.merge_item = QGraphicsPixmapItem()
        self.scene_merge = QGraphicsScene()
        self.scene_main = None
        self.show_optics = False
        self.actionoptics.triggered.connect(self.show_optics_dialog)
        self.actionthreshold.triggered.connect(self.show_continuous_dialog)
        self.actionchangebg.triggered.connect(self.change_bg_dialog)
        self.actiondraw.triggered.connect(self.show_draw_dialog)
        self.actionddownloadoptics.triggered.connect(self.show_download_optics_dialog)
        self.grabGesture(Qt.PinchGesture)

    def load_data(self, image_path, data_paths: dict, optics_colors_path='colors.txt'):
        self.bg_pixmap = QPixmap(image_path)
        self.data_lists = OrderedDict(data_paths)
        for data in data_paths:
            self.data_lists[data]['data'] = pd.read_csv(self.data_lists[data]['path'], index_col=0).values
        self.optics_colors = np.loadtxt(optics_colors_path, dtype='uint8', delimiter=',')
        self.setup()

    def setup(self):
        self.n = len(self.data_lists)
        self.bg_pixmap_shape = [self.bg_pixmap.width(), self.bg_pixmap.height()]
        self.bg_pixmap_items = OrderedDict(zip(list(self.data_lists) + ['main', 'merge'],
                                               [QGraphicsPixmapItem(self.bg_pixmap) for _ in range(self.n + 2)]))
        # 获得副图视窗数目和列表
        self.auxiliary_views = OrderedDict(zip(list(self.data_lists),
                                               [getattr(self, f"graphicsView_{i + 1}") for i in range(self.n)]))
        self.key_optics = [key for key, value in data_paths.items() if value['type'] == 'Optics'][0]
        self.keys_continuous = [key for key, value in data_paths.items() if value['type'] == 'Continuous']

        [getattr(self, f"label_{i + 1}").setText(value) for i, value in enumerate(self.data_lists)]

    def run(self):
        for data in self.data_lists:
            optics_bool = False
            if self.data_lists[data]['type'] == 'Optics':
                item = OpticsPixmapItem(input_array=self.data_lists[data]['data'][:, 0:2],
                                        image_width_height=self.bg_pixmap_shape,
                                        eps_samples=[2, 8],
                                        colors=self.optics_colors)
                optics_bool = True
            elif self.data_lists[data]['type'] == 'Continuous':
                item = ContinuousPixmapItem(input_array=self.data_lists[data]['data'],
                                            image_width_height=self.bg_pixmap_shape,
                                            truncation_range=[95, 99],
                                            color_gradient=['blue', 'orange', 'red'])
            elif self.data_lists[data]['type'] == 'Uniform':
                item = UniformPixmapItem(input_array=self.data_lists[data]['data'],
                                         image_width_height=self.bg_pixmap_shape)
            else:
                print('no type')
            self.set_scene(view=self.auxiliary_views[data], item=item,
                           bg_item=self.bg_pixmap_items[data], optics=optics_bool)
            self.auxiliary_items[data] = item

        self.merge_image()
        self.scene_merge.addItem(self.bg_pixmap_items['merge'])
        self.scene_merge.addItem(self.merge_item.original_item)
        self.graphicsView_merge.setScene(self.scene_merge)
        self.graphicsView_merge.mousePressEvent = lambda event: self.cover_main(self.merge_item)

        self.scene_main = MainScene(image_width_height=self.bg_pixmap_shape, colors=self.optics_colors)
        self.scene_main.addItem(self.bg_pixmap_items['main'])
        self.graphicsView_main.setScene(self.scene_main)

    def set_scene(self, view, item, bg_item, optics=False):
        scene = QGraphicsScene()
        scene.addItem(bg_item)
        scene.addItem(item.original_item)
        view.setScene(scene)
        view.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        view.mousePressEvent = lambda event: self.update_main(item, optics)

    def merge_image(self, update=False):
        merge_data = np.sum([item.image_bool for item in self.auxiliary_items.values()], axis=0).astype('float64')
        if update:
            self.merge_item.update(df_new=merge_data)
        else:
            self.merge_item = MergePixmapItem(input_array=merge_data, image_width_height=self.bg_pixmap_shape, color_gradient=['grey', 'orange', 'red'])

    def show_optics_dialog(self):
        dialog = QDialog(self)
        dialog_ui = Ui_Optics_Dialog()
        dialog_ui.setupUi(dialog)
        self.optics_params_dict = {
            '5 points': {'max_eps': 1, 'range': (2, 5)},
            '9 points': {'max_eps': 1.5, 'range': (2, 9)},
            '13 points': {'max_eps': 2, 'range': (2, 13)},
            '21 points': {'max_eps': 2.5, 'range': (2, 21)},
        }
        dialog_ui.comboBox.currentIndexChanged.connect(lambda: self.update_min_samples_options(dialog_ui))
        dialog_ui.spinBox.valueChanged.connect(lambda: self.cluster_and_draw(item=self.auxiliary_items[self.key_optics],
                                                                             dialog_ui=dialog_ui))
        dialog_ui.close_button.clicked.connect(lambda: self.optics_closing_operation(item=self.auxiliary_items[self.key_optics]))
        dialog.show()

    def update_min_samples_options(self, dialog_ui):
        option = dialog_ui.comboBox.currentText()
        range_min, range_max = self.optics_params_dict[option]['range']
        dialog_ui.spinBox.setRange(range_min, range_max)
        dialog_ui.spinBox.setDisabled(False)

    def cluster_and_draw(self, item, dialog_ui=None):
        min_samples = dialog_ui.spinBox.value()
        option = dialog_ui.comboBox.currentText()
        max_eps = self.optics_params_dict[option]['max_eps']
        item.update([max_eps, min_samples])
        self.merge_image(update=True)
        self.scene_main.label_data = item.label_data if self.show_optics else None

    def optics_closing_operation(self, item):
        item.close_update()
        self.merge_image(update=True)
        self.scene_main.label_data = item.label_data if self.show_optics else None

    def show_continuous_dialog(self):
        num_sliders = len(self.keys_continuous)
        continuous_dialog_ui = RangeSliderDialog(num_sliders, [85, 100], self)
        continuous_dialog_ui.show()

        for num in range(num_sliders):
            item = self.auxiliary_items[self.keys_continuous[num]]
            slider = continuous_dialog_ui.sliders[num]
            slider.startValueChanged.connect(
                lambda value, item=item, slider=slider: self.threshold_and_draw(item, slider))
            slider.endValueChanged.connect(
                lambda value, item=item, slider=slider: self.threshold_and_draw(item, slider))

    def threshold_and_draw(self, item, slider=None):
        item.update([slider._start / 100 * 15 + 85, slider._end / 100 * 15 + 85])
        self.merge_image(update=True)

    def change_bg_dialog(self):
        dialog = Change_BG_Dialog(self)
        dialog.accepted.connect(self.change_bg)
        dialog.show()

    def change_bg(self):
        dialog = self.sender()
        image_path = dialog.file_path
        self.bg_pixmap = QPixmap(image_path)
        self.bg_pixmap_items['main'].setPixmap(self.bg_pixmap)
        # 更换全部背景
        # for item in self.bg_pixmap_items.values():
        #     item.setPixmap(self.bg_pixmap)
        dialog.deleteLater()

    def show_draw_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Drawing Settings')
        layout = QVBoxLayout(dialog)
        checkbox = QCheckBox('Enable Drawing', dialog)
        checkbox.setChecked(self.scene_main.draw_enabled)
        checkbox.stateChanged.connect(self.set_draw_enabled)
        layout.addWidget(checkbox)

        colorSpinBox = QSpinBox(dialog)
        colorSpinBox.setMinimum(0)
        colorSpinBox.setMaximum(410)
        colorSpinBox.setValue(self.scene_main.currentPenColorIndex)
        colorSpinBox.valueChanged.connect(self.set_current_pen_color_index)
        layout.addWidget(colorSpinBox)

        button = QPushButton('Confirm Drawing', dialog)
        button.clicked.connect(self.confirm_drawing)
        layout.addWidget(button)

        button = QPushButton('Cancel Drawing', dialog)
        button.clicked.connect(self.cancel_drawing)
        layout.addWidget(button)

        dialog.show()

    def set_draw_enabled(self, state):
        self.scene_main.draw_enabled = state == Qt.Checked

    def set_current_pen_color_index(self, index):
        self.scene_main.currentPenColorIndex = index
        self.scene_main.get_color()

    def confirm_drawing(self):
        self.auxiliary_items[self.key_optics].points_update(self.scene_main.points)
        self.scene_main.points = {}
        self.merge_image(update=True)

    def cancel_drawing(self):
        self.scene_main.points = {}

    def show_download_optics_dialog(self):
        dialog = Save_Optics_Dialog(self)
        dialog.accepted.connect(self.download_optics)
        dialog.show()

    def download_optics(self):
        dialog = self.sender()
        file_path = dialog.file_path
        label_data = self.auxiliary_items[self.key_optics].label_data
        optics_result = np.row_stack((np.where(label_data != 0), label_data[np.where(label_data != 0)])).T
        np.savetxt(file_path, optics_result, delimiter="\t", fmt="%d")
        dialog.deleteLater()

    def event(self, event):
        if isinstance(event, QGestureEvent):
            return self.gestureEvent(event)
        return super(MainWindow, self).event(event)

    def gestureEvent(self, event):
        gesture = event.gesture(Qt.PinchGesture)
        if isinstance(gesture, QPinchGesture):
            self.pinchTriggered(gesture)
            return True
        return False

    def pinchTriggered(self, gesture):
        views_with_main = list(self.auxiliary_views.values()) + [self.graphicsView_main]
        scale_factor = gesture.scaleFactor()
        if scale_factor > 1:
            for view in views_with_main:
                view.scale(1.1, 1.1)
        else:
            for view in views_with_main:
                view.scale(0.9, 0.9)

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        all_views = list(self.auxiliary_views.values()) + [self.graphicsView_merge, self.graphicsView_main]
        for view in all_views:
            view.fitInView(view.scene().itemsBoundingRect(), Qt.KeepAspectRatio)

    def cover_main(self, item):
        self.scene_main = MainScene(image_width_height=self.bg_pixmap_shape, colors=self.optics_colors)
        [auxiliary_item.delete('clone_main') for auxiliary_item in self.auxiliary_items.values() if 'clone_main' in auxiliary_item.clone_items]
        self.scene_main.addItem(self.bg_pixmap_items['main'])
        self.graphicsView_main.setScene(self.scene_main)
        if 'clone_main' in item.clone_items:
            item.delete('clone_main')
        else:
            item.clone('clone_main')
            self.scene_main.addItem(item.clone_items['clone_main'])
        self.scene_main.show_optics = self.show_optics = False
        self.graphicsView_main.optics_label.setText(None)

    def update_main(self, item, optics):
        if 'clone_main' in item.clone_items:
            self.scene_main.removeItem(item.clone_items['clone_main'])
            item.delete('clone_main')
        else:
            item.clone('clone_main')
            self.scene_main.addItem(item.clone_items['clone_main'])
        if optics:
            if self.show_optics:
                self.graphicsView_main.optics_label.setText(None)
            self.show_optics = not self.show_optics
            self.scene_main.show_optics = self.show_optics
            self.scene_main.label_data = item.label_data


if __name__ == '__main__':
    app = QApplication()

    mainWindow = MainWindow()
    image_path = './data/HCC04_T_ssDNA.tif'

    data_paths = {
        'Optics': {'type': 'Optics', 'path': './data/HCC04_T_coor_TLS.csv'},
        'Immune cells': {'type': 'Uniform', 'path': './data/HCC04_T_coor_TLS.csv'},
        'TLS markers scores': {'type': 'Continuous', 'path': './data/HCC04_T_TLSmarkers_scores.csv'},
        'Chemokine scores': {'type': 'Continuous', 'path': './data/HCC04_T_chemokine_scores.csv'},
        'Hotspot': {'type': 'Continuous', 'path': './data/HCC04_T_hotspot.csv'},
        'Region': {'type': 'Uniform', 'path': './data/HCC04_T_coor_bin50.csv'}
    }
    mainWindow.load_data(image_path, data_paths)
    mainWindow.run()
    mainWindow.show()

    sys.exit(app.exec_())
