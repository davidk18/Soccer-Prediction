import tkinter as tk
import pred_table
import bet_table
import table_controls as tc
import control_panel as con
import header


class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.predictions_table_frame = tk.Frame(borderwidth=5)
        self.predictions_table = pred_table.PredTable(self.predictions_table_frame)

        self.table_header = header.Header(self)

        self.betting_table_frame = tk.Frame(borderwidth=5)
        self.betting_table = bet_table.BetTable(self.betting_table_frame)

        self.control_panel_frame = tk.Frame()
        self.control_panel = tc.TableControls(self.control_panel_frame)
        self.train_panel = con.ControlPanel(self)

        self.control_panel_frame.grid(row=2, column=0)
        self.predictions_table_frame.grid(row=1, column=0)
        self.betting_table_frame.grid(row=1, column=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)



