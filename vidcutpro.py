#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QMimeData, QTimer
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPalette, QColor, QIcon
from datetime import datetime, timedelta
import os
import platform
from enum import Enum
import ffmpeg


basedir = os.path.abspath(os.path.dirname(__file__))


class OperatingSystem(Enum):
    MACOS = "macOS"
    LINUX = "Linux"
    WINDOWS = "Windows"
    UNKNOWN = "Unknown"

class DropArea(QLabel):
    def __init__(self, parent):
        super().__init__("Drag and drop a file here", parent)
        self.parent = parent
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
            self.setText("File: %s"%file_path)
            event.acceptProposedAction()
            
            # Open the video playback after a delay of 500ms
            QTimer.singleShot(50, lambda: 3) 
            self.parent.open_video_playback(file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.os = self.get_operating_system()
        
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

        # start area
        self.start_label = QLabel("Start:", self)
        timestamp_layout.addWidget(self.start_label)

        self.start_time_edit = QLineEdit(self)
        timestamp_layout.addWidget(self.start_time_edit)

        # end area
        self.end_label = QLabel("End:", self)
        timestamp_layout.addWidget(self.end_label)

        self.end_time_edit = QLineEdit(self)
        timestamp_layout.addWidget(self.end_time_edit)

        main_layout.addWidget(timestamp_widget)

        # speed up factor area
        self.speed_up_label = QLabel("Speed up factor:", self)
        timestamp_layout.addWidget(self.speed_up_label)

        self.speed_up_edit = QLineEdit(self)
        self.speed_up_edit.setText("1.0") 
        timestamp_layout.addWidget(self.speed_up_edit)

        main_layout.addWidget(timestamp_widget)

        # Part 3: Cut button area
        self.cut_button = QPushButton("Process video", self)
        main_layout.addWidget(self.cut_button)

        # Connect button click event to the function that executes the bash command
        self.cut_button.clicked.connect(self.process_video)

    def open_video_playback(self, file_path):
        if self.os == OperatingSystem.MACOS:
            open_cmd = 'open'
        elif self.os == OperatingSystem.LINUX:
            open_cmd = 'xdg-open'
        
        try:
            os.system(f'{open_cmd} "{file_path}"')
        except:
            print("Couldn't open video file")

    def get_operating_system(self):
        system = platform.system()
        if system == "Darwin":
            return OperatingSystem.MACOS
        elif system == "Linux":
            return OperatingSystem.LINUX
        elif system == "Windows":
            return OperatingSystem.WINDOWS
        else:
            return OperatingSystem.UNKNOWN

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

    def speed_up_and_cut_video(self):
        # get time strings
        start_time_string = self.reformat_time_string(self.start_time_edit.text())
        end_time_string = self.reformat_time_string(self.end_time_edit.text())
        # check if both start and end time are valid
        if start_time_string is None:
            start_time_string = "00:00:00.000"
        if end_time_string is None:
            end_time_string = "23:59:59.99"
        start_time = datetime.strptime(start_time_string, '%H:%M:%S.%f')
        end_time = datetime.strptime(end_time_string, '%H:%M:%S.%f')
        duration = end_time - start_time
        duration_string = self.format_duration_or_datetime(duration)
        
        file_in_path = self.file_label.file_path
        suffix = ''

        speed_up_factor = float(self.speed_up_edit.text())
        
        # get file paths
        file_in_base, file_in_extension = self.separate_file_extension(self.file_label.file_path)
        
        # get file paths
        file_in_base, file_in_extension = os.path.splitext(file_in_path)

        # check if speed up factor is between 0.5 and 100
        if (0.5 <= speed_up_factor <= 100) and (speed_up_factor != 1.0):
            file_audio_path = file_in_base + '_audio.aac'
            file_audio_speedup_path = file_in_base + '_audio_speedup.aac'
            file_video_speedup_path = file_in_base + '_video_speedup' + file_in_extension
            file_intermediate = file_in_base + '_intermediate' + file_in_extension
    
            # cut video
            if not((start_time_string == "00:00:00.000") and (end_time_string == "23:59:59.99")):
                do_cut = True
                suffix += '_cut'
                input_args = {'ss': start_time_string, 't': duration_string}
                output_args = {'c': 'copy', 'y': None}
                input_stream = ffmpeg.input(file_in_path, **input_args)
                output_stream = ffmpeg.output(input_stream, file_intermediate, **output_args)
                output_stream.run()
            else:
                do_cut = False
                file_intermediate = file_in_path

            # speed up video without audio
            input_args = {'itsscale': 1.0/speed_up_factor}
            output_args = {'c:v': 'copy', 'an': None, 'y': None}
            input_stream = ffmpeg.input(file_intermediate, **input_args)
            output_stream = ffmpeg.output(input_stream, file_video_speedup_path, **output_args)
            output_stream.run()

            # extract audio
            input_args = {}
            output_args = {'vn': None, 'acodec': 'copy', 'y': None}
            input_stream = ffmpeg.input(file_intermediate, **input_args)
            output_stream = ffmpeg.output(input_stream, file_audio_path, **output_args)
            output_stream.run()

            # speed up audio
            input_args = {}
            output_args = {'filter:a': f'atempo={speed_up_factor}', 'y': None}
            input_stream = ffmpeg.input(file_audio_path, **input_args)
            output_stream = ffmpeg.output(input_stream, file_audio_speedup_path, **output_args)
            output_stream.run()

            # merge audio and video
            suffix += '_speedup'
            file_out_path = file_in_base + suffix + file_in_extension
            input_args = {}
            output_args = {'c:v': 'copy', 'c:a': 'aac', 'map': '0:v:0', 'map': '1:a:0', 'y': None}
            input_video_stream = ffmpeg.input(file_video_speedup_path, **input_args)
            input_audio_stream = ffmpeg.input(file_audio_speedup_path, **input_args)
            output_stream = ffmpeg.output(input_video_stream, input_audio_stream, file_out_path, **output_args)
            output_stream.run()

            # remove intermediate files
            if do_cut:
                os.remove(file_intermediate)
            os.remove(file_video_speedup_path)
            os.remove(file_audio_path)
            os.remove(file_audio_speedup_path)
        else:
            # speed up or cut video without audio
            input_args = {}
            output_args = {'c': 'copy', 'y': None}
            if not((start_time_string == "00:00:00.000") and (end_time_string == "23:59:59.99")):
                input_args.update({'ss': start_time_string, 't': duration_string})
                suffix += '_cut'
            if speed_up_factor != 1.0:
                input_args.update({'itsscale': 1.0/speed_up_factor, 'an': None})
                suffix += '_speedup'
            if input_args:
                file_out_path = file_in_base + suffix + file_in_extension
                input_stream = ffmpeg.input(file_in_path, **input_args)
                output_stream = ffmpeg.output(input_stream, file_out_path, **output_args)
                output_stream.run()
            else:
                os.rename(file_in_path, file_out_path)

    def process_video(self):
        self.cut_button.setText("Processing..."); self.cut_button.repaint()
        self.speed_up_and_cut_video()
        self.cut_button.setText("Done!"); self.cut_button.repaint()

        # notify user of termination
        try:
            if self.os == OperatingSystem.LINUX:
                os.system("notify-send 'Cutting done!'")
            elif self.os == OperatingSystem.MACOS:
                os.system("osascript -e 'display notification \"Cutting done!\" with title \"VidCutPro\"'")
        except:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, 'icon.png')))
    window = MainWindow()
    window.setWindowTitle("VidCutPro")
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec_())
