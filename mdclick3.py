import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import pyautogui
import schedule

class TimePickerDialog(tk.Toplevel):
    def __init__(self, parent, current_time):
        super().__init__(parent)
        self.title("Pelago - Select Execution Time")
        self.configure(bg='#FFFFFF')
        self.resizable(False, False)
        self.geometry(f"+{parent.winfo_x()+150}+{parent.winfo_y()+150}")

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TCombobox', background='#FFFFFF', font=("Inter", 12))
        
        try:
            hours, minutes, seconds = current_time.split(':')
        except:
            hours, minutes, seconds = ('08', '59', '59')

        # Time selection widgets
        tk.Label(self, text="Hours:", bg='#FFFFFF', fg="#212121", font=("Inter", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.hours_combo = ttk.Combobox(self, values=[f"{i:02d}" for i in range(24)], width=4)
        self.hours_combo.set(hours)
        self.hours_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Minutes:", bg='#FFFFFF', fg="#212121", font=("Inter", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.minutes_combo = ttk.Combobox(self, values=[f"{i:02d}" for i in range(60)], width=4)
        self.minutes_combo.set(minutes)
        self.minutes_combo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self, text="Seconds:", bg='#FFFFFF', fg="#212121", font=("Inter", 12)).grid(row=0, column=4, padx=5, pady=5)
        self.seconds_combo = ttk.Combobox(self, values=[f"{i:02d}" for i in range(60)], width=4)
        self.seconds_combo.set(seconds)
        self.seconds_combo.grid(row=0, column=5, padx=5, pady=5)

        # Action buttons
        button_frame = tk.Frame(self, bg='#FFFFFF')
        button_frame.grid(row=1, column=0, columnspan=6, pady=10)

        tk.Button(button_frame, text="Cancel", font=("Inter", 12), bg="#B0BEC5", fg="black",
                 relief="flat", command=self.destroy).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Set Time", font=("Inter", 12), bg="#2196F3", fg="white",
                 relief="flat", command=self.validate_time).pack(side=tk.RIGHT, padx=10)

        self.transient(parent)
        self.grab_set()

    def validate_time(self):
        try:
            time_str = f"{self.hours_combo.get()}:{self.minutes_combo.get()}:{self.seconds_combo.get()}"
            time.strptime(time_str, "%H:%M:%S")
            self.parent_time_var = time_str
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Time", "Please select valid time values", parent=self)

class AutoMouseClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Pelago Mouse Scheduler")
        self.root.geometry("600x450")
        self.root.configure(bg='#FFFFFF')
        
        self.locations = []
        self.execution_time = "08:59:59"

        # Header Section
        header_frame = tk.Frame(root, bg="#E3F2FD", height=60)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Pelago Mouse Scheduler", font=("Inter", 16, "bold"), 
                bg="#E3F2FD", fg="#0D47A1").pack(pady=15)

        # Location Management
        content_frame = tk.Frame(root, bg="#FFFFFF")
        content_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(content_frame, height=5, width=40, font=("Inter", 12), 
                               bg="#FAFAFA", bd=2, relief="solid", selectbackground="#BBDEFB")
        self.listbox.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='ew')

        self.add_button = tk.Button(content_frame, text="➕ Pick Location", font=("Inter", 12), 
                                  bg="#4CAF50", fg="white", relief="flat", command=self.pick_location)
        self.add_button.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

        self.delete_button = tk.Button(content_frame, text="🗑 Delete Selected", font=("Inter", 12), 
                                     bg="#F44336", fg="white", relief="flat", command=self.delete_location)
        self.delete_button.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        # Time Scheduling Section
        time_frame = tk.Frame(root, bg="#FFFFFF")
        time_frame.pack(pady=10, fill=tk.X)

        tk.Label(time_frame, text="Scheduled Execution:", font=("Inter", 12), 
                bg='#FFFFFF', fg="#212121").pack(side=tk.LEFT)
        
        self.time_display = tk.Label(time_frame, text=self.execution_time, 
                                   font=("Inter", 12, "bold"), bg='#FFFFFF', fg="#0D47A1")
        self.time_display.pack(side=tk.LEFT, padx=5)

        self.change_time_button = tk.Button(root, text="⏱ Change Time", font=("Inter", 12), 
                                          bg="#2196F3", fg="white", relief="flat", 
                                          command=self.change_execution_time)
        self.change_time_button.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(root, text="▶ Start Scheduler", font=("Inter", 14, "bold"), 
                                    bg="#FFC107", fg="black", relief="flat", command=self.start_scheduler)
        self.start_button.pack(pady=20, ipadx=20, ipady=10)

        # Maker Info
        maker_frame = tk.Frame(root, bg="#FFFFFF")
        maker_frame.pack(fill=tk.X, pady=5)

        maker_label = tk.Label(maker_frame, text="Made by Amnas Ahamed | amnasahmd@gmail.com", 
                               font=("Inter", 10), bg="#FFFFFF", fg="#606060")
        maker_label.pack(pady=2)

        # Configure grid weights
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)

    def pick_location(self):
        if len(self.locations) >= 5:
            messagebox.showwarning("Limit Reached", "Maximum 5 locations allowed")
            return

        self.root.withdraw()
        self.root.config(cursor="crosshair")

        overlay = tk.Toplevel(self.root)
        overlay.configure(bg='black')
        overlay.attributes('-alpha', 0.01)
        overlay.attributes('-fullscreen', True)
        overlay.attributes('-topmost', True)
        overlay.grab_set()
        overlay.configure(cursor="crosshair")

        def on_click(event):
            x, y = event.x_root, event.y_root
            self.locations.append((x, y))
            self.listbox.insert(tk.END, f"({x}, {y})")
            overlay.destroy()
            self.root.config(cursor="")
            self.root.deiconify()

        overlay.bind('<Button-1>', on_click)

    def delete_location(self):
        try:
            selected_index = self.listbox.curselection()[0]
            self.locations.pop(selected_index)
            self.listbox.delete(selected_index)
        except IndexError:
            messagebox.showinfo("No Selection", "Please select a location to delete")

    def change_execution_time(self):
        dialog = TimePickerDialog(self.root, self.execution_time)
        self.root.wait_window(dialog)
        if hasattr(dialog, 'parent_time_var'):
            self.execution_time = dialog.parent_time_var
            self.time_display.config(text=self.execution_time)

    def execute_clicks(self):
        for x, y in self.locations:
            pyautogui.click(x, y)
            time.sleep(0.5)

    def start_scheduler(self):
        if not self.locations:
            messagebox.showwarning("No Locations", "Please add at least one location")
            return

        try:
            schedule.every().day.at(self.execution_time).do(self.execute_clicks)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid time format: {str(e)}")
            return

        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(1)

        threading.Thread(target=run_schedule, daemon=True).start()
        messagebox.showinfo("Scheduler Started", 
                          f"Clicking will occur daily at {self.execution_time}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoMouseClicker(root)
    root.mainloop()