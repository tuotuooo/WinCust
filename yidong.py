import win32gui
import win32con

def get_window_position(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    width = rect[2] - x
    height = rect[3] - y
    return x, y, width, height

def set_window_position(hwnd, x, y, width, height):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, 0)

def synchronize_window_position(hwnd_a, hwnd_b):
    x_a, y_a, width_a, height_a = get_window_position(hwnd_a)
    x_b, y_b, width_b, height_b = get_window_position(hwnd_b)
    offset_x = x_a - x_b
    offset_y = y_a - y_b

    while True:
        x_b, y_b, width_b, height_b = get_window_position(hwnd_b)
        x_a_target = x_b + offset_x
        y_a_target = y_b + offset_y
        set_window_position(hwnd_a, x_a_target, y_a_target, width_a, height_a)

# 使用示例
hwnd_a = xxxx  # 已知A窗口的句柄
hwnd_b = xxxx  # 已知B窗口的句柄
synchronize_window_position(hwnd_a, hwnd_b)
