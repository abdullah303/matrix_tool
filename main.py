import tkinter as tk
import numpy as np
import pandas as pd
import os

class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # initial settings
        self.title("Matrix Learning Tool")
        self.geometry("1280x720")
        self.resizable(True, True)


        # create a container
        self.container = tk.Frame(self, bg="#B8D8D8")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # initialise frames
        self.frames = {}


        # define frames and pack them
        for F in (HomePage, CreateExercisePage, CompleteExercisePage, LeaderboardPage, CreateAddSubMultExercisePage, CreateEigenvalueExercisePage, CreateEigenvectorExercisePage, CreateInvDetExercisePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
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
        self.controller = controller

        #header
        label = tk.Label(self, text="Create Exercise", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=0, padx=10, pady=10)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: self.controller.show_frame("HomePage"))
        button.grid()



        self.file_name = "test.csv"
        file_entry = tk.StringVar()
        tk.Entry(self, text="Hi", textvariable=file_entry).grid(column=1, row=9)
        tk.Label(self, text="Enter Filename: ", font={"Helvetica", 20}).grid(column=0, row=9)
        set_file = tk.Button(self, text="Submit Filename", command=lambda: self.setFileName(file_entry.get()))
        set_file.grid(column=2, row= 9)

        # operation menu
        self.v = tk.StringVar()
        self.operation = ""
        operations = {"Addition" : "addition",
                      "Subtraction" : "subtraction",
                      "Multiplication" : "multiplication",
                      "Eigenvalue" : "eigenvalue",
                      "Eigenvector" : "eigenvector",
                      "Inverse" : "inverse",
                      "Determinant" : "determinant"}

        for (text, value) in operations.items():
            tk.Radiobutton(self, text=text, variable=self.v, value=value, command=lambda: self.controller.show_frame(self.getOperationPage(self.v.get())), indicator=0, background="light blue", width=15).grid(column=0)


    def getOperationPage(self, operation):
        self.operation = operation

        label = tk.Label(self, text=self.operation, font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=6, padx=10, pady=10)

        match operation:
            case ("addition"|"multiplication"|"subtraction"):
                return "CreateAddSubMultExercisePage"
            case "eigenvalue":
                return "CreateEigenvalueExercisePage"
            case "eigenvector":
                return "CreateEigenvectorExercisePage"
            case ("inverse"|"determinant"):
                return "CreateInvDetExercisePage"

    def setFileName(self, file_name):
        self.file_name = file_name




class CreateAddSubMultExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.matrix1 = MatrixInput(self, 3, 3)
        self.matrix2 = MatrixInput(self, 3, 3)

        self.matrix1.grid(column=6, row=10)
        self.matrix2.grid(column=11, row=10)

        submit = tk.Button(self, text="Submit", command=self.onSubmit)
        submit.grid(column= 8, row= 13)

    def onSubmit(self):
        npMatrix1 = self.matrix1.get()
        npMatrix2 = self.matrix2.get()

        question = {"operation": [self.operation], "matrix 1": [np.array2string(npMatrix1)], "matrix 2": [np.array2string(npMatrix2)]}
        dataframe = pd.DataFrame(question)
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False)

class CreateInvDetExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.matrix1 = MatrixInput(self, 3, 3)

        self.matrix1.grid(column=6, row=10)

        submit = tk.Button(self, text="Submit", command=self.onSubmit)
        submit.grid(column= 8, row= 13)

    def onSubmit(self):
        npMatrix1 = self.matrix1.get()

        question = {"operation": [self.operation], "matrix 1": [np.array2string(npMatrix1)], "matrix 2": [""]}
        dataframe = pd.DataFrame(question)
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False)


class CreateEigenvalueExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)



class CreateEigenvectorExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)





class MatrixInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        self.entry = {}
        self.rows = rows
        self.columns = columns

        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, width=3, font={"Helvetica", 30})
                e.grid(row=row, column=column, stick="nsew", ipadx=10, ipady=10)
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
                current_row.append(int(self.entry[index].get()))
                self.entry[index].delete(0, "end")
            result.append(current_row)
        return np.reshape(result, (self.rows, self.columns))


class CompleteExercisePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #header
        label = tk.Label(self, text="Complete Exercise", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=0, padx=10, pady=10)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: self.controller.show_frame("HomePage"))
        button.grid()










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
        