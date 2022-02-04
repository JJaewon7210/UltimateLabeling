from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QComboBox, QLabel
from PyQt5.QtCore import Qt
from ultimatelabeling.models import KeyboardListener, StateListener
from .class_editor import ClassEditor
from .action_editor import ActionEditor


class InfoDetection(QGroupBox, StateListener, KeyboardListener):
    def __init__(self, state):
        super().__init__("Info")

        self.state = state
        self.state.add_listener(self)

        self.class_editor = ClassEditor(self.state, self)
        self.action_editor = ActionEditor(self.state, self)

        self.block_listener = False

        self.show_kps_bbox_checkbox = QCheckBox("Show keypoint bboxes", self)
        self.show_kps_bbox_checkbox.setCheckState(Qt.Checked if self.state.keypoints_show_bbox else Qt.Unchecked)
        self.show_kps_bbox_checkbox.stateChanged.connect(lambda state: self.state.set_keypoints_show_bbox(state == Qt.Checked))

        self.kps_instance_color_checkbox = QCheckBox("Color keypoints by instance", self)
        self.kps_instance_color_checkbox.setCheckState(Qt.Checked if self.state.keypoints_instance_color else Qt.Unchecked)
        self.kps_instance_color_checkbox.stateChanged.connect(lambda state: self.state.set_keypoints_instance_color(state == Qt.Checked))

        self.bbox_class_color_checkbox = QCheckBox("Color bboxes by class", self)
        self.bbox_class_color_checkbox.setCheckState(Qt.Checked if self.state.bbox_class_color else Qt.Unchecked)
        self.bbox_class_color_checkbox.stateChanged.connect(lambda state: self.state.set_bbox_class_color(state == Qt.Checked))

        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.show_kps_bbox_checkbox)
        checkboxes_layout.addWidget(self.kps_instance_color_checkbox)
        checkboxes_layout.addWidget(self.bbox_class_color_checkbox)

        class_layout = QHBoxLayout()
        self.class_id_dropdown = QComboBox()
        self.class_id_dropdown.addItems(self._get_class_names())
        self.class_id_dropdown.currentIndexChanged.connect(self.class_id_changed)
        self.edit_classes_button = QPushButton("Edit")
        self.edit_classes_button.clicked.connect(self.edit_classes_clicked)
        class_layout.addWidget(QLabel("Class:"))
        class_layout.addWidget(self.class_id_dropdown)
        class_layout.addWidget(self.edit_classes_button)

        action_layout = QHBoxLayout()
        self.action_id_dropdown = QComboBox()
        self.action_id_dropdown.addItems(self._get_action_names())
        self.action_id_dropdown.currentIndexChanged.connect(self.action_id_changed)
        self.edit_actions_button = QPushButton("Edit")
        self.edit_actions_button.clicked.connect(self.edit_actions_clicked)
        action_layout.addWidget(QLabel("Action:"))
        action_layout.addWidget(self.action_id_dropdown)
        action_layout.addWidget(self.edit_actions_button)

        self.nb_track_ids = 0
        instance_layout = QHBoxLayout()
        self.instance_id_dropdown = QComboBox()
        self.instance_id_dropdown.addItems(self._get_track_ids())
        self.instance_id_dropdown.currentIndexChanged.connect(self.instance_id_changed)
        instance_layout.addWidget(QLabel("Instance ID:"))
        instance_layout.addWidget(self.instance_id_dropdown)

        layout = QVBoxLayout()
        layout.addLayout(checkboxes_layout)
        layout.addLayout(class_layout)
        layout.addLayout(action_layout)
        layout.addLayout(instance_layout)
        self.setLayout(layout)

    def edit_classes_clicked(self):
        self.class_editor.update()
        self.class_editor.show()

    def edit_actions_clicked(self):
        self.action_editor.update()
        self.action_editor.show()

    def class_editor_closed(self):
        print("class_editor_closed")
        self.on_video_change()

    def action_editor_closed(self):
        print("action_editor_closed")
        self.on_video_change()

    def on_key_number(self, number):
        # self.class_id_changed(class_id=number)
        # self.action_id_changed(action_id=number)
        pass

    def on_key_ws(self, go_up):
        if self.state.current_detection:
            # class_id = self.state.current_detection.class_id
            # class_names = list(self.state.track_info.class_names)
            # i = class_names.index(class_id)
            # new_i = (i + (1 if go_up else -1)) % len(class_names)
            # self.class_id_changed(i=new_i)

            # action_id = self.state.current_detection.action_id
            # action_names = list(self.state.track_info.action_names)
            # i = action_names.index(action_id)
            # new_i = (i + (1 if go_up else -1)) % len(action_names)
            # self.action_id_changed(i=new_i)
            pass

    def _get_track_ids(self):
        self.nb_track_ids = self.state.track_info.nb_track_ids

        return [str(id) for id in range(self.nb_track_ids)]

    def _get_class_names(self):
        class_names = self.state.track_info.class_names

        return ["{} ({})".format(k, cl) for k, cl in class_names.items()]

    def _get_action_names(self):
        action_names = self.state.track_info.action_names

        return ["{} ({})".format(k, cl) for k, cl in action_names.items()]

    def class_id_changed(self, i=-1, class_id=-1):
        if self.state.current_detection:

            if i >= 0:
                class_id = list(self.state.track_info.class_names)[i]

            if class_id >= 0:
                self.block_listener = True
                self.state.modify_class_id_and_future(self.state.current_detection, class_id)
                self.block_listener = False

    def action_id_changed(self, i=-1, action_id=-1):
        if self.state.current_detection:

            if i >= 0:
                action_id = list(self.state.track_info.action_names)[i]

            if action_id >= 0:
                self.block_listener = True
                self.state.modify_action_id_and_future(self.state.current_detection, action_id)
                self.block_listener = False

    def instance_id_changed(self, i):
        if self.state.current_detection and i >= 0:
            self.state.current_detection.track_id = i

            self.block_listener = True
            self.state.notify_listeners("on_detection_change")
            self.block_listener = False

    def on_detection_change(self):
        if not self.block_listener:
            detection = self.state.current_detection

            self.instance_id_dropdown.blockSignals(True); 
            self.class_id_dropdown.blockSignals(True)
            self.action_id_dropdown.blockSignals(True)

            self.instance_id_dropdown.clear()
            self.instance_id_dropdown.addItems(self._get_track_ids())

            if detection:
                instance_id = detection.track_id
                class_index = list(self.state.track_info.class_names).index(detection.class_id)
                action_index = list(self.state.track_info.action_names).index(detection.action_id)

                self.instance_id_dropdown.setCurrentIndex(instance_id)
                self.class_id_dropdown.setCurrentIndex(class_index)
                self.action_id_dropdown.setCurrentIndex(action_index)

            self.instance_id_dropdown.blockSignals(False)
            self.class_id_dropdown.blockSignals(False)
            self.action_id_dropdown.blockSignals(False)

    def on_video_change(self):
        if not self.block_listener:
            self.instance_id_dropdown.blockSignals(True) 
            self.class_id_dropdown.blockSignals(True)
            self.action_id_dropdown.blockSignals(True)

            self.class_id_dropdown.clear()
            self.action_id_dropdown.clear()
            self.class_id_dropdown.addItems(self._get_class_names())
            self.action_id_dropdown.addItems(self._get_action_names())
            self.instance_id_dropdown.clear()
            self.instance_id_dropdown.addItems(self._get_track_ids())

            self.instance_id_dropdown.blockSignals(False) 
            self.class_id_dropdown.blockSignals(False)
            self.action_id_dropdown.blockSignals(False)

