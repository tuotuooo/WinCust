import win32gui
import win32process
import win32con
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# 获取可执行文件所在的路径
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
# 加载图标文件
icon_path = os.path.join(base_path, '1.ico')

def enum_windows_callback(hwnd, windows):
    # 检查窗口是否可见
    if win32gui.IsWindowVisible(hwnd):
        # 获取窗口标题
        title = win32gui.GetWindowText(hwnd)

        # 检查窗口标题是否为空
        if title:
            # 获取窗口进程ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # 将窗口信息添加到列表中
            windows.append((title, pid, hwnd))

    return True

def search_windows():
    # 创建一个空列表来存储窗口信息
    windows = []

    # 调用EnumWindows函数遍历所有窗口
    win32gui.EnumWindows(enum_windows_callback, windows)

    return windows

def set_window_opacity(hwnd, opacity):
    # 修改窗口样式，使其支持透明度
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    # 设置窗口透明度
    win32gui.SetLayeredWindowAttributes(hwnd, 0, int(opacity * 255), win32con.LWA_ALPHA)

def set_window_topmost(hwnd):
    # 将窗口置顶
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
def unset_window_topmost(hwnd):
    # 取消窗口置顶
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def on_search_button_click():
    # 清空下拉菜单选项
    window_dropdown['menu'].delete(0, 'end')

    # 搜索窗口
    windows = search_windows()

    # 将窗口信息添加到下拉菜单中
    for title, pid, hwnd in windows:
        menu_label = f"{title} (PID: {pid}, 句柄: {hwnd})"
        window_dropdown['menu'].add_command(label=menu_label, command=lambda title=title, hwnd=hwnd: on_window_selected(title, hwnd))

    # 隐藏默认数据
    window_var.set("数据已更新")

def on_window_selected(title, hwnd):
    # 设置下拉菜单的选中内容
    window_var.set(title)

    # 保存选中的窗口信息
    selected_window['title'] = title
    selected_window['hwnd'] = hwnd

def on_opacity_slider_changed(value):
    # 更新透明度标签
    opacity_label['text'] = f'透明度（0.0-1.0）：{value}'

def on_set_opacity_button_click():
    # 获取选中的窗口信息
    title = selected_window['title']
    hwnd = selected_window['hwnd']

    # 获取滑块的值
    opacity = opacity_slider.get()

    try:
        # 设置窗口透明度
        set_window_opacity(hwnd, float(opacity))

        # 在选定的窗口上显示设置结果
        messagebox.showinfo('设置结果', f'已将透明度设置为 {opacity}，应用于窗口：{title}\n窗口句柄：{hwnd}')
    except Exception as e:
        messagebox.showerror('错误', f'无法设置窗口透明度：{str(e)}')
def on_set_topmost_button_click():
    # 获取选中的窗口信息
    title = selected_window['title']
    hwnd = selected_window['hwnd']

    try:
        # 设置窗口透明度
        set_window_topmost(hwnd)

        # 在选定的窗口上显示设置结果
        messagebox.showinfo('设置结果', f'已将窗口设置为 置顶，应用于窗口：{title}\n窗口句柄：{hwnd}')
    except Exception as e:
        messagebox.showerror('错误', f'无法设置窗口置顶：{str(e)}')
def on_unset_topmost_button_click():
    # 获取选中的窗口信息
    title = selected_window['title']
    hwnd = selected_window['hwnd']

    try:
        # 设置窗口透明度
        unset_window_topmost(hwnd)

        # 在选定的窗口上显示设置结果
        messagebox.showinfo('设置结果', f'已取消窗口设置为 置顶，应用于窗口：{title}\n窗口句柄：{hwnd}')
    except Exception as e:
        messagebox.showerror('错误', f'无法取消窗口置顶：{str(e)}')
# 创建主窗口
root = tk.Tk()
root.title('moyu-tmzd')
root.geometry('300x300')

# 设置窗口图标
root.iconbitmap(icon_path)

# 创建搜索按钮
search_button = tk.Button(root, text='搜索窗口', command=on_search_button_click)
search_button.pack(pady=10)

# 创建窗口下拉菜单
window_var = tk.StringVar()
window_var.set("请先点击“搜索窗口”获取信息")
window_dropdown = ttk.OptionMenu(root, window_var, '')
window_dropdown.pack(fill=tk.X, padx=50, pady=10)

# 创建透明度滑块
opacity_label = tk.Label(root, text='透明度（0.0-1.0）：0.0')
opacity_label.pack()
opacity_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, command=on_opacity_slider_changed)
opacity_slider.pack(padx=10, pady=10)

# 创建设置透明度按钮
set_opacity_button = tk.Button(root, text='设置透明度', command=on_set_opacity_button_click)
set_opacity_button.pack(pady=10)
#设置框架限制
frame = tk.Frame(root)
frame.pack(after=set_opacity_button)
#置顶
set_topmost_button = tk.Button(frame, text='设置置顶', command=on_set_topmost_button_click)
set_topmost_button.pack(padx=10,pady=10,side="left")
#置顶取消
unset_topmost_button = tk.Button(frame, text='取消置顶', command=on_unset_topmost_button_click)
unset_topmost_button.pack(padx=10,pady=10,side="left")

# 保存选中的窗口信息
selected_window = {'title': '', 'hwnd': 0}

# 设置下拉菜单的背景色为纯白色
window_dropdown['menu'].config(bg='white')

# 运行主循环
root.mainloop()
