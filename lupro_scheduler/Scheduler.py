'''调度器'''

from .Process import ProcessPool
from .Thread import ThreadMap, ThreadPool, Thread
from .Asyncio import Gevent, Asyncio
from .typing import Union, Callable, RunCalculation, RunIOintensive, RunTask
from .Communication import broadcast, Processbroadcast, asyncbroadcast, Lock
from .publictool import tasksequence, dict_slice, taskmethodput
import asyncio
from queue import Empty
import time

# 计算密集型
class Calculation(ProcessPool):
    '''计算密集型'''

    Preferred : RunCalculation = RunCalculation.APPLYASYNC
    '''`Calculation` default `method`'''

    def __init__(self, func: Union[list, Callable], *args, kwargs=[]):
        super().__init__(func, *args, kwargs=kwargs)

    def run(self, method : Union[int, RunCalculation] = None, *args, **kwargs):
        ''' 运行 `Calculation` 计算型密集型实例

        Args:
            `method` : `Union[int, RunCalculation]` 执行方法
            `args` : `tuple` ProcessPool args
            `kwargs` : `dict` ProcessPool kwargs
        
        Returns:
            `List` : 任务返回值列表
        '''
        if method:
            value = method if isinstance(method, int) else method.value
        elif isinstance(Calculation.Preferred, int):
            value = Calculation.Preferred
        else:
            value = Calculation.Preferred.value
        if value in [0, RunCalculation.APPLY]:
            return self.apply(*args, **kwargs)
        elif value in [1, RunCalculation.APPLYASYNC]:
            return self.apply_async(*args, **kwargs)
        elif value in [2, RunCalculation.MAP]:
            return self.map(*args, **kwargs)
        elif value in [3, RunCalculation.MAPASYNC]:
            return self.map_async(*args, **kwargs)
        elif value in [4, RunCalculation.EXECUTOR]:
            return self.Executor(*args, **kwargs)
        else:
            raise TypeError(
                f"Calculation.Preferred({Calculation.Preferred}) or Calculation.run.method({method}) not in Enum RunCalculation!")

# IO密集型
class IOintensive():
    '''IO密集型'''

    Preferred = RunIOintensive.RunThreadMap_MAP
    '''`IOintensive` default `method`'''

    def __init__(self, func: Union[list, Callable], *args, kwargs=[]):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self, method : Union[int, RunIOintensive] = None, *args, **kwargs):
        ''' 运行 `IOintensive` IO型密集型实例

        Args:
            `method` : `Union[int, RunIOintensive]` 执行方法
            `args` : `tuple` ProcessPool args
            `kwargs` : `dict` ProcessPool kwargs
        
        Returns:
            `List` : 任务返回值列表
        '''
        if method:
            value = method if isinstance(method, int) else method.value
        elif isinstance(IOintensive.Preferred, int):
            value = IOintensive.Preferred
        else:
            value = IOintensive.Preferred.value
        if value < 20:
            return Asyncio(self.func, *self.args, kwargs = self.kwargs).run(value - 10)
        elif value < 30:
            return ThreadMap(self.func, *self.args, kwargs = self.kwargs).run(value - 20)
        elif value < 40:
            return ThreadPool(self.func, *self.args, kwargs = self.kwargs).run(value - 30)
        elif value < 50:
            return Gevent(self.func, *self.args, kwargs = self.kwargs).run(value - 40)
        else:
            raise TypeError(
                f"IOintensive.Preferred({Calculation.Preferred}) or IOintensive.run.method({method}) not in Enum RunIOintensive!")

# 任务
class Task:

    Calculation = Calculation

    IOintensive = IOintensive

    def __init__(self, func: Union[list, Callable], *args, kwargs=[], method : Union[int, RunTask] = None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.runm = taskmethodput(method)
        self.method = method
    
    def run(self, method : Union[int, RunTask] = None):
        ''' 运行 `Task` 任务实例

        Args:
            `method` : `Union[int, RunTask]` 执行方法 可重载实例化时的 `method`
        
        Returns:
            `List` : 任务返回值列表
        '''
        if method is None:
            method = self.method
            if method is None:
                raise TypeError(f'Task({self}) method is None')
            task = getattr(Task, self.runm)(self.func,*self.args, kwargs = self.kwargs)
        else:
            task = getattr(Task, taskmethodput(method))(self.func,*self.args, kwargs = self.kwargs)

        return task.run(method)

    @staticmethod
    def threads(func, *args, **kwargs):
        '''异步任务队列'''
        task = Thread(target = func, args = (*args, ), kwargs = kwargs)
        task.start()
        return task

    def length(self):
        return tasksequence(self.func, self.args, self.kwargs)
    
# 调度器  
class Scheduler():
    '''调度器 '''
    
    Calculation = Calculation

    IOintensive = IOintensive

    def __init__(self):
        self.tasks = []     # 任务链
        self.sequence = 0   # 任务链长度
        self.length = 0     # 任务数
        self.lock = []      # 通讯锁
        self.medium = []    # 通讯链路
        self.waits = []     # 中继器线程
        self.results = []   # 任务链结果
    
    def addIO(self, func: Union[list, Callable], *args, kwargs = [], method : Union[int, RunIOintensive] = None):
        ''' 添加 `IOintensive` 型任务

        Args:
            `func` : Union[list, Callable] 任务函数
            `args` : `tuple` 任务位置参数
            `kwargs` : `dict` 任务关键字参数
            `method` : `Union[int, RunIOintensive]` 执行方法 可重载IOintensive.Preferred的 `method`
        
        Returns:
            None 
        '''
        if method is None:
            method = IOintensive.Preferred
        elif taskmethodput(method) != 'IOintensive':
            raise TypeError(
                f"Task.method({method}) not in Enum RunIOintensive!")
        if self.tasks:
            self.tasks.append(Task(func, *args, kwargs = kwargs, method = method))
        else:
            self.tasks.append(Task(func, *args, kwargs = kwargs, method = method))
            self.length = tasksequence(func, args, kwargs)

    def addCal(self, func: Union[list, Callable], *args, kwargs = [], method : Union[int, RunCalculation] = None):
        ''' 添加 `Calculation` 型任务

        Args:
            `func` : Union[list, Callable] 任务函数
            `args` : `tuple` 任务位置参数
            `kwargs` : `dict` 任务关键字参数
            `method` : `Union[int, RunTask]` 执行方法 可重载Calculation.Preferred的 `method`
        
        Returns:
            None 
        '''
        if method is None:
            method = Calculation.Preferred
        elif taskmethodput(method) != 'Calculation':
            raise TypeError(
                f"Task.method({method}) not in Enum RunCalculation!")
        if self.tasks:
            self.tasks.append(Task(func, *args, kwargs = kwargs, method = method))
        else:
            self.tasks.append(Task(func, *args, kwargs = kwargs, method = method))
            self.length = tasksequence(func, args, kwargs)
    
    def run(self, join : bool = True):
        ''' 运行 `Scheduler` 实例

        Args:
            `join` : bool 是否等待调度，当有 `Calculation` 任务时不可不等待
        
        Returns:
            List : 返回有序的调度任务结果
        '''
        if not self.tasks:
            raise TypeError("Scheduler tasks is null!")
        self.sequence = len(self.tasks)
        self.lock = Lock.get_lock(self.tasks, join)
        self.medium = [{} for _ in range(self.sequence)]

            # 序列参数添加 与 通讯装饰器增加
        for i,j in enumerate(self.tasks):
            if isinstance(j.func, list):
                if asyncio.iscoroutinefunction(j.func[0]):
                    j.func = [asyncbroadcast(j.func[z], self.lock[i], self.medium[i]) for z in range(self.length)]
                else:
                    j.func = (
                        [
                            Processbroadcast(
                                j.func[z], self.lock[i], self.medium[i]
                            )
                            for z in range(self.length)
                        ]
                        if j.runm == 'Calculation'
                        else [
                            broadcast(j.func[z], self.lock[i], self.medium[i])
                            for z in range(self.length)
                        ]
                    )

            elif asyncio.iscoroutinefunction(j.func):
                j.func = asyncbroadcast(j.func, self.lock[i], self.medium[i])
            else:
                j.func = (
                    Processbroadcast(j.func, self.lock[i], self.medium[i])
                    if j.runm == 'Calculation'
                    else broadcast(j.func, self.lock[i], self.medium[i])
                )

            if i==0:
                j.args = tuple([list(range(self.length))] + list(j.args))

        # 初始任务
        for i,j in enumerate(self.tasks):
            if i==0:
                task0 = getattr(Scheduler, j.runm)(j.func, *j.args,kwargs = j.kwargs)
                self.threads(task0.run, j.method)
            if i < self.sequence - 1:
                if self.tasks[i].runm == 'Calculation':
                    self.waits.append(self.threads(self.CalRepeater, self.tasks[i+1], self.length, self.lock[i], self.medium[i]))
                else:
                    self.waits.append(self.threads(self.IORepeater, self.tasks[i+1], self.length, self.lock[i], self.medium[i]))
            else:
                self.waits.append(self.threads(self.Interrupt, j, self.length, self.lock[i], self.medium[i]))

        if join:
            self.wait()
            for i in self.medium:
                self.results.append(list(map(lambda x:x[1], sorted(i.items(), key=lambda x:x[0]))))
            return self.results
    
    def IORepeater(self, task, l, lock, medium):
        '''线程 中继器'''
        i = 0
        while i<l:
            with lock:
                a = len(medium)
                if a > i:
                    res = dict_slice(medium, i, a)
                    i = a
                    task.args = (list(res.keys()), list(res.values()))
                    task0 = getattr(Scheduler, task.runm)(task.func, *task.args)
                    self.threads(task0.run, task.method)
            time.sleep(0.1)

    def CalRepeater(self, task, l, lock, medium):
        '''进程 中继器'''
        i = 0
        while i<l:
            while True:
                try:
                    medium.update(lock.get(timeout = 0.1))
                except Empty:
                    a = len(medium)
                    if a > i:
                        res = dict_slice(medium, i, a)
                        i = a
                        task.args = (list(res.keys()), list(res.values()))
                        task0 = getattr(Scheduler, task.runm)(task.func, *task.args)
                        self.threads(task0.run, task.method)
                break
            time.sleep(0.1)

    def Interrupt(self, task, l, lock, medium):
        '''Scheduler 调度完结监听器'''
        i = 0
        if task.runm == 'Calculation':
            while i<l:
                while True:
                    try:
                        medium.update(lock.get(timeout = 0.1))
                    except Empty:
                        a = len(medium)
                        if a > i:
                            i = a
                    break
                time.sleep(0.1)
        else:
            while i<l:
                with lock:
                    a = len(medium)
                    if a > i:
                        i = a
                time.sleep(0.1)

    def wait(self):
        for i in self.waits:
            i.join()

    @staticmethod
    def threads(func, *args, **kwargs):
        '''异步任务队列'''
        task = Thread(target = func, args = (*args, ), kwargs = kwargs)
        task.start()
        return task