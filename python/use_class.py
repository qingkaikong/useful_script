'''
The snippet contains:

How to declare and use a class with attributes and methods
How to declare a class using inheritance

grab from 
http://glowingpython.blogspot.com/2011/04/how-to-define-class-using-inheritance.html
'''

class Point2D:
 """ a point in a 2D space """
 name = "A dummy name" # attribute

 def __init__(self,x,y): # constructor
  self.x = x
  self.y = y

 def product(self,p): # method
  """ product with another point """
  return self.x*p.x + self.y*p.y

 def print_2D(self):
  print "(",self.x,",",self.y,")"

class Point3D(Point2D): # Point3D inherit Point2D
 def __init__(self,x,y,z):
  self.x = x
  self.y = y
  self.z = z

 def print_3D(self):
  print "(",self.x,",",self.y,",",self.z,")"

## just test the our classes ##

p2 = Point2D(1,2)
p2.print_2D()
print p2.product(Point2D(2,1))

p3 = Point3D(5,4,3)
p3.print_2D()
p3.print_3D() # inherited method
print p3.name # inherited attribute
print dir(Point2D)
print dir(Point3D) # dir return a list with attribute and methods of the class