#class to print out the x, y coordinate
class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "Coord: " + str(self.__dict__)

#function to add        
def add(a, b):
    return Coordinate(a.x + b.x, a.y + b.y)
#function to substract        
def sub(a, b):
    return Coordinate(a.x - b.x, a.y - b.y)
    
one = Coordinate(100, 200)
two = Coordinate(300, 200)

def wrapper(func):
    def checker(a, b): # 1
        if a.x < 0 or a.y < 0:
            a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
        if b.x < 0 or b.y < 0:
            b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
        ret = func(a, b)
        if ret.x < 0 or ret.y < 0:
            ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
        return ret
    return checker

#Here we got negative value from the sub function
print sub(one, two)

#But we need check if the result is negative, then we want it to be 0 (non-negative)
#We add a wrapper on it, this is actually a decoration on the original function
add = wrapper(add)
sub = wrapper(sub)
print sub(one, two)

#now use the decoratior operator
@wrapper
def sub1(a, b):
    return Coordinate(a.x - b.x, a.y - b.y)

#we will get the same result as above
print sub1(one, two)