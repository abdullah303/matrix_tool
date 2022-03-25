
from operator import index
import tkinter as tk
import numpy as np
import pandas as pd
import csv
import os
import ast

class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # initial settings
        self.title("Matrix Learning Tool")
        self.geometry("1000x500")
        self.resizable(True, True)


        # create a container
        self.container = tk.Frame(self, bg="#AFE3E4")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # initialise frames
        self.frames = {}


        # define frames and pack them
        for F in (HomePage, CreateExercisePage, CompleteExercisePage, LeaderboardPage, CreateAddSubMultExercisePage, CreateInvDetEigenExercisePage):
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
        tk.Frame.__init__(self, parent, bg="#AFE3E4")

        label = tk.Label(self, text="Matrix Learning Tool", font={"Helvetica", 20})
        label.pack(side="left", fill="x", padx = 100, pady=100)

        button1 = tk.Button(self, text="Go to Create Exercise",
                    command=lambda: controller.show_frame("CreateExercisePage"),
                    padx= 50, pady = 50)
        button2 = tk.Button(self, text="Go to Complete Exercise",
                    command=lambda: controller.show_frame("CompleteExercisePage"),
                    padx= 50, pady = 50)
        button3 = tk.Button(self, text="Go to Leaderboard",
                    command=lambda: controller.show_frame("LeaderboardPage"),
                    padx= 50, pady = 50) 

        button1.pack(fill="none", expand=True)
        button2.pack(fill="none", expand=True)
        button3.pack(fill="none", expand=True) 

      
class CreateExercisePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#AFE3E4")
        self.controller = controller

        #header
        label = tk.Label(self, text="Create Exercise", font={"Helvetica", 20}, width=25, bg="#AFE3E4")
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
            case ("inverse"|"determinant"|"eigenvalue"|"eigenvector"):
                return "CreateInvDetEigenExercisePage"

    def setFileName(self, file_name):
        self.file_name = file_name




class CreateAddSubMultExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.matrix1 = MatrixInput(self, 3, 3)
        self.matrix2 = MatrixInput(self, 3, 3)

        self.matrix1.place(x=300, y=200)
        self.matrix2.place(x=600, y=200)

        submit = tk.Button(self, text="Submit", command=self.onSubmit)
        submit.place(x=500, y=350)

    def onSubmit(self):
        npMatrix1 = self.matrix1.get()
        npMatrix2 = self.matrix2.get()

        question = {"operation": [self.operation], "matrix 1": [npMatrix1], "matrix 2": [npMatrix2]}
        dataframe = pd.DataFrame(question)
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False, index=False)

class CreateInvDetEigenExercisePage(CreateExercisePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.matrix1 = MatrixInput(self, 3, 3)

        self.matrix1.place(x=400, y=200)

        submit = tk.Button(self, text="Submit", command=self.onSubmit)
        submit.place(x=450, y=350)

    def onSubmit(self):
        npMatrix1 = self.matrix1.get()

        question = {"operation": [self.operation], "matrix 1": [npMatrix1], "matrix 2": [""]}
        dataframe = pd.DataFrame(question)
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False, index=False)





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
        return result
        #np.reshape(result, (self.rows, self.columns))


class CompleteExercisePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_exercise = ""
        self.answer = ""

        #header
        label = tk.Label(self, text="Complete Exercise", font={"Helvetica", 20}, width=25)
        label.grid(row=0, column=0, padx=10, pady=10)

        button = tk.Button(self, text="Go to the Main Menu", command=lambda: self.controller.show_frame("HomePage"))
        button.grid()

        self.getExercises()


    def getExercises(self):
        exercises = os.listdir(os.path.join(os.getcwd(), "exercises"))
        self.variable = tk.StringVar(self)
        menu = tk.OptionMenu(self, self.variable, *exercises)
        menu.grid()

        tk.Button(self, text="select exercise", command=lambda: self.setExercise(self.variable)).grid()

        ans = tk.Label(self ,text = "Answer").grid(row = 10,column = 1)
        self.answer = tk.StringVar()
        ansForm = tk.Entry(self, textvariable=self.answer).grid(row=11, column=1)
        answerFormat = tk.Label(self, text="Give answer in format [[x1,x2,x3],[x4,x5,x6],[x7,x8,x9]]").grid(row=13, column=1, padx=10, pady=10)

    def setExercise(self, variable):
        self.current_exercise = variable.get()
        path = os.path.join(os.getcwd(), "exercises", self.current_exercise)
        df = pd.read_csv(path)
        File = open(path)
        Reader = csv.reader(File)
        self.Data = list(Reader)
        # del(Data[0])

        list_of_entries = []
        for x in list(range(0,len(self.Data))):
            list_of_entries.append(self.Data[x][0])
        var = tk.StringVar(value = list_of_entries)
        listbox1 = tk.Listbox(self, listvariable = var)
        listbox1.grid(row=10 , column=0)

        def update():
            try:
                self.index = listbox1.curselection()[0]
            except:
                self.index = 0
            operationLabel2.config(text = self.Data[self.index][0])
            matrix1Label2.config(text = np.reshape(ast.literal_eval(self.Data[self.index][1]), (3,3)))
            matrix2Label2.config(text = np.reshape(ast.literal_eval(self.Data[self.index][2]), (3,3)))
            # answerlabel2.config(text = Data[index][3])
            
        def ans():
            update()
            self.bigtuple = (self.index, self.Data[self.index][0], self.Data[self.index][1], self.Data[self.index][2])
            return self.checkANS(self.bigtuple)

        buttonANS = tk.Button(self, text="Check Answer", command=ans).grid(row=12, column=1, padx=10, pady=10)


        button1 = tk.Button(self, text="Update", command=update)
        button1.grid(row=15, column=0)

        operationLabel = tk.Label(self, text="Operation").grid(row=0, column=1,sticky="w")
        matrix1Label = tk.Label(self, text="Matrix 1").grid(row=2, column=1,sticky="w")
        matrix2Label = tk.Label(self, text="Matrix 2").grid(row=2, column=2,sticky="w")
        # answerlabel = tk.Label(self, text="Answer").grid(row=4, column=0,sticky="w")

        operationLabel2 = tk.Label(self, text="")
        operationLabel2.grid(row=1, column=1,sticky="w")
        matrix1Label2 = tk.Label(self, text="")
        matrix1Label2.grid(row=3, column=1,sticky="w")
        matrix2Label2 = tk.Label(self, text="")
        matrix2Label2.grid(row=3, column=2,sticky="w")
        # answerlabel2 = tk.Label(self, text="")
        # answerlabel2.grid(row=4, column=1,sticky="w")
        # print(df)
        return update()
        

    def checkANS(self, bigtuple):
        index, DataOperation, matrix1, matrix2 = bigtuple

        try:
            npMatrix1 = np.reshape(ast.literal_eval(matrix1), (3,3))
            npMatrix2 = np.reshape(ast.literal_eval(matrix2), (3,3))
            answer = np.reshape(ast.literal_eval(self.answer.get()), (3,3))

        except:
            pass

        def correct():
            tk.Label(self, text="Correct!").grid(column=10, row=10)

        def incorrect():
            tk.Label(self, text="Inorrect!").grid(column=10, row=10)
        
        match DataOperation:
            case "addition":
                correct() if (answer == np.add(npMatrix1, npMatrix2)).all() else incorrect()
            case "subtraction":
                correct() if (answer == np.subtract(npMatrix1, npMatrix2)).all() else incorrect()
            case "multiplication":
                correct() if (answer == np.multiply(npMatrix1, npMatrix2)).all() else incorrect()
            case "eigenvalue":
                values, vector = np.linalg.eigh(np.reshape(npMatrix1))
                correct() if self.answer.get() == (str(values[0])) or self.answer.get() == (str(values[1])) else incorrect()
            case "eigenvector":
                values, vector = np.linalg.eigh(np.reshape(npMatrix1))
                correct() if self.answer.get() == (str(vector).tolist()).replace(" ", "") else incorrect()
            case "inverse":
                correct() if (answer == np.linalg.inv(npMatrix1)).all() else incorrect()
            case "determinant":
                correct() if self.answer.get() == (str(determinant(matrix1))) else incorrect()

    def new_method(self):
        print("answer is correct")


def determinant(matrix):
    print(matrix)
    matrix = np.array(matrix)
    if len(matrix[0]) == len(matrix[:,0]) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[1][0]*matrix[0][1]
    elif len(matrix[0]) == len(matrix[:,0]) == 3:
        det1 = determinant(np.array([[matrix[1][1],matrix[2][1]],[matrix[1][2],matrix[2][2]]]))
        det2 = determinant(np.array([[matrix[0][1],matrix[2][1]],[matrix[0][2],matrix[2][2]]]))
        det3 = determinant(np.array([[matrix[0][1],matrix[1][1]],[matrix[0][2],matrix[1][2]]]))
        return matrix[0][0]*det1 - matrix[1][0]*det2 + matrix[2][0]*det3



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
        