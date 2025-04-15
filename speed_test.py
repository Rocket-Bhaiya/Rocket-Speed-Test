#!/usr/bin/env python3
import sys
import threading
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
                            QPushButton, QLabel, QProgressBar, QFrame)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette
import speedtest

class SpeedTestThread(QThread):
    """Thread to run speedtest without freezing the UI"""
    update_signal = pyqtSignal(dict)
    
    def run(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            
            # Measure ping
            ping = st.results.ping
            
            # Measure download speed
            download = st.download() / 1_000_000  # Convert to Mbps
            
            # Measure upload speed
            upload = st.upload() / 1_000_000  # Convert to Mbps
            
            # Send results back to main thread
            self.update_signal.emit({
                'ping': round(ping, 2),
                'download': round(download, 2),
                'upload': round(upload, 2)
            })
        except Exception as e:
            self.update_signal.emit({
                'error': str(e)
            })


class RoundedWidget(QFrame):
    """Custom widget with rounded corners"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RoundedWidget")
        self.setStyleSheet("""
            #RoundedWidget {
                background-color: #3D4255;  /* Lighter background color */
                border-radius: 10px;
                padding: 10px;
            }
        """)


class SpeedTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rocket Speed Test")
        self.setMinimumSize(600, 500)
        
        # Set application style
        self.setup_style()
        
        # Initialize UI
        self.init_ui()
        
        # Initialize values
        self.download_speed = 0
        self.upload_speed = 0
        self.ping = 0
        
        # Thread for speedtest
        self.speed_thread = SpeedTestThread()
        self.speed_thread.update_signal.connect(self.update_results)
    
    def setup_style(self):
        """Set up the application style"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(68, 78, 94))  # Lighter background color
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(83, 101, 134))  # Lighter button color
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #7390D3;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5E73AD;
            }
            QPushButton:pressed {
                background-color: #4B5A89;
            }
            QPushButton:disabled {
                background-color: #45526E;
            }
            QProgressBar {
                background-color: #222222;  /* Slightly lighter */
                color: white;
                border-radius: 15px;
                text-align: center;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #7390D3;
                border-radius: 15px;
            }
        """)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title label
        title_label = QLabel("Rocket Speed Test")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Test your internet connection speed")
        desc_label.setFont(QFont("Arial", 12))
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)
        
        # Container for test results
        results_container = RoundedWidget()
        results_layout = QGridLayout(results_container)
        
        # Labels for results
        self.download_label = QLabel("-- Mbps")
        self.download_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.download_label.setAlignment(Qt.AlignCenter)
        
        self.upload_label = QLabel("-- Mbps")
        self.upload_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.upload_label.setAlignment(Qt.AlignCenter)
        
        self.ping_label = QLabel("-- ms")
        self.ping_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.ping_label.setAlignment(Qt.AlignCenter)
        
        # Add labels to grid
        results_layout.addWidget(QLabel("Download"), 0, 0, alignment=Qt.AlignCenter)
        results_layout.addWidget(self.download_label, 1, 0)
        
        results_layout.addWidget(QLabel("Upload"), 0, 1, alignment=Qt.AlignCenter)
        results_layout.addWidget(self.upload_label, 1, 1)
        
        results_layout.addWidget(QLabel("Ping"), 0, 2, alignment=Qt.AlignCenter)
        results_layout.addWidget(self.ping_label, 1, 2)
        
        main_layout.addWidget(results_container)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(30)
        main_layout.addWidget(self.progress_bar)
        
        # Start test button
        self.start_button = QPushButton("Start Test")
        self.start_button.setFixedHeight(50)
        self.start_button.clicked.connect(self.start_test)
        main_layout.addWidget(self.start_button)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFixedHeight(50)
        self.refresh_button.clicked.connect(self.reset_ui)
        main_layout.addWidget(self.refresh_button)
        
        # Set central widget
        self.setCentralWidget(central_widget)
    
    def start_test(self):
        """Start the speed test"""
        self.start_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Reset labels
        self.download_label.setText("Testing...")
        self.upload_label.setText("Testing...")
        self.ping_label.setText("Testing...")
        
        # Start progress animation
        self.progress_animation()
        
        # Start test in separate thread
        self.speed_thread.start()
    
    def progress_animation(self):
        """Animate progress bar during test"""
        self.progress_counter = 0
        
        def update_progress():
            if self.progress_counter < 95:
                self.progress_counter += 1
                self.progress_bar.setValue(self.progress_counter)
                threading.Timer(0.1, update_progress).start()
        
        update_progress()
    
    def update_results(self, results):
        """Update UI with test results"""
        if 'error' in results:
            self.download_label.setText("Error")
            self.upload_label.setText("Error")
            self.ping_label.setText("Error")
        else:
            self.download_speed = results['download']
            self.upload_speed = results['upload']
            self.ping = results['ping']
            
            self.download_label.setText(f"{self.download_speed} Mbps")
            self.upload_label.setText(f"{self.upload_speed} Mbps")
            self.ping_label.setText(f"{self.ping} ms")
        
        # Complete the progress bar
        self.progress_bar.setValue(100)
        self.start_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
    
    def reset_ui(self):
        """Reset UI for a new test"""
        self.download_label.setText("-- Mbps")
        self.upload_label.setText("-- Mbps")
        self.ping_label.setText("-- ms")
        self.progress_bar.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec_())