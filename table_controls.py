import tkinter as tk

class TableControls(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        content = parent

        self.predictions_button_frame = tk.Frame()
        self.predictions_button = tk.Label(self.predictions_button_frame, text="Predictions", padx=8, pady=6)

        self.bar_frame = tk.Frame()

        self.betting_button_frame = tk.Frame()
        self.betting_button = tk.Label(self.betting_button_frame, text="Bets Placed", padx=8, pady=6)

        self.bar_frame.grid(row=0, column=1)
        self.betting_button_frame.grid(row=0, column=1)
        self.predictions_button_frame.grid(row=0, column=0)
        self.betting_button.grid(row=0, column=0)
        self.predictions_button.grid(row=0, column=1)
