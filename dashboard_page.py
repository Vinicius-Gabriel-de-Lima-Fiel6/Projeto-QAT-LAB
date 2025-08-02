# pages/dashboard_page.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
         #titulo do painel
        title = QLabel("🔷 Painel Inicial do LabSmartAI")
        title.setStyleSheet("font-size: 24px;font-weight:bold;color: black;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setContentsMargins(0,30,0,0)
        layout.addWidget(title)
        #logo da uea
        self.logouea=QLabel(self)
        pixmapuea=QPixmap('imagens/logouea.png')
        self.logouea.setPixmap(pixmapuea)
        self.logouea.setGeometry(0,0,self.width(),self.height())
        layout.addWidget(self.logouea)
        #imagem de fundo
        self.background_label=QLabel(self)
        background_pixmap=QPixmap('imagens/planodefundolab.jpg')
        self.background_label.setPixmap(background_pixmap)
        self.background_label.setScaledContents(True)
        layout.addWidget(self.background_label)
        self.setLayout(layout)
    def resizeEvent(self,event):
        self.background_label.setGeometry(0,0,self.width(),self.height())
        super().resizeEvent(event)