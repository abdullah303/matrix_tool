
from operator import index
import tkinter as tk
import numpy as np
import pandas as pd
import csv
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
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False, index=False)

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
        dataframe.to_csv(os.path.join(os.getcwd(), "exercises", self.file_name), mode="a", header=False, index=False)


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

# class DisplayArray(tk.Frame):
#     def __init__(self, parent, array):
#         array = np.frombuffer(np.array(array), dtype=)
        

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
        variable = tk.StringVar(self)
        menu = tk.OptionMenu(self, variable, *exercises)
        menu.grid()

        tk.Button(self, text="select exercise", command=lambda: self.setExercise(variable)).grid()
        tk.Button(self, text="Next Question", command=lambda: self.nextQ()).grid()
        tk.Button(self, text="Previous Question", command=lambda: self.previousQ()).grid()
        # labelType = tk.Label(self, text="Question Type", font={"Helvetica", 20}, width=25).grid(row=0, column=1, padx=10, pady=10)
        # labelMat1 = tk.Label(self, text="Matrix1", font={"Helvetica", 20}, width=25).grid(row=1, column=1, padx=10, pady=10)
        # labelMat2 = tk.Label(self, text="Matrix2", font={"Helvetica", 20}, width=25).grid(row=1, column=2, padx=10, pady=10)
        # ans = tk.Label(self ,text = "Answer").grid(row = 10,column = 1)
        self.answer = tk.StringVar()
        ansForm = tk.Entry(self, textvariable=self.answer).grid(row=11, column=1)
        buttonANS = tk.Button(self, text="Check Answer", command=lambda: self.checkANS(self.setExercise(variable))).grid(row=12, column=1, padx=10, pady=10)
        answerFormat = tk.Label(self, text="Give answer in format [[x1,x2,x3],[x4,x5,x6],[x7,x8,x9]]").grid(row=13, column=1, padx=10, pady=10)

    def setExercise(self, variable):
        self.current_exercise = variable.get()
        path = os.path.join(os.getcwd(), "exercises", self.current_exercise)
        df = pd.read_csv(path)
        print(df.iloc[:,0])
        File = open(path)
        Reader = csv.reader(File)
        Data = list(Reader)
        # del(Data[0])

        list_of_entries = []
        for x in list(range(0,len(Data))):
            list_of_entries.append(Data[x][0])
        var = tk.StringVar(value = list_of_entries)
        listbox1 = tk.Listbox(self, listvariable = var)
        listbox1.grid(row=10 , column=0)

        def update():
            index = listbox1.curselection()[0]
            operationLabel2.config(text = Data[index][0])
            matrix1Label2.config(text = Data[index][1])
            matrix2Label2.config(text = Data[index][2])
            # answerlabel2.config(text = Data[index][3])
            
            return (index, Data[index][0], Data[index][1], Data[index][2])

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
        print(self.current_exercise)
        return update()

    def checkANS(self, bigtuple):
        index, DataOperation, matrix1, matrix2 = bigtuple
        #(index, DataOperation, DataMat1, DataMat2) bigtuple
        if DataOperation == "addition":
                    if self.answer.get() == str(np.add(np.array(matrix1), np.array(matrix2)).tolist()).replace(" ", ""):
                        print("answer is correct")
                    else:
                        print("answer is incorrect")
                        print(self.answer.get())
                        print(str(np.add(np.array(matrix1), np.array(matrix2)).tolist()).replace(" ", ""))
        elif DataOperation == "subtraction":
            if self.answer.get() == str(np.subtract(np.array(matrix1), np.array(matrix2)).tolist()).replace(" ", ""):
                print("answer is correct")
            else:
                print("answer is incorrect")
        elif DataOperation == "multiplication":
            if self.answer.get() == str(np.multiply(np.array(matrix1), np.array(matrix2)).tolist()).replace(" ", ""):
                print("answer is correct")
            else:
                print("answer is incorrect")
        elif DataOperation == "eigenvalue":
            values, vector = np.linalg.eigh(np.array(matrix1))
            if self.answer.get() == (str(values[0])) or self.answer.get() == (str(values[1])):
                print("answer is correct")
            else:
                print("answer is incorrect")
        elif DataOperation == "eigenvector":
            values, vector = np.linalg.eigh(np.array(matrix1))
            if self.answer.get() == (str(vector).tolist()).replace(" ", ""):
                print("answer is correct")
            else:
                print("answer is incorrect")
        elif DataOperation == "inverse":
            if self.answer.get() == str(np.linalg.inv(np.array(matrix1)).tolist()).replace(" ", ""):
                print("answer is correct")
            else:
                print("answer is incorrect")
        elif DataOperation == "determinant":
            if self.answer.get() == (str(determinant(matrix1))):
                print("answer is correct")
            else:
                print("answer is incorrect")

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


class DoExercisePage(CompleteExercisePage):
    def __init__(self, parent, controller):
        pass


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
        