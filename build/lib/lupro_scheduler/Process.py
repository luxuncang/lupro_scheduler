from .typing import Union, Callable
from .publictool import SeparateArgs, init_task
from multiprocessing import Process as process

# 进程(无返回值)
class Process(process):
    '''Process method'''

    def __init__(self, group = None, target = None, name = None, args = (), kwargs = {}, *, daemon = None):
        super(Process, self).__init__(group, target, name, args, kwargs, daemon = daemon)
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        '''Process.run method'''
        if self.target:
            self.target(*self.args, **self.kwargs)

# 多进程或进程池 multiprocessing.Pool ProcessPoolExecutor
class ProcessPool():
    '''ProcessPool.multiprocessing.Pool or ProcessPool.ProcessPoolExecutor method'''

    def __init__(self, func : Union[list, Callable], *args, kwargs = []):
        init_task(self, func = func, args = args, kwargs = kwargs)

    def apply_async(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None, callback = None, error_callback = None):
        '''multiprocessing.Pool.apply_async method'''
        from multiprocessing import Pool
        pool = Pool(processes = processes, initializer = initializer, initargs = initargs, maxtasksperchild = maxtasksperchild)
        if isinstance(self.func, Callable):
            for i in range(self.l):
                self.task.append(pool.apply_async(self.func, args = self.d['args'][i], kwds = self.d['kwargs'][i], callback = callback, error_callback = error_callback))
        else:
            for i in range(self.l):
                self.task.append(pool.apply_async(self.func[i], args = self.d['args'][i], kwds = self.d['kwargs'][i], callback = callback, error_callback = error_callback))
        pool.close()
        pool.join()
        return [i.get() for i in self.task]
    
    def apply(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None):
        '''multiprocessing.Pool.apply method'''
        from multiprocessing import Pool
        pool = Pool(processes = processes, initializer = initializer, initargs = initargs, maxtasksperchild = maxtasksperchild)
        if isinstance(self.func, Callable):
            for i in range(self.l):
                self.task.append(pool.apply(self.func, args = self.d['args'][i], kwds = self.d['kwargs'][i]))
        else:
            for i in range(self.l):
                self.task.append(pool.apply(self.func[i], args = self.d['args'][i], kwds = self.d['kwargs'][i]))
        pool.close()
        pool.join()
        return self.task

    def map(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None, chunksize = None):
        '''multiprocessing.Pool.map method'''
        from multiprocessing import Pool
        pool = Pool(processes = processes, initializer = initializer, initargs = initargs, maxtasksperchild = maxtasksperchild)
        if isinstance(self.func, Callable):
            self.task = pool.map(SeparateArgs(self.func), self.d['args'], chunksize)
        else:
            self.task = pool.map(SeparateArgs(self.func[0]), self.d['args'], chunksize)
        pool.close()    # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        pool.join() 
        return self.task
    
    def map_async(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None, chunksize=None, callback=None, error_callback=None):
        '''multiprocessing.Pool.map_async method'''
        from multiprocessing import Pool
        pool = Pool(processes = processes, initializer = initializer, initargs = initargs, maxtasksperchild = maxtasksperchild)
        if isinstance(self.func, Callable):
            self.task = pool.map_async(SeparateArgs(self.func), self.d['args'], chunksize)
        else:
            self.task = pool.map_async(SeparateArgs(self.func[0]), self.d['args'], chunksize)
        pool.close()    # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
        pool.join() 
        return self.task.get()

    def Executor(self, max_workers=None, mp_context=None, initializer=None, initargs=(), timeout=None, chunksize=1):
        '''concurrent.futures.ProcessPoolExecutor.(map, submit) method'''
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers = max_workers, mp_context = mp_context, initializer = initializer, initargs = initargs) as pool:
            if isinstance(self.func, Callable):
                self.task = pool.map(self.func, *self.args, timeout = timeout, chunksize = chunksize)
            else:
                self.task = [pool.submit(self.func[i], *self.d['args'][i]) for i in range(self.l)]
        def result(self):
            if isinstance(self.task, list):
                return [i.result() for i in self.task]
            return list(self.task)
        return result(self)
