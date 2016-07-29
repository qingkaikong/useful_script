# import the function from the function module
import func.func as func

# we define an add function here
def add ():
    a = 2
    b = 3
    return a + b
    
# then we actually run the function later in the module function test
func.test(1, add)