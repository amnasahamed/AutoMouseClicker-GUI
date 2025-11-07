"""
Auto Mouse Clicker - Professional macOS Automation Tool

A feature-rich auto mouse clicker with scheduling, persistent configuration,
and comprehensive logging for macOS.

Author: Amnas Ahamed
Email: amnasahmd@gmail.com
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Tuple, Optional, Dict, Any
import time
import threading
import pyautogui
import schedule
import json
import os
from datetime import datetime
from pathlib import Path

# Constants
CONFIG_FILE = "clicker_config.json"
MAX_LOCATIONS = 100  # Configurable limit
DEFAULT_EXECUTION_TIME = "08:59:59"
CLICK_DELAY = 0.5
LOG_MAX_LINES = 1000

# Configure PyAutoGUI safety features
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1


class TimePickerDialog(tk.Toplevel):
    """Dialog for selecting execution time with hour, minute, and second dropdowns."""

    def __init__(self, parent: tk.Tk, current_time: str) -> None:
        """
        Initialize the time picker dialog.

        Args:
            parent: Parent window
            current_time: Current time in HH:MM:SS format
        """
        super().__init__(parent)
        self.title("Select Execution Time")
        self.configure(bg='#FFFFFF')
        self.resizable(False, False)
        self.geometry(f"+{parent.winfo_x()+150}+{parent.winfo_y()+150}")

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TCombobox', background='#FFFFFF', font=("SF Pro", 12))

        try:
            hours, minutes, seconds = current_time.split(':')
        except ValueError:
            hours, minutes, seconds = ('08', '59', '59')

        # Time selection widgets
        tk.Label(self, text="Hours:", bg='#FFFFFF', fg="#212121",
                font=("SF Pro", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.hours_combo = ttk.Combobox(self, values=[f"{i:02d}" for i in range(24)], width=4)
        self.hours_combo.set(hours)
        self.hours_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Minutes:", bg='#FFFFFF', fg="#212121",
                font=("SF Pro", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.minutes_combo = ttk.Combobox(self, values=[f"{i:02d}" for i in range(60)], width=4)
        self.minutes_combo.set(minutes)
        self.minutes_combo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self, text="Seconds:", bg='#FFFFFF', fg="#212121",
                font=("SF Pro", 12)).grid(row=0, column=4, padx=5, pady=5)
        self.seconds_combo = ttk.Combobox(self, values=[f"{i:02d}" for i in range(60)], width=4)
        self.seconds_combo.set(seconds)
        self.seconds_combo.grid(row=0, column=5, padx=5, pady=5)

        # Action buttons
        button_frame = tk.Frame(self, bg='#FFFFFF')
        button_frame.grid(row=1, column=0, columnspan=6, pady=10)

        tk.Button(button_frame, text="Cancel", font=("SF Pro", 12), bg="#B0BEC5", fg="black",
                 relief="flat", command=self.destroy).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Set Time", font=("SF Pro", 12), bg="#007AFF", fg="white",
                 relief="flat", command=self.validate_time).pack(side=tk.RIGHT, padx=10)

        self.transient(parent)
        self.grab_set()

        self.parent_time_var: Optional[str] = None

    def validate_time(self) -> None:
        """Validate and save the selected time."""
        try:
            time_str = f"{self.hours_combo.get()}:{self.minutes_combo.get()}:{self.seconds_combo.get()}"
            time.strptime(time_str, "%H:%M:%S")
            self.parent_time_var = time_str
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Time", "Please select valid time values", parent=self)


class ClickTypeDialog(tk.Toplevel):
    """Dialog for configuring click type and delay for each location."""

    def __init__(self, parent: tk.Tk, current_type: str = "left",
                 current_delay: float = CLICK_DELAY) -> None:
        """
        Initialize the click type configuration dialog.

        Args:
            parent: Parent window
            current_type: Current click type (left, double, right)
            current_delay: Current delay after click in seconds
        """
        super().__init__(parent)
        self.title("Configure Click")
        self.configure(bg='#FFFFFF')
        self.resizable(False, False)
        self.geometry(f"+{parent.winfo_x()+150}+{parent.winfo_y()+150}")

        self.result: Optional[Dict[str, Any]] = None

        # Click type selection
        tk.Label(self, text="Click Type:", bg='#FFFFFF', fg="#212121",
                font=("SF Pro", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.click_type_var = tk.StringVar(value=current_type)

        types_frame = tk.Frame(self, bg='#FFFFFF')
        types_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        tk.Radiobutton(types_frame, text="Single Click", variable=self.click_type_var,
                      value="left", bg='#FFFFFF', font=("SF Pro", 11)).pack(anchor='w')
        tk.Radiobutton(types_frame, text="Double Click", variable=self.click_type_var,
                      value="double", bg='#FFFFFF', font=("SF Pro", 11)).pack(anchor='w')
        tk.Radiobutton(types_frame, text="Right Click", variable=self.click_type_var,
                      value="right", bg='#FFFFFF', font=("SF Pro", 11)).pack(anchor='w')

        # Delay configuration
        tk.Label(self, text="Delay After Click (seconds):", bg='#FFFFFF', fg="#212121",
                font=("SF Pro", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.delay_var = tk.DoubleVar(value=current_delay)
        delay_spinbox = tk.Spinbox(self, from_=0.1, to=10.0, increment=0.1,
                                  textvariable=self.delay_var, font=("SF Pro", 12), width=10)
        delay_spinbox.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        # Action buttons
        button_frame = tk.Frame(self, bg='#FFFFFF')
        button_frame.grid(row=4, column=0, pady=15)

        tk.Button(button_frame, text="Cancel", font=("SF Pro", 12), bg="#B0BEC5", fg="black",
                 relief="flat", command=self.destroy).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Apply", font=("SF Pro", 12), bg="#34C759", fg="white",
                 relief="flat", command=self.apply_settings).pack(side=tk.RIGHT, padx=10)

        self.transient(parent)
        self.grab_set()

    def apply_settings(self) -> None:
        """Apply the selected settings."""
        self.result = {
            'type': self.click_type_var.get(),
            'delay': self.delay_var.get()
        }
        self.destroy()


class AutoMouseClicker:
    """Main application class for the Auto Mouse Clicker."""

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the Auto Mouse Clicker application.

        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Auto Mouse Clicker Pro")
        self.root.geometry("700x700")
        self.root.configure(bg='#F5F5F7')

        # Application state
        self.locations: List[Dict[str, Any]] = []
        self.execution_time: str = DEFAULT_EXECUTION_TIME
        self.scheduler_running: bool = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.stop_scheduler_flag: threading.Event = threading.Event()

        # Load saved configuration
        self.load_config()

        # Build UI
        self._build_ui()

        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _build_ui(self) -> None:
        """Build the user interface."""
        # Header Section
        header_frame = tk.Frame(self.root, bg="#007AFF", height=70)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="🖱 Auto Mouse Clicker Pro",
                font=("SF Pro Display", 20, "bold"),
                bg="#007AFF", fg="#FFFFFF").pack(pady=20)

        # Main content with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Locations
        locations_tab = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(locations_tab, text="📍 Locations")
        self._build_locations_tab(locations_tab)

        # Tab 2: History/Log
        log_tab = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(log_tab, text="📋 History")
        self._build_log_tab(log_tab)

        # Control Panel at bottom
        self._build_control_panel()

    def _build_locations_tab(self, parent: tk.Frame) -> None:
        """Build the locations management tab."""
        # Location list with scrollbar
        list_frame = tk.Frame(parent, bg="#FFFFFF")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, font=("SF Mono", 11),
                                 bg="#FAFAFA", bd=2, relief="solid",
                                 selectbackground="#007AFF",
                                 yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Populate existing locations
        self._refresh_location_list()

        # Buttons
        button_frame = tk.Frame(parent, bg="#FFFFFF")
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Button(button_frame, text="➕ Add Location", font=("SF Pro", 12),
                 bg="#34C759", fg="white", relief="flat",
                 command=self.pick_location).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Button(button_frame, text="⚙️ Configure", font=("SF Pro", 12),
                 bg="#007AFF", fg="white", relief="flat",
                 command=self.configure_location).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Button(button_frame, text="🗑 Delete", font=("SF Pro", 12),
                 bg="#FF3B30", fg="white", relief="flat",
                 command=self.delete_location).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        tk.Button(button_frame, text="🗑 Clear All", font=("SF Pro", 12),
                 bg="#FF9500", fg="white", relief="flat",
                 command=self.clear_all_locations).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Info label
        self.location_info = tk.Label(parent,
                                     text=f"Locations: {len(self.locations)}/{MAX_LOCATIONS}",
                                     font=("SF Pro", 10), bg="#FFFFFF", fg="#8E8E93")
        self.location_info.pack(pady=5)

    def _build_log_tab(self, parent: tk.Frame) -> None:
        """Build the execution history/log tab."""
        log_frame = tk.Frame(parent, bg="#FFFFFF")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(log_frame, text="Execution History", font=("SF Pro", 14, "bold"),
                bg="#FFFFFF", fg="#1C1C1E").pack(pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, font=("SF Mono", 10),
                                                  bg="#FAFAFA", fg="#1C1C1E",
                                                  wrap=tk.WORD, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # Clear log button
        tk.Button(log_frame, text="🗑 Clear History", font=("SF Pro", 11),
                 bg="#FF9500", fg="white", relief="flat",
                 command=self.clear_log).pack(pady=5)

    def _build_control_panel(self) -> None:
        """Build the control panel at the bottom."""
        control_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid")
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Time scheduling
        time_frame = tk.Frame(control_frame, bg="#FFFFFF")
        time_frame.pack(pady=10)

        tk.Label(time_frame, text="⏰ Scheduled Time:", font=("SF Pro", 13),
                bg='#FFFFFF', fg="#1C1C1E").pack(side=tk.LEFT, padx=5)

        self.time_display = tk.Label(time_frame, text=self.execution_time,
                                     font=("SF Pro", 13, "bold"), bg='#FFFFFF', fg="#007AFF")
        self.time_display.pack(side=tk.LEFT, padx=5)

        tk.Button(time_frame, text="Change", font=("SF Pro", 11),
                 bg="#5856D6", fg="white", relief="flat",
                 command=self.change_execution_time).pack(side=tk.LEFT, padx=5)

        # Status indicator
        self.status_label = tk.Label(control_frame, text="● Status: Idle",
                                    font=("SF Pro", 12, "bold"),
                                    bg='#FFFFFF', fg="#8E8E93")
        self.status_label.pack(pady=5)

        # Control buttons
        button_control_frame = tk.Frame(control_frame, bg="#FFFFFF")
        button_control_frame.pack(pady=10)

        self.start_button = tk.Button(button_control_frame, text="▶ Start Scheduler",
                                     font=("SF Pro", 13, "bold"),
                                     bg="#34C759", fg="white", relief="flat",
                                     command=self.start_scheduler, width=18)
        self.start_button.pack(side=tk.LEFT, padx=5, ipady=8)

        self.stop_button = tk.Button(button_control_frame, text="■ Stop Scheduler",
                                    font=("SF Pro", 13, "bold"),
                                    bg="#FF3B30", fg="white", relief="flat",
                                    command=self.stop_scheduler, width=18, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, ipady=8)

        self.manual_button = tk.Button(button_control_frame, text="⚡ Execute Now",
                                      font=("SF Pro", 13, "bold"),
                                      bg="#FF9500", fg="white", relief="flat",
                                      command=self.execute_now, width=18)
        self.manual_button.pack(side=tk.LEFT, padx=5, ipady=8)

        # Footer
        footer = tk.Frame(control_frame, bg="#FFFFFF")
        footer.pack(pady=5)

        tk.Label(footer, text="Made by Amnas Ahamed | amnasahmd@gmail.com",
                font=("SF Pro", 9), bg="#FFFFFF", fg="#8E8E93").pack()

        tk.Label(footer, text="💡 Tip: Move mouse to screen corner to activate fail-safe",
                font=("SF Pro", 8, "italic"), bg="#FFFFFF", fg="#8E8E93").pack()

    def _refresh_location_list(self) -> None:
        """Refresh the location listbox display."""
        self.listbox.delete(0, tk.END)
        for i, loc in enumerate(self.locations):
            click_type = loc.get('type', 'left')
            delay = loc.get('delay', CLICK_DELAY)
            display = f"{i+1}. ({loc['x']}, {loc['y']}) - {click_type.upper()} - {delay}s delay"
            self.listbox.insert(tk.END, display)

        self.location_info.config(text=f"Locations: {len(self.locations)}/{MAX_LOCATIONS}")

    def pick_location(self) -> None:
        """Allow user to pick a location on screen."""
        if len(self.locations) >= MAX_LOCATIONS:
            messagebox.showwarning("Limit Reached",
                                  f"Maximum {MAX_LOCATIONS} locations allowed.\n"
                                  "Delete some locations to add more.")
            return

        self.log_message("Waiting for location selection...")
        self.root.withdraw()

        overlay = tk.Toplevel(self.root)
        overlay.configure(bg='black')
        overlay.attributes('-alpha', 0.01)
        overlay.attributes('-fullscreen', True)
        overlay.attributes('-topmost', True)
        overlay.grab_set()
        overlay.configure(cursor="crosshair")

        def on_click(event: tk.Event) -> None:
            x, y = event.x_root, event.y_root

            # Open click configuration dialog
            overlay.destroy()
            self.root.deiconify()

            dialog = ClickTypeDialog(self.root)
            self.root.wait_window(dialog)

            if dialog.result:
                location = {
                    'x': x,
                    'y': y,
                    'type': dialog.result['type'],
                    'delay': dialog.result['delay']
                }
                self.locations.append(location)
                self._refresh_location_list()
                self.save_config()
                self.log_message(f"Added location ({x}, {y}) - {dialog.result['type']} click")
            else:
                self.log_message("Location selection cancelled")

        overlay.bind('<Button-1>', on_click)

        # Cancel with ESC key
        def on_escape(event: tk.Event) -> None:
            overlay.destroy()
            self.root.deiconify()
            self.log_message("Location selection cancelled")

        overlay.bind('<Escape>', on_escape)

    def configure_location(self) -> None:
        """Configure the selected location's click type and delay."""
        try:
            selected_index = self.listbox.curselection()[0]
            loc = self.locations[selected_index]

            dialog = ClickTypeDialog(self.root, loc.get('type', 'left'),
                                    loc.get('delay', CLICK_DELAY))
            self.root.wait_window(dialog)

            if dialog.result:
                self.locations[selected_index]['type'] = dialog.result['type']
                self.locations[selected_index]['delay'] = dialog.result['delay']
                self._refresh_location_list()
                self.save_config()
                self.log_message(f"Updated location {selected_index + 1} configuration")
        except IndexError:
            messagebox.showinfo("No Selection", "Please select a location to configure")

    def delete_location(self) -> None:
        """Delete the selected location."""
        try:
            selected_index = self.listbox.curselection()[0]
            loc = self.locations[selected_index]
            self.locations.pop(selected_index)
            self._refresh_location_list()
            self.save_config()
            self.log_message(f"Deleted location ({loc['x']}, {loc['y']})")
        except IndexError:
            messagebox.showinfo("No Selection", "Please select a location to delete")

    def clear_all_locations(self) -> None:
        """Clear all locations after confirmation."""
        if not self.locations:
            messagebox.showinfo("No Locations", "No locations to clear")
            return

        if messagebox.askyesno("Confirm Clear",
                              f"Are you sure you want to delete all {len(self.locations)} locations?"):
            self.locations.clear()
            self._refresh_location_list()
            self.save_config()
            self.log_message("Cleared all locations")

    def change_execution_time(self) -> None:
        """Change the scheduled execution time."""
        dialog = TimePickerDialog(self.root, self.execution_time)
        self.root.wait_window(dialog)
        if dialog.parent_time_var:
            self.execution_time = dialog.parent_time_var
            self.time_display.config(text=self.execution_time)
            self.save_config()
            self.log_message(f"Changed execution time to {self.execution_time}")

    def perform_click(self, location: Dict[str, Any]) -> None:
        """
        Perform a click at the specified location with configured type.

        Args:
            location: Dictionary containing x, y, type, and delay
        """
        x, y = location['x'], location['y']
        click_type = location.get('type', 'left')
        delay = location.get('delay', CLICK_DELAY)

        try:
            if click_type == 'double':
                pyautogui.doubleClick(x, y)
            elif click_type == 'right':
                pyautogui.rightClick(x, y)
            else:  # left click
                pyautogui.click(x, y)

            time.sleep(delay)
        except pyautogui.FailSafeException:
            self.log_message("⚠️ FAIL-SAFE triggered! Mouse moved to corner.")
            raise

    def execute_clicks(self) -> None:
        """Execute all configured clicks in sequence."""
        if not self.locations:
            self.log_message("⚠️ No locations to click")
            return

        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_message(f"▶ Started click sequence at {start_time}")

        try:
            for i, location in enumerate(self.locations):
                self.log_message(f"  Clicking location {i+1}/{len(self.locations)}: "
                               f"({location['x']}, {location['y']}) - {location.get('type', 'left')}")
                self.perform_click(location)

            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_message(f"✓ Completed click sequence at {end_time}")

        except pyautogui.FailSafeException:
            self.log_message("✗ Click sequence aborted by fail-safe")
            messagebox.showwarning("Fail-Safe Activated",
                                 "Click sequence stopped! You moved the mouse to a screen corner.")
        except Exception as e:
            self.log_message(f"✗ Error during click sequence: {str(e)}")
            messagebox.showerror("Error", f"Error during click execution: {str(e)}")

    def execute_now(self) -> None:
        """Execute clicks immediately (manual trigger)."""
        if not self.locations:
            messagebox.showwarning("No Locations", "Please add at least one location first")
            return

        if messagebox.askyesno("Confirm Execution",
                              f"Execute clicks at {len(self.locations)} locations now?"):
            self.log_message("⚡ Manual execution triggered")
            threading.Thread(target=self.execute_clicks, daemon=True).start()

    def start_scheduler(self) -> None:
        """Start the automated scheduler."""
        if not self.locations:
            messagebox.showwarning("No Locations", "Please add at least one location")
            return

        if self.scheduler_running:
            messagebox.showinfo("Already Running", "Scheduler is already running")
            return

        try:
            schedule.clear()  # Clear any previous schedules
            schedule.every().day.at(self.execution_time).do(self.execute_clicks)

            self.scheduler_running = True
            self.stop_scheduler_flag.clear()

            def run_schedule() -> None:
                while not self.stop_scheduler_flag.is_set():
                    schedule.run_pending()
                    time.sleep(1)

            self.scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
            self.scheduler_thread.start()

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="● Status: Running", fg="#34C759")

            self.log_message(f"✓ Scheduler started - will execute daily at {self.execution_time}")
            messagebox.showinfo("Scheduler Started",
                              f"Clicks will execute automatically at {self.execution_time} daily.\n\n"
                              f"Locations: {len(self.locations)}\n"
                              f"Next execution: {self.execution_time}")

        except Exception as e:
            self.log_message(f"✗ Failed to start scheduler: {str(e)}")
            messagebox.showerror("Error", f"Failed to start scheduler: {str(e)}")

    def stop_scheduler(self) -> None:
        """Stop the automated scheduler."""
        if not self.scheduler_running:
            return

        self.stop_scheduler_flag.set()
        self.scheduler_running = False
        schedule.clear()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="● Status: Stopped", fg="#FF3B30")

        self.log_message("■ Scheduler stopped")
        messagebox.showinfo("Scheduler Stopped", "Automated scheduler has been stopped")

    def log_message(self, message: str) -> None:
        """
        Add a message to the log with timestamp.

        Args:
            message: The message to log
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

        # Limit log size
        line_count = int(self.log_text.index('end-1c').split('.')[0])
        if line_count > LOG_MAX_LINES:
            self.log_text.delete('1.0', f'{line_count - LOG_MAX_LINES}.0')

        self.log_text.config(state=tk.DISABLED)

    def clear_log(self) -> None:
        """Clear the execution history log."""
        if messagebox.askyesno("Confirm Clear", "Clear all execution history?"):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete('1.0', tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.log_message("Log cleared")

    def save_config(self) -> None:
        """Save configuration to JSON file."""
        try:
            config = {
                'locations': self.locations,
                'execution_time': self.execution_time,
                'version': '2.0'
            }

            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            self.log_message(f"⚠️ Failed to save configuration: {str(e)}")

    def load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)

                self.locations = config.get('locations', [])
                self.execution_time = config.get('execution_time', DEFAULT_EXECUTION_TIME)

                print(f"Loaded {len(self.locations)} locations from config")
            else:
                print("No config file found, using defaults")
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            messagebox.showwarning("Config Load Error",
                                 f"Failed to load saved configuration: {str(e)}\n"
                                 "Starting with default settings.")

    def on_closing(self) -> None:
        """Handle application closing."""
        if self.scheduler_running:
            if messagebox.askyesno("Scheduler Running",
                                  "The scheduler is still running.\n"
                                  "Do you want to stop it and quit?"):
                self.stop_scheduler()
                self.save_config()
                self.root.destroy()
        else:
            self.save_config()
            self.root.destroy()


def check_macos_permissions() -> None:
    """Check and inform about macOS accessibility permissions."""
    import platform

    if platform.system() == 'Darwin':  # macOS
        print("\n" + "="*60)
        print("macOS ACCESSIBILITY PERMISSIONS REQUIRED")
        print("="*60)
        print("\nThis application requires Accessibility permissions to control")
        print("the mouse. If clicks don't work:")
        print("\n1. Open System Preferences > Security & Privacy > Privacy")
        print("2. Select 'Accessibility' from the left sidebar")
        print("3. Add Terminal (or your Python app) to the list")
        print("4. Restart this application")
        print("\n" + "="*60 + "\n")

        time.sleep(2)  # Give user time to read


def main() -> None:
    """Main entry point for the application."""
    check_macos_permissions()

    root = tk.Tk()
    app = AutoMouseClicker(root)

    # Log startup
    app.log_message("=== Auto Mouse Clicker Pro Started ===")
    app.log_message(f"Loaded {len(app.locations)} saved locations")
    app.log_message(f"Scheduled time: {app.execution_time}")
    app.log_message("Ready to go!")

    root.mainloop()


if __name__ == "__main__":
    main()
