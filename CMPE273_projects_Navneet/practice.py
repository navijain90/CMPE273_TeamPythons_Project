from functools import wraps

# def get_text(name):
#     print "Inisde get text"
#     return "lorem ipsum, {0} dolor sit amet".format(name)
#
# def p_decorate(func):
#     print "Inside p_decorator"
#     def func_wrapper(name):
#        print "Inside func_wrapper"
#        return "<p>{0}</p>".format(func(name))
#     return func_wrapper
#
# my_get_text = p_decorate(get_text)
#
# print my_get_text("John")

# def p_decorator(func):
#     def func_wrapper(*args,**kwargs):
#         return "<p>{0}<p>".format(func(args))
#     return func_wrapper
# def s_decorator(func):
#     def func_wrapper(*args,**kwargs):
#         return "<div>{0}".format(func(args))
#     return func_wrapper
#
# @p_decorator
# @s_decorator
# def getname(name):
#     return "this is my {0} decorator".format(name)
# print  getname("john")

from functools import wraps
def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print args
        print 'Calling decorated function'
        return f(*args, **kwargs)
    return wrapper

@my_decorator
def example(a=10):
    """Docstring"""
    print 'Called example function' +str(a)
example()
print example.__name__
print example.__doc__
