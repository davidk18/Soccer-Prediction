from tkintertable import *
import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import model
import tkfontchooser as tkf

class Header(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        content = parent

        self.predictions_header_frame = tk.Frame(borderwidth=5, relief="sunken", width=30, height=30, background="red")
        self.selections_header_frame = tk.Frame(borderwidth=5, relief="sunken", width=30, height=30)

        self.predictions_header = tkf.Label(self.predictions_header_frame, compound = tk.CENTER, text="PREDICTIONS")

        self.selections_header = tk.Label(self.selections_header_frame, compound = tk.CENTER, text="BETS")

        self.predictions_header_frame.grid(row=0,  column=0)
        self.selections_header_frame.grid(row=0, column=1)



