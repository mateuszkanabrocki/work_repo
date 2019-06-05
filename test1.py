def foo(a):
    if a > 0:
        print ('Hi')
    else:
        print("3" + 5) # won't raise error in foo(2)

foo(2)