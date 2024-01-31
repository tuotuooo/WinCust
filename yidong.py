import win32gui
import win32con
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QPalette, QColor, QIcon
import sys
import os

# 获取可执行文件所在的路径
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
# 加载图标文件
icon_path = os.path.join(base_path, '1.ico')
def get_visible_window_titles():
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and len(win32gui.GetWindowText(hwnd)) > 0:
            hwnds.append((hwnd, win32gui.GetWindowText(hwnd)))
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

class WindowSyncApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口位置同步工具")
        self.setWindowIcon(QIcon(icon_path))  # 替换成你自己的图标文件路径
        self.resize(400, 300)  # 设置窗口大小
        layout = QVBoxLayout()

        self.search_button = QPushButton("搜索窗口")
        self.search_button.clicked.connect(self.search_windows)
        layout.addWidget(self.search_button)

        self.info_label = QLabel("请先点击“搜索窗口”获取信息")
        layout.addWidget(self.info_label)

        self.hwnd_a_label = QLabel("跟随窗口A:")
        layout.addWidget(self.hwnd_a_label)
        self.hwnd_a_combobox = QComboBox()
        self.hwnd_a_combobox.currentIndexChanged.connect(self.clear_info)
        layout.addWidget(self.hwnd_a_combobox)

        self.hwnd_b_label = QLabel("移动窗口B:")
        layout.addWidget(self.hwnd_b_label)
        self.hwnd_b_combobox = QComboBox()
        self.hwnd_b_combobox.currentIndexChanged.connect(self.clear_info)
        layout.addWidget(self.hwnd_b_combobox)

        self.start_button = QPushButton("开始同步")
        self.start_button.clicked.connect(self.start_synchronize_thread)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("停止同步")
        self.stop_button.clicked.connect(self.stop_synchronize_thread)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def get_window_position(self, hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        width = rect[2] - x
        height = rect[3] - y
        return x, y, width, height

    def search_windows(self):
        hwnds = get_visible_window_titles()
        self.hwnd_a_combobox.clear()
        self.hwnd_a_combobox.addItem("请选择窗口A", -1)  # 设置默认项
        self.hwnd_b_combobox.clear()
        self.hwnd_b_combobox.addItem("请选择窗口B", -1)  # 设置默认项
        for hwnd, title in hwnds:
            self.hwnd_a_combobox.addItem(f"{title}", hwnd)
            self.hwnd_b_combobox.addItem(f"{title}", hwnd)
        self.set_default_style(self.hwnd_a_combobox, "请选择窗口A")
        self.set_default_style(self.hwnd_b_combobox, "请选择窗口B")
        self.info_label.setText("数据已更新")

    def start_synchronize_thread(self):
        self.synchronize_flag = True
        synchronize_thread = threading.Thread(target=self.synchronize_window_position)
        synchronize_thread.start()

    def stop_synchronize_thread(self):
        self.synchronize_flag = False

    def synchronize_window_position(self):
        hwnd_a = self.hwnd_a_combobox.currentData()
        hwnd_b = self.hwnd_b_combobox.currentData()
        x_a, y_a, width_a, height_a = self.get_window_position(hwnd_a)
        x_b, y_b, width_b, height_b = self.get_window_position(hwnd_b)
        offset_x = x_a - x_b
        offset_y = y_a - y_b

        while self.synchronize_flag:
            x_b, y_b, width_b, height_b = self.get_window_position(hwnd_b)
            x_a_target = x_b + offset_x
            y_a_target = y_b + offset_y
            win32gui.SetWindowPos(hwnd_a, win32con.HWND_TOP, x_a_target, y_a_target, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

    def clear_info(self):
        self.info_label.setText("")

    def set_default_style(self, combobox, default_text):
        index = combobox.findText(default_text)
        if index >= 0:
            combobox.model().item(index).setEnabled(False)
            palette = QPalette()
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(150, 150, 150))
            combobox.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_sync_app = WindowSyncApp()
    window_sync_app.show()
    sys.exit(app.exec_())
