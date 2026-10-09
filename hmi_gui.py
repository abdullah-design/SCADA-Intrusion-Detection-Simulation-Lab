import tkinter as tk
from tkinter import messagebox
from pymodbus.client import ModbusTcpClient
import threading
import time

class SCADA_HMI_App:
    def __init__(self, root):
        self.root = root
        self.root.title("SCADA HMI Dashboard - Capstone Project")
        self.root.geometry("520x480")
        self.root.config(bg="#1e1e1e")

        self.client = ModbusTcpClient("127.0.0.1", port=5020)
        self.is_connected = False
        self.running = True

        self.create_widgets()

        self.thread = threading.Thread(target=self.poll_plc, daemon=True)
        self.thread.start()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Industrial PLC HMI Dashboard", font=("Arial", 16, "bold"), fg="#ffffff", bg="#1e1e1e")
        title_label.pack(pady=15)

        self.status_indicator = tk.Label(self.root, text="Status: Disconnected", font=("Arial", 11, "bold"), fg="#ff4d4d", bg="#1e1e1e")
        self.status_indicator.pack(pady=5)

        # Reading Frame
        frame_reading = tk.Frame(self.root, bg="#2d2d2d", bd=2, relief="groove")
        frame_reading.pack(pady=10, padx=20, fill="x")

        lbl_reg = tk.Label(frame_reading, text="Holding Register [0] Live Value:", font=("Arial", 11), fg="#b0b0b0", bg="#2d2d2d")
        lbl_reg.pack(pady=5)

        self.value_display = tk.Label(frame_reading, text="---", font=("Arial", 24, "bold"), fg="#4da6ff", bg="#2d2d2d")
        self.value_display.pack(pady=5)

        # Writing / Control Frame
        frame_control = tk.Frame(self.root, bg="#2d2d2d", bd=2, relief="groove")
        frame_control.pack(pady=10, padx=20, fill="x")

        lbl_write = tk.Label(frame_control, text="Write New Value to Register [0]:", font=("Arial", 11), fg="#b0b0b0", bg="#2d2d2d")
        lbl_write.pack(pady=5)

        self.entry_value = tk.Entry(frame_control, font=("Arial", 14), justify="center", width=10)
        self.entry_value.pack(pady=5)
        self.entry_value.insert(0, "150")

        btn_write = tk.Button(frame_control, text="Write to PLC", command=self.write_to_plc, font=("Arial", 10, "bold"), bg="#0275d8", fg="white", width=15)
        btn_write.pack(pady=8)

        # Exit Button
        btn_quit = tk.Button(self.root, text="Exit HMI", command=self.on_closing, font=("Arial", 10, "bold"), bg="#d9534f", fg="white", width=15)
        btn_quit.pack(pady=10)

    def poll_plc(self):
        if self.client.connect():
            self.is_connected = True
            self.status_indicator.config(text="Status: Connected to PLC", fg="#5cb85c")
        else:
            self.status_indicator.config(text="Status: Connection Failed", fg="#ff4d4d")
            return

        while self.running:
            try:
                result = self.client.read_holding_registers(address=0, count=1)
                if not result.isError():
                    val = result.registers[0]
                    self.value_display.config(text=str(val))
                else:
                    self.value_display.config(text="Error")
            except Exception as e:
                self.status_indicator.config(text="Status: Connection Lost", fg="#ff4d4d")
            
            time.sleep(1.5)

    def write_to_plc(self):
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to PLC!")
            return
        
        try:
            new_val = int(self.entry_value.get())
            # كتابة القيمة الجديدة إلى السجل 0 في السيرفر
            result = self.client.write_register(address=0, value=new_val)
            if not result.isError():
                messagebox.showinfo("Success", f"Successfully wrote value {new_val} to PLC!")
            else:
                messagebox.showerror("Error", "Failed to write to PLC register.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer number.")

    def on_closing(self):
        self.running = False
        try:
            self.client.close()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SCADA_HMI_App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()