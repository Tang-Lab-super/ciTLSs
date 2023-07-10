from PySide2.QtWidgets import QPushButton, QDialog, QFileDialog, QVBoxLayout, QLineEdit

class Save_Optics_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Data")
        self.file_name = None
        self.dir_path = None
        self.file_path = None

        self.file_dialog = QFileDialog(self)
        self.file_dialog.setFileMode(QFileDialog.Directory)
        self.file_dialog.setNameFilter("All Files (*)")

        self.text_file_name = QLineEdit(self)
        self.text_dir_path = QLineEdit(self)

        button_select = QPushButton("Select Directory", self)
        button_select.clicked.connect(self.handle_dir_selected)

        button_ok = QPushButton("Save", self)
        button_ok.clicked.connect(self.handle_ok_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.text_file_name)
        layout.addWidget(self.text_dir_path)
        layout.addWidget(button_select)
        layout.addWidget(button_ok)
        self.setLayout(layout)

    def handle_dir_selected(self):
        dir_path = self.file_dialog.getExistingDirectory()
        self.text_dir_path.setText(dir_path)

    def handle_ok_clicked(self):
        self.file_name = self.text_file_name.text()
        self.dir_path = self.text_dir_path.text()
        self.file_path = self.dir_path + '/' + self.file_name
        # 保存文件操作
        self.accept()