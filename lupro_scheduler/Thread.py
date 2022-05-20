'''线程接口'''

import threading
from concurrent.futures import ThreadPoolExecutor
from .typing import Union, Callable, Iterable
from .publictool import init_task

# 重写可返回的线程
class Thread(threading.Thread):
    '''Thread method(可返回)'''

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.target = kwargs['target']
        self.args = kwargs['args']
        self.kwargs = kwargs['kwargs'] if kwargs.get('kwargs') else {}

    def run(self):
        try:
            if self.target:
                self.results = self.target(*self.args, **self.kwargs)
        finally:
            del self.target, self.args, self.kwargs

    def result(self):
        try:
            return self.results   # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

# Thread map 特性 函数 必须要一个Iterable对象
class ThreadMap():
    '''Thread map method'''

    def __init__(self, target = None, *args : "Iterable[tuple]", kwargs : "Iterable[dict]" = None, name : Iterable = None,  daemon : Iterable = None):
        if not (args or name or kwargs or daemon or isinstance(target, Iterable)):
            raise TypeError("ThreadMap() missing 1 required positional argument: 'iterable'")
        d = {'args': (), 'name' : None, 'kwargs' : None, 'daemon' : None}
        self.task = []
        self.l = 0
        if target and isinstance(target, Iterable):
            self.l = len(target)
            d['func'] = target
        if args:
            d['args'] = list(zip(*args))
            self.l = len(d['args'])
        if name:
            d['name'] = name
            if not self.l:
                self.l = len(args)
        if kwargs:
            d['kwargs'] = kwargs
            if not self.l:
                self.l = len(d['kwargs'])
        if daemon:
            d['daemon'] = daemon
            if not self.l:
                self.l = len(daemon)
        for i in d:
            if not d[i]:
                d[i] = [d[i]]*self.l
        if isinstance(target, Callable):
            self.task = [Thread(target = target, name = d['args'][i],args = d['args'][i], kwargs = d['kwargs'][i], daemon = d['daemon'][i]) for i in range(self.l)]
        else:
            self.task = [Thread(target = d['func'][i], name = d['args'][i],args = d['args'][i], kwargs = d['kwargs'][i], daemon = d['daemon'][i]) for i in range(self.l)]
        del d
        
    def start(self):
        for i in self.task:
            i.start()
    
    def join(self):
        for i in self.task:
            i.join()

    def result(self):
        self.join()
        return [i.result() for i in self.task]

    def run(self, method = 0, join = True):
        if method != 0:
            raise TypeError(
                f"ThreadMap.run.method({method}) not in Enum RunThreadMap!")
        self.start()
        if join:
            self.join()
        return self.result()

# 线程池
class ThreadPool():
    '''concurrent.futures.ThreadPoolExecutor method'''

    def __init__(self, func : Union[list, Callable], *args, kwargs = []):
        init_task(self, func = func, args = args, kwargs = kwargs)

    def start(self, max_workers = None, thread_name_prefix='', initializer=None, initargs=(), timeout=None, chunksize=1):
        with ThreadPoolExecutor(max_workers, thread_name_prefix , initializer, initargs) as pool:
            if isinstance(self.func, Callable):
                self.task = pool.map(self.func, *self.args, timeout = timeout, chunksize = chunksize)
            else:
                self.task = [pool.submit(self.func[i], *self.d['args'][i]) for i in range(self.l)]

    def result(self):
        if isinstance(self.task, list):
            return [i.result() for i in self.task]
        return list(self.task)

    def run(self, method = 0):
        if method == 0:
            self.start()
        else:
            raise TypeError(
                f"ThreadPool.run.method({method}) not in Enum ThreadPool!")
        return self.result()