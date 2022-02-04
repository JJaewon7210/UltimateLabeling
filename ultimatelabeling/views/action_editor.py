from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QGroupBox, QStyle, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread
from ultimatelabeling.models import KeyboardListener, FrameMode
import time


class ActionEditor(QWidget):
    def __init__(self, state, info_detection):
        super().__init__()

        self.state = state
        self.info_detection = info_detection

        self.table = QTableWidget()
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_empty_row)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selected_rows)

        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.update_editor()

    def update_editor(self):
        self.action_names = self.state.track_info.action_names.copy()

        self.table.setRowCount(len(self.action_names))
        self.table.setColumnCount(2)

        for row, key in enumerate(self.action_names):
            value = self.action_names[key]

            self.table.setItem(row, 0, QTableWidgetItem(str(key)))
            self.table.setItem(row, 1, QTableWidgetItem(value))

    def closeEvent(self, event):
        action_names = dict()

        for row in range(self.table.rowCount()):
            key, value = int(self.table.item(row, 0).text()), self.table.item(row, 1).text()
            action_names[key] = value

        self.state.track_info.action_names = action_names

        self.info_detection.action_editor_closed()

    def add_empty_row(self):
        self.table.insertRow(self.table.rowCount())

    def delete_selected_rows(self):

        selected_items = self.table.selectedItems()
        selected_rows = set()

        for item in selected_items:
            selected_rows.add(item.row())

        selected_rows = sorted(list(selected_rows))

        for row in reversed(selected_rows):
            self.table.removeRow(row)
