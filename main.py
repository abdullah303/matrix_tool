from cgitb import text
import tkinter as tk
from tkinter import ttk
import numpy as np


class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # initial settings
        self.title("Matrix Learning Tool")
        self.geometry("1280x720")
        self.resizable(True, True)


        # create a container
        container = tk.Frame(self, bg="#B8D8D8")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initialise frames
        self.frames = {}


        # define frames and pack them
        for F in (HomePage, CreateExercisePage, CompleteExercisePage, LeaderboardPage, CompleteAdditionExercisePage, CompleteSubtractionExercisePage,
        CompleteMultiplicationExercisePage, CompleteEigenvalueExercisePage, CompleteEigenvectorExercisePage, CompleteInverseExercisePage, CompleteDeterminantExercisePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()



class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Home Page", font={"Helvetica", 20})
        label.pack(pady=0, padx=0)

        button1 = tk.Button(self, text="Go to Create Exercise", command=lambda: controller.show_frame("CreateExercisePage"), padx=50, pady=50)
        button2 = tk.Button(self, text="Go to Complete Exercise", command=lambda: controller.show_frame("CompleteExercisePage"), padx=50, pady=50)
        button3 = tk.Button(self, text="Go to Leaderboard", command=lambda: controller.show_frame("LeaderboardPage"), padx=50, pady=50)

        button1.pack(fill="none", expand=True)
        button2.pack(fill="none", expand=True)
        button3.pack(fill="none", expand=True)     

      
class CreateExercisePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Create Exercise", font={"Helvetica", 20})
        label.pack(pady=0, padx=0)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: controller.show_frame("HomePage"))
        button.pack()



class MatrixInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        self.entry = {}
        self.rows = rows
        self.columns = columns

        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, width=4)
                e.grid(row=row, column=column, stick="nsew")
                self.entry[index] = e

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)

        self.grid_rowconfigure(rows, weight=1)

    def get(self):
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(self.entry[index].get())
            result.append(current_row)
        return result


class CompleteExercisePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #header
        label = tk.Label(self, text="Complete Exercise", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=0, padx=10, pady=10)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: controller.show_frame("HomePage"))
        button.grid()


        # operation menu
        v = tk.StringVar()

        operations = {"Addition" : "CompleteAdditionExercisePage",
                      "Subtraction" : "CompleteSubtractionExercisePage",
                      "Multiplication" : "CompleteMultiplicationExercisePage",
                      "Eigenvalue" : "CompleteEigenvalueExercisePage",
                      "Eigenvector" : "CompleteEigenvectorExercisePage",
                      "Inverse" : "CompleteInverseExercisePage",
                      "Determinant" : "CompleteDeterminantExercisePage"}

        for (text, value) in operations.items():
            tk.Radiobutton(self, text=text, variable=v, value=value, command=lambda: controller.show_frame(v.get()), indicator=0, background="light blue", width=15).grid(column=0)

    




class CompleteAdditionExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Addition", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)

class CompleteSubtractionExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Subtraction", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)

class CompleteMultiplicationExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Multiplication", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)

class CompleteEigenvalueExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Eigenvalue", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)

class CompleteEigenvectorExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Eigenvector", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)

class CompleteInverseExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Inverse", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)

class CompleteDeterminantExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = tk.Label(self, text="Determinant", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)








class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Leaderboard", font={"Helvetica", 20})
        label.pack(pady=0, padx=0)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: controller.show_frame("HomePage"))
        button.pack()

if __name__ == "__main__":
    app = MatrixApp()
    app.mainloop()
        