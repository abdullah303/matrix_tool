import numpy as np
arr = np.array([[1,2,3],[4,5,6],[7,8,9]])
ARRstring = np.array2string(arr)
#ARRstring = "[[1,2,3],[4,5,6],[7,8,9]]"
arr2 = np.fromstring(ARRstring, sep=' ')
print("arr \n",arr)
print("ARRstring \n",ARRstring)
print("arr2",arr2)