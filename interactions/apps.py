import sys
import os
import base64
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint
import requests
import pyautogui

class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selection_start = QPoint()
        self.selection_end = QPoint()
        self.is_selecting = False
        
    def initUI(self):
        self.setWindowTitle('Screenshot App')
        self.setGeometry(300, 300, 300, 250)
        
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        self.fullScreenBtn = QPushButton('Full Screen', self)
        self.fullScreenBtn.clicked.connect(self.capture_full_screenshot)
        button_layout.addWidget(self.fullScreenBtn)
        
        self.selectionBtn = QPushButton('Selection', self)
        self.selectionBtn.clicked.connect(self.start_selection)
        button_layout.addWidget(self.selectionBtn)
        
        layout.addLayout(button_layout)
        
        self.statusLabel = QLabel('Ready', self)
        layout.addWidget(self.statusLabel)
        
        self.previewLabel = QLabel(self)
        self.previewLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.previewLabel)
        
        self.setLayout(layout)
        
    def capture_full_screenshot(self):
        self.statusLabel.setText('Capturing full screen...')
        QTimer.singleShot(1000, self._delayed_capture)
        
    def _delayed_capture(self):
        screenshot = pyautogui.screenshot()
        self.save_and_process_screenshot(screenshot)
        
    def start_selection(self):
        self.statusLabel.setText('Select area...')
        self.setWindowOpacity(0.3)
        screen = QApplication.primaryScreen()
        self.original_screenshot = screen.grabWindow(0)
        self.showFullScreen()
        self.setMouseTracking(True)
        
    def save_and_process_screenshot(self, screenshot):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(os.path.expanduser("~"), "Screenshots", filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        screenshot.save(filepath)
        
        self.display_preview(filepath)
        self.transfer_image(filepath)
        
    def display_preview(self, filepath):
        pixmap = QPixmap(filepath)
        scaled_pixmap = pixmap.scaled(280, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.previewLabel.setPixmap(scaled_pixmap)
        
    def transfer_image(self, filepath):
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this picture:"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_string}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 100,
            "stream": False
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_API_KEY_HERE"
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            response_filepath = filepath.replace('.png', '_response.json')
            with open(response_filepath, 'w') as f:
                json.dump(response_data, f, indent=2)
            self.statusLabel.setText('Image transferred and response saved')
        else:
            self.statusLabel.setText(f'Error: {response.status_code}')
            
    def mousePressEvent(self, event):
        if self.isFullScreen() and event.button() == Qt.LeftButton:
            self.selection_start = event.pos()
            self.selection_end = event.pos()
            self.is_selecting = True

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.selection_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.is_selecting:
            self.selection_end = event.pos()
            self.is_selecting = False
            self.capture_selection()

    def paintEvent(self, event):
        if self.isFullScreen():
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.original_screenshot)
            if self.is_selecting:
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                painter.drawRect(QRect(self.selection_start, self.selection_end))

    def capture_selection(self):
        x = min(self.selection_start.x(), self.selection_end.x())
        y = min(self.selection_start.y(), self.selection_end.y())
        width = abs(self.selection_start.x() - self.selection_end.x())
        height = abs(self.selection_start.y() - self.selection_end.y())
        
        selected_area = self.original_screenshot.copy(x, y, width, height)
        self.save_and_process_screenshot(selected_area)
        
        self.setWindowOpacity(1)
        self.showNormal()
        self.setMouseTracking(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotApp()
    ex.show()
    sys.exit(app.exec_())