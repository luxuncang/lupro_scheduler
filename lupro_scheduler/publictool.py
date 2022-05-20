'''通用工具'''

import asyncio
from .typing import Union, Callable, Iterable, RunTask, RUNTASK, RunIOintensive, RunCalculation

# 参数分离
class SeparateArgs():
    '''参数分离'''

    def __init__(self, func):
        self.func = func
    
    def __call__(self, args):
        return self.func(*args)

# 泛属性元类
class inherit(type):
    '''类泛属性'''

    def __getattr__(self, name):
        if '__general__' not in dir(self):
            raise NameError("name '__general__' is not defined")
        if hasattr(self.__general__, name):
            return getattr(self.__general__, name)
        return getattr(object.__getattr__, name)

# 调用类对象属性
def calling_methodc(cls ,name):
    '''调用类对象属性'''
    return getattr(cls, name)()

# 任务长度
def tasksequence(func, args, kwargs):
    '''Scheduler sequence'''
    if isinstance(func, list):
        return len(func)
    elif args and isinstance(args[0], Iterable):
        return len(args[0])
    elif isinstance(kwargs, list):
        return len(kwargs)
    else:
        raise TypeError("One Scheduler Task must have an Iterable!")

# Asyncio类的特殊判断方式(弃用)
def classput(self, func):
    if type(self).__name__ == 'Asyncio':
        return asyncio.iscoroutinefunction(func)
    else:
        return isinstance(func, Callable)

# 初始化任务参数解析
def init_task(self, func, args, kwargs):
    '''通用初始化任务参数解析'''
    self.l = 0
    d = {'args': (), 'kwargs': {}}
    if isinstance(func, list):
        self.l = len(func)
    # elif classput(self ,func):
    #     pass
    if args:
        d['args'] = list(zip(*args))
        self.l = len(d['args'])
    if kwargs:
        d['kwargs'] = kwargs
        if not self.l:
            self.l = len(d['kwargs'])
    if not self.l:
        raise TypeError(f"{type(self).__name__}() missing 1 required positional argument: 'iterable' or 'func[callable]'")
    for i in d:
        if not d[i]:
            d[i] = [d[i]] *self.l
    self.d = d
    self.func = func
    self.task = []
    self.args = args

# 切片字典
def dict_slice(adict, start, end):
    '''切片字典'''
    keys = adict.keys()
    return {k: adict[k] for k in list(keys)[start:end]}

# Task 方法判断
def taskmethodput(method : Union[int, RunTask]):
    '''Task 方法判断'''
    if isinstance(method, int):
        value = method
    elif isinstance(method, RunTask) or isinstance(method, RunCalculation) or isinstance(method, RunIOintensive):
        value = method.value
    else:
        raise TypeError(
                f"Task.method({method}) not in Enum RunTask!")
    if value in RUNTASK:
        return 'Calculation' if value < 10 else 'IOintensive'
    else:
        raise TypeError(
                f"Task.method({method}) not in Enum RunTask!")
