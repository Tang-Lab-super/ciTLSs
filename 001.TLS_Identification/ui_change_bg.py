from PySide2.QtWidgets import QPushButton, QDialog, QFileDialog, QVBoxLayout, QLineEdit

class Change_BG_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Image")
        self.file_path = None

        self.file_dialog = QFileDialog(self)
        self.file_dialog.setFileMode(QFileDialog.ExistingFile)
        self.file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg *.tif)")

        self.text_input = QLineEdit(self)

        button_select = QPushButton("Select", self)
        button_select.clicked.connect(self.handle_file_selected)

        button_ok = QPushButton("OK", self)
        button_ok.clicked.connect(self.handle_ok_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.file_dialog)
        layout.addWidget(self.text_input)
        layout.addWidget(button_select)
        layout.addWidget(button_ok)
        self.setLayout(layout)

    def handle_file_selected(self):
        file_path, _ = self.file_dialog.getOpenFileName()
        self.text_input.setText(file_path)

    def handle_ok_clicked(self):
        self.file_path = self.text_input.text()
        self.accept()