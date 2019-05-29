from tkintertable import *
import tkinter as tk


class BetTable(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        content = parent
        self.predictions = TableCanvas(parent,
               cellwidth=40, cellbackgr='#E3F6CE',
               rowheight=16, editable=False,
              rowselectedcolor='yellow')
        self.predictions.importCSV('Betting.csv')

        update_button = tk.Button(parent, text="Update Table", padx=8, pady=6, command=self.update_pred_table)
        update_button.grid(row=2, rowspan=5, columnspan=5, padx=30, pady=30)


        self.predictions.grid()
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def update_pred_table(self):
        self.predictions.importCSV('Betting.csv')
