import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QMimeData, QTimer
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPalette, QColor
import subprocess
from datetime import datetime, timedelta
import os


class DropArea(QLabel):
    def __init__(self, parent):
        super().__init__("Drag and drop a file here", parent)
        self.file_path = ""
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 2px dashed gray; padding: 10px; color: gray;")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.file_path = file_path
            self.setText(f"File: {file_path}")
            event.acceptProposedAction()
            
            QTimer.singleShot(500, lambda: self.open_video_playback(file_path))
    
    def open_video_playback(self, file_path):
        try:
            command = 'flatpak run io.mpv.Mpv "%s"'%file_path
            subprocess.run(command, shell=True, check=True)
        except:
            try:
                command = 'mpv "%s"'%file_path
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print("Error executing the command: %s"%command)
            else:
                print("Bash command executed successfully")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        use_nordic_palette = False
        if use_nordic_palette:
            # Set the "Fusion" style for the application
            QApplication.setStyle("Fusion")

            # Configure the palette to match the Nordic color scheme
            nordic_palette = QPalette()
            nordic_palette.setColor(QPalette.Window, QColor("#2E3440"))          # Background color
            nordic_palette.setColor(QPalette.WindowText, QColor("#D8DEE9"))      # Text color
            nordic_palette.setColor(QPalette.Base, QColor("#3B4252"))            # Base color
            nordic_palette.setColor(QPalette.AlternateBase, QColor("#434C5E"))   # Alternate base color
            nordic_palette.setColor(QPalette.ToolTipBase, QColor("#D8DEE9"))      # ToolTip background color
            nordic_palette.setColor(QPalette.ToolTipText, QColor("#2E3440"))      # ToolTip text color
            nordic_palette.setColor(QPalette.Text, QColor("#E5E9F0"))             # Text color
            nordic_palette.setColor(QPalette.Button, QColor("#4C566A"))          # Button color
            nordic_palette.setColor(QPalette.ButtonText, QColor("#E5E9F0"))      # Button text color
            nordic_palette.setColor(QPalette.BrightText, QColor("#ECEFF4"))       # Bright text color
            nordic_palette.setColor(QPalette.Link, QColor("#88C0D0"))            # Link color
            nordic_palette.setColor(QPalette.Highlight, QColor("#5E81AC"))       # Highlight color
            nordic_palette.setColor(QPalette.HighlightedText, QColor("#ECEFF4"))  # Highlighted text color

            self.setPalette(nordic_palette)
        
        # Create the main widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create the main layout
        main_layout = QVBoxLayout(main_widget)

        # Part 1: Drag and drop file area
        self.file_label = DropArea(self)
        main_layout.addWidget(self.file_label)

        # Part 2: Start and End timestamp area
        timestamp_widget = QWidget(self)
        timestamp_layout = QHBoxLayout(timestamp_widget)

        self.start_label = QLabel("Start:", self)
        timestamp_layout.addWidget(self.start_label)

        self.start_time_edit = QLineEdit(self)
        timestamp_layout.addWidget(self.start_time_edit)

        self.end_label = QLabel("End:", self)
        timestamp_layout.addWidget(self.end_label)

        self.end_time_edit = QLineEdit(self)
        timestamp_layout.addWidget(self.end_time_edit)

        main_layout.addWidget(timestamp_widget)

        # Part 3: Cut button area
        self.cut_button = QPushButton("Cut", self)
        main_layout.addWidget(self.cut_button)

        # Connect button click event to the function that executes the bash command
        self.cut_button.clicked.connect(self.execute_bash_command)

    def reformat_time_string(self, input_time):
        # Check if the input_time contains a colon
        if ':' not in input_time:
            # If there is no colon, it is in seconds
            try:
                total_seconds = float(input_time)
                hours = int(total_seconds / 3600)
                minutes = int((total_seconds % 3600) / 60)
                seconds = total_seconds % 60
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
                return formatted_time
            except ValueError:
                # Handle the case where the input time is not a valid number
                return None

        # Split the input_time by colon to get hours, minutes, and seconds
        time_components = input_time.split(':')
        num_components = len(time_components)

        # Initialize the time components to 0
        hours, minutes, seconds = 0, 0, 0.0

        if num_components == 2:
            # If there is one colon, read minutes and seconds
            try:
                minutes, seconds = map(float, time_components)
                formatted_time = "%02d:%02d:%06.3f"%(hours, minutes, seconds)
                return formatted_time
            except ValueError:
                # Handle the case where the input time is not in a valid format
                return None

        elif num_components == 3:
            # If there are three components, assume it's in the format "HH:MM:SS"
            try:
                hours, minutes, seconds = map(float, time_components)
                formatted_time = "%02d:%02d:%06.3f"%(hours, minutes, seconds)
                return formatted_time
            except ValueError:
                # Handle the case where the input time is not in a valid format
                return None

        # Handle the case where the input_time is not in a recognized format
        return None

    def format_duration_or_datetime(self,duration_or_datetime):
        if isinstance(duration_or_datetime, timedelta):
            # For timedelta objects
            total_seconds = duration_or_datetime.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = total_seconds % 60
            milliseconds = (duration_or_datetime.microseconds) if duration_or_datetime.microseconds else 0
            formatted_time = "%02d:%02d:%02d.%03d"%(hours, minutes, seconds, milliseconds)
            # f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
            return formatted_time
        elif isinstance(duration_or_datetime, datetime):
            # For datetime objects
            total_seconds = duration_or_datetime.hour * 3600 + duration_or_datetime.minute * 60 + duration_or_datetime.second
            hours = duration_or_datetime.hour
            minutes = duration_or_datetime.minute
            seconds = duration_or_datetime.second
            milliseconds = (duration_or_datetime.microsecond) if duration_or_datetime.microsecond else 0
            formatted_time = "%02d:%02d:%02d.%03d"%(hours, minutes, seconds, milliseconds)
            return formatted_time
        else:
            # Invalid input type
            return None

    def separate_file_extension(self, file_path):
        base_name, file_extension = os.path.splitext(file_path)
        return base_name, file_extension

    def execute_bash_command(self):
        # Replace the command with your desired bash command
        start_time = datetime.strptime(self.reformat_time_string(self.start_time_edit.text()), '%H:%M:%S.%f')
        end_time = datetime.strptime(self.reformat_time_string(self.end_time_edit.text()), '%H:%M:%S.%f')
        duration = end_time - start_time
        file_in_base, file_in_extension = self.separate_file_extension(self.file_label.file_path)
        file_out_path = file_in_base + '_cut' + file_in_extension
        
        command = 'ffmpeg -i "%s" -ss %s -t %s -c copy "%s" -y'%(
            self.file_label.file_path,
            self.format_duration_or_datetime(start_time),
            self.format_duration_or_datetime(duration),
            file_out_path)

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print("Error executing the command: %s"%self.file_label.file_path)
        else:
            subprocess.run("notify-send 'Cutting done!'", shell=True, check=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("VidCutPro")
    window.resize(800, 300)
    window.show()
    sys.exit(app.exec_())
