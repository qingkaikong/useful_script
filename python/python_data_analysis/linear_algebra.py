
#inverse an matrix
import numpy as np
A = np.mat("2 4 6;4 2 6;10 -4 18")
print "A\n", A
inverse = np.linalg.inv(A)
print "inverse of A\n", inverse
print "Check\n", A * inverse
print "Error\n", A * inverse - np.eye(3)

#solve linear system with numpy
import numpy as np
A = np.mat("1 -2 1;0 2 -8;-4 5 9")
print "A\n", A
b = np.array([0, 8, -9])
print "b\n", b
x = np.linalg.solve(A, b)
print "Solution", x
print "Check\n", np.dot(A , x)

#find eigenvalue and eigenvectors
import numpy as np
A = np.mat("3 -2;1 0")
print "A\n", A
print "Eigenvalues", np.linalg.eigvals(A)
eigenvalues, eigenvectors = np.linalg.eig(A)
print "First tuple of eig", eigenvalues
print "Second tuple of eig\n", eigenvectors
for i in range(len(eigenvalues)):
    print "Left", np.dot(A, eigenvectors[:,i])
    print "Right", eigenvalues[i] * eigenvectors[:,i]
    print
    
