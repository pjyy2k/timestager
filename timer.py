import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
import time
from screeninfo import get_monitors

class OverlayTimer:
    def __init__(self, root):
        self.root = root
        self.timer_running = False
        self.start_time = None
        self.elapsed_time = 0.0
        self.blinking = False
        self.blink_status = False
        self.monitors = get_monitors()
        self.current_monitor = self.monitors[0]

        # 오버레이 시계 설정
        self.clock = Toplevel(root)
        self.clock.overrideredirect(True)
        self.clock.attributes('-topmost', True)
        self.clock.config(bg='white')
        self.clock.attributes('-alpha', 0.7)

        self.label = tk.Label(self.clock, text="00:00:00.0", font=("Helvetica", 18, "bold"), bg='white', fg="black")
        self.label.pack()
        self.message_label = tk.Label(self.clock, text="", font=("Helvetica", 12, "bold"), bg='white', fg="red")
        self.message_label.pack(fill=tk.BOTH, expand=True)

        self.position_clock(self.current_monitor)
        self.clock.bind("<Button-1>", self.activate_control_window)

        # 컨트롤 창 설정
        self.control_window = Toplevel(root)
        self.control_window.title("Timer Controls by.JinYoungPark")
        self.control_window.protocol("WM_DELETE_WINDOW", self.on_control_window_close)

        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')  # 테마 선택
        style.configure('TButton', font=('Helvetica', 12), padding=5)
        style.configure('TFrame', background='white')

        # UI 구성
        self.setup_ui()

        self.update_time()

    def setup_ui(self):
        monitor_frame = ttk.Frame(self.control_window)
        monitor_frame.pack(fill=tk.X, padx=10, pady=10)
        control_frame = ttk.Frame(self.control_window)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        text_frame = ttk.Frame(self.control_window)
        text_frame.pack(fill=tk.X, padx=10, pady=10)

        for i, monitor in enumerate(self.monitors):
            btn = ttk.Button(monitor_frame, text=f"Monitor {i+1}", command=lambda m=monitor: self.set_monitor(m))
            btn.pack(side=tk.LEFT, expand=True, padx=2)

        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, expand=True, padx=2)
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, expand=True, padx=2)
        self.reset_button = ttk.Button(control_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, expand=True, padx=2)

        self.text_entry = ttk.Entry(text_frame)
        self.text_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.publish_button = ttk.Button(text_frame, text="Publish", command=self.publish_text)
        self.publish_button.pack(side=tk.LEFT, padx=2)
        self.blink_button = ttk.Button(text_frame, text="Blink", command=self.toggle_blink)
        self.blink_button.pack(side=tk.LEFT, padx=2)

    def set_monitor(self, monitor):
        self.current_monitor = monitor
        self.position_clock(monitor)

    def position_clock(self, monitor):
        window_width = max(200, self.message_label.winfo_reqwidth() + 20)
        window_height = 100
        x = monitor.x + monitor.width - window_width - 10
        y = 10
        self.clock.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def update_time(self):
        if self.timer_running and self.start_time is not None:
            elapsed = time.time() - self.start_time
            self.elapsed_time += elapsed
            self.start_time = time.time()
        minutes, seconds = divmod(self.elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(seconds * 10 % 10)}"
        self.label.config(text=formatted_time)
        self.root.after(100, self.update_time)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()

    def stop_timer(self):
        self.timer_running = False
        self.start_time = None

    def reset_timer(self):
        self.timer_running = False
        self.elapsed_time = 0.0
        self.label.config(text="00:00:00.0")
        self.message_label.config(text="", bg="white")
        self.blinking = False
        self.blink_status = False

    def publish_text(self):
        message = self.text_entry.get()
        self.message_label.config(text=message)
        self.position_clock(self.current_monitor)

    def toggle_blink(self):
        self.blinking = not self.blinking
        if not self.blinking:
            self.message_label.config(bg="white")  # Reset to default background if blinking is turned off
        self.blink()

    def blink(self):
        if self.blinking:
            self.blink_status = not self.blink_status
            self.message_label.config(bg="yellow" if self.blink_status else "white")
            self.root.after(500, self.blink)

    def activate_control_window(self, event):
        if self.control_window.state() == 'withdrawn':
            self.control_window.deiconify()
        self.control_window.lift()
        self.control_window.focus_force()

    def on_control_window_close(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    root.withdraw()
    app = OverlayTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
