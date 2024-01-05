import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import win32gui
import win32con
import win32process

def get_expanded_windows_info():
    windows_info = []

    def callback(hwnd, windows_info):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindow(hwnd):
            title = win32gui.GetWindowText(hwnd).strip()
            if title:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                windows_info.append((title, pid))

    win32gui.EnumWindows(callback, windows_info)
    return windows_info

def set_window_transparency(pid, transparency):
    hwnd = None

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0 and win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
            hwnds.append(hwnd)

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        hwnd = hwnds[0]

    if hwnd:
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, transparency, win32con.LWA_ALPHA)
    else:
        messagebox.showerror("错误", "未找到目标窗口")

def main():
    def on_apply_button_click():
        try:
            pid = int(pid_entry.get())
            transparency = int(transparency_entry.get())
            set_window_transparency(pid, transparency)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的PID和透明度")

    def update_window_info():
        window_info_text.delete(1.0, tk.END)
        expanded_windows_info = get_expanded_windows_info()
        for title, pid in expanded_windows_info:
            window_info_text.insert(tk.END, f"应用窗口的标题: {title}\nPID: {pid}\n\n")

    root = tk.Tk()
    root.title("窗口透明度调节")
    root.geometry("400x400")

    window_info_label = ttk.Label(root, text="搜索可视窗口信息")
    window_info_label.pack(pady=10)

    window_info_text = tk.Text(root, height=10, width=40)
    window_info_text.pack()

    update_button = ttk.Button(root, text="更新信息", command=update_window_info)
    update_button.pack(pady=10)

    pid_label = ttk.Label(root, text="PID:")
    pid_label.pack()

    pid_entry = ttk.Entry(root)
    pid_entry.pack()

    transparency_label = ttk.Label(root, text="透明度(0-255):")
    transparency_label.pack()

    transparency_entry = ttk.Entry(root)
    transparency_entry.pack()

    apply_button = ttk.Button(root, text="应用", command=on_apply_button_click)
    apply_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
