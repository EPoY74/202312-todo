import inspect

def bar():
    current_frame = inspect.currentframe()
    previous_frame = current_frame.f_back
    print (previous_frame.f_code.co_name)

def foo():
    bar()

foo()