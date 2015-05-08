import time

#decorator for timing the function
def time_dec(func):

  def wrapper(*arg):
      t = time.clock()
      res = func(*arg)
      print func.func_name, time.clock()-t
      return res

  return wrapper

@time_dec
def myFunction(n):
    x = 0
    for i in range(n):
        x = i    
        
myFunction(100000)

