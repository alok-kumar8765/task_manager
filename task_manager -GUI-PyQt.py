import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTimer


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Task Manager (PyQt)")
        self.setGeometry(200, 200, 300, 150)

        self.label = QLabel("Loading...", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def update_stats(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()

        self.label.setText(
            f"CPU Usage : {cpu}%\n"
            f"Memory    : {mem.percent}%"
        )


def main():
    app = QApplication(sys.argv)
    win = TaskManager()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
