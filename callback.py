def inner():
    print("I am function inner()")

def another_func():
    print("To be or not to be")
    
def sum(a,b):
    print(str(a + b))

def outer(function):
    function(5,3)

def main():
    outer(sum)
    
main()