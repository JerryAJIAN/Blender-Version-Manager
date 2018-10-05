import os
import shutil
import subprocess
import time

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QSizePolicy

import resources_rc


class B3dItemLayout(QHBoxLayout):
    def __init__(self, root_folder, version, is_latest, parent):
        super(B3dItemLayout, self).__init__(None)
        self.root_folder = root_folder
        self.version = version
        self.parent = parent

        ts = os.path.getctime(os.path.join(
            root_folder, version, "blender.exe"))
        date = time.strftime("%d-%b-%Y", time.gmtime(ts))
        self.btnOpen = QPushButton(
            (version.split('-',)[-2]).replace("git.", "Git-") + " | " + date)
        self.btnOpen.clicked.connect(
            lambda: subprocess.Popen(os.path.join(root_folder, version, "blender.exe")))

        if (is_latest):
            self.btnOpen.setIcon(parent.star_icon)

        self.btnDelete = QPushButton(parent.trash_icon, "")
        self.btnDelete.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.btnDelete.clicked.connect(lambda: self.delete())

        self.addWidget(self.btnOpen)
        self.addWidget(self.btnDelete)

    def delete(self):
        delete = QMessageBox.question(
            self.parent, "Warning", "Are you sure you want to delete '" + self.version + "' from disk?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if delete == QMessageBox.Yes:
            shutil.rmtree(os.path.join(self.root_folder, self.version))
            self.parent.draw_versions_layout()