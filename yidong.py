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

# 已知A窗口的句柄
hwnd_a = xxxx

# 已知B窗口的句柄
hwnd_b = xxxx

# 获取A窗口的初始位置
x_a, y_a, width_a, height_a = get_window_position(hwnd_a)

# 获取B窗口的初始位置
x_b, y_b, width_b, height_b = get_window_position(hwnd_b)

# 计算A窗口与B窗口的初始偏移量
offset_x = x_a - x_b
offset_y = y_a - y_b

while True:
    # 获取B窗口的当前位置
    x_b, y_b, width_b, height_b = get_window_position(hwnd_b)

    # 计算A窗口的目标位置
    x_a_target = x_b + offset_x
    y_a_target = y_b + offset_y

    # 设置A窗口的位置
    set_window_position(hwnd_a, x_a_target, y_a_target, width_a, height_a)

