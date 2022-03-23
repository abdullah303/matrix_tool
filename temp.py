from tkinter import *
from tkinter import ttk
import numpy as np

#GUI for input
def GUI_Input(n,m):

    root = Tk()
    root.title('Table Input')

    #Input frame
    frame = ttk.Frame(root)
    frame.grid(row=0, column=0)


    list_Items = [0]*(n*m)
    N = n
    M = m
    k=0
    for i in range(0, n):
        for j in range(0, m):


            list_Items[k] = ttk.Entry(frame,width=2)
            list_Items[k].grid(row=i+1, column=j+1)
            k+=1


    #Get data from a text box and print it out as a two-dimensional array
    def ButtonClicked_Run():
        B = [0]*(N*M)

        for i in range(N*M):
            B[i] = list_Items[i].get()

        A= np.reshape(B, (N,M))
        print(A)




    #Installation of execute button
    button_Run = ttk.Button(root,
                            text='Run',
                            padding=5,
                            command=ButtonClicked_Run)
    button_Run.grid(row=1, column=0)

    root.mainloop()


#n,Change the number of m to change the number of rows in the table

m = 9
n = 9
GUI_Input(m,n)