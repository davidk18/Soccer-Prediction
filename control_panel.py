from tkintertable import *
import tkinter as tk
import tkinter.ttk as ttk
import model as mod
import future_bet_table as ft


class ControlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        content = parent

        self.last_spend = 0
        self.last_betting_return = 0
        self.last_performance = 0
        self.last_accuracy = 0
        self.last_loss = 0

        self.iterations_frame = tk.Frame()
        self.iterations_label = Label(self.iterations_frame, text="Enter Iterations\n      e.g. 3")
        self.iterations_input = Entry(self.iterations_frame)

        self.edge_frame = tk.Frame()
        self.edge_label = Label(self.edge_frame, text="Enter Probability Advantage\n\t e.g. 0.03")
        self.edge_input = Entry(self.edge_frame)

        self.train_button_frame = tk.Frame(padx=10, pady=10)
        self.train_button = tk.Button(self.train_button_frame, text="Run", padx=8, pady=6, command=self.instantiate_model)

        self.bar_frame = tk.Frame()
        self.progress = ttk.Progressbar(self.bar_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')

        self.list_frame = tk.Frame()

        self.risk = StringVar(self.list_frame)

        self.choices = ['Default', 'Default', 'Low', 'Medium', 'High' ]
        self.risk.set('Default')  # set the default option

        self.popupMenu = OptionMenu(self.list_frame, self.risk, *self.choices)
        self.label = Label(self.list_frame, text="Select Staking Strategy")

        self.output_frame = tk.Frame(padx=10)
        self.model_output = tk.Text(self.output_frame)

        self.future_bet_table_frame = tk.Frame(padx=10)
        self.bet_output = ft.FutureBetTable(self.future_bet_table_frame)

        self.table_label_frame = tk.Frame()
        self.table_label = tk.Label(self.table_label_frame, text="Future Bets")

        self.model_output_heading_frame = tk.Frame()
        self.model_output_heading = tk.Label(self.model_output_heading_frame, text="Output Summary")

        self.pic_frame = tk.Frame()
        self.pic = PhotoImage(file="pl.png")
        self.pic_label = tk.Label(self.pic_frame, image=self.pic)

        self.pic2_frame = tk.Frame()
        self.pic2 = PhotoImage(file="bet.png")
        self.pic2_label = tk.Label(self.pic2_frame, image=self.pic2)



        self.bar_frame.grid(row=2, columnspan=2)
        self.progress.grid(row=0, column=0)

        self.iterations_frame.grid(row=3, columnspan=2)
        self.iterations_label.grid(row=0, columnspan=2)
        self.iterations_input.grid(row=3, columnspan=2)

        self.edge_frame.grid(row=4, columnspan=2)
        self.edge_label.grid(row=2, columnspan=2)
        self.edge_input.grid(row=3, columnspan=2)

        self.pic_frame.grid(row=2, column=0, rowspan=4)
        self.pic_label.grid()

        self.pic2_frame.grid(row=2, column=1, rowspan=4)
        self.pic2_label.grid()

        self.list_frame.grid(row=5, columnspan=2)
        self.popupMenu.grid(row=3, columnspan=2)
        self.label.grid(row=2, columnspan=2)

        self.train_button_frame.grid(row=6, columnspan=2)
        self.train_button.grid(row=2, column=0)

        self.table_label_frame.grid(row=6, column=1)
        self.table_label.grid(row=2, column=0)

        self.model_output_heading_frame.grid(row=6, column=0)
        self.model_output_heading.grid(row=2, column=0)

        self.output_frame.grid(row=7)
        self.model_output.grid(row=2, columnspan=1)

        self.future_bet_table_frame.grid(row=7, column=1)
        self.bet_output.grid(row=2, column=1)


    def instantiate_model(self):
        self.model_output.delete('1.0', END)
        self.model_output.update()

        model = mod.Model()
        iterations = int(self.iterations_input.get())
        edge = float(self.edge_input.get())
        strategy = self.risk.get()
        progress_increase = 100 / iterations
        spend = 0
        betting_return = 0
        performance = 0
        accuracy = 0
        average_loss = 0


        for i in range(0, iterations):
            model_result = model.begin(edge, strategy)
            spend = spend + model_result[0]['spend']
            betting_return = betting_return + model_result[0]['return']
            performance = performance + model_result[0]['performance']
            accuracy = accuracy + model_result[1]['accuracy']
            average_loss = average_loss + model_result[1]['average_loss']

            self.progress['value'] = self.progress['value'] + progress_increase
            self.progress.update()

            if i == iterations-1:
                self.last_spend = round(model_result[0]['spend'], 2)
                self.last_betting_return = round(model_result[0]['return'], 2)
                self.last_performance = round(model_result[0]['performance'], 2)
                self.last_accuracy = round(model_result[1]['accuracy'], 3)
                self.last_loss = round(model_result[1]['average_loss'], 2)


        self.progress['value'] = 100
        time.sleep(1)
        self.progress['value'] = 0

        spend = round((spend / iterations), 2)
        betting_return = round((betting_return / iterations), 2)
        performance_rounded = round((performance / iterations), 2)
        accuracy_rounded = round((accuracy / iterations), 3)
        average_loss_rounded = round((average_loss / iterations), 2)

        if iterations > 1:
            self.model_output.insert("2.0", "AVG SPEND:\t\t\t" + str(self.last_spend) + "\n")
            self.model_output.insert("3.0", "AVG RETURN:\t\t\t" + str(self.last_betting_return) + "\n")
            self.model_output.insert("4.0", "AVG PERFORMANCE:\t\t\t" + str(self.last_performance) + "\n")
            self.model_output.insert("5.0", "AVG ACCURACY:\t\t\t" + str(self.last_accuracy) + "\n")
            self.model_output.insert("6.0", "AVG LOSS:\t\t\t" + str(self.last_loss) + "\n")
            self.model_output.insert("7.0", "STRATEGY:\t\t\t" + strategy + "\n")
            self.model_output.insert("8.0", "EDGE:\t\t\t" + str(edge) + "\n\n")



        self.model_output.insert("9.0", "SPEND:\t\t\t" + str(spend) + "\n")
        self.model_output.insert("10.0", "RETURN:\t\t\t" + str(betting_return) + "\n")
        self.model_output.insert("11.0", "PERFORMANCE:\t\t\t" + str(performance_rounded) + "\n")
        self.model_output.insert("12.0", "ACCURACY:\t\t\t" + str(accuracy_rounded) + "\n")
        self.model_output.insert("13.0", "LOSS:\t\t\t" + str(average_loss_rounded) + "\n")
        self.model_output.insert("14.0", "STRATEGY:\t\t\t" + strategy + "\n")
        self.model_output.insert("15.0", "EDGE:\t\t\t" + str(edge) + "\n\n")

        




