import threading # 线程
from multiprocessing import Manager
import asyncio

# 通迅锁
class Lock():
    '''通迅锁'''

    @staticmethod
    def lock():
       return threading.Lock()

    @staticmethod
    def RLock():
        return threading.RLock()
    
    @staticmethod
    def Manager_RLock():
        return Manager().RLock()

    @staticmethod
    def Manager_Queue():
        return Manager().Queue()

    @staticmethod
    def get_lock(tasks, join):
        res = []
        for i in tasks:
            if i.runm == 'IOintensive':
                res.append(Lock.RLock())
            elif i.runm == 'Calculation' and join:
                res.append(Lock.Manager_Queue())
            else:
                raise TypeError("Calculation Task can't wait!")
        return res

# IO广播通迅装饰器
class broadcast():
    '''IO广播通迅装饰器'''

    def __init__(self, func, lock, medium):
        self.func = func
        self.lock = lock
        self.medium = medium
    
    def __call__(self, *args, **kwargs):
        res = self.func(*args[1:], **kwargs)
        with self.lock:
            self.medium[args[0]] = res
        return res

# asyn广播通迅装饰器
class asyncbroadcast():
    '''asyn广播通迅装饰器'''

    def __init__(self, func, lock, medium):
        self.func = func
        self.lock = lock
        self.medium = medium
    
    async def __call__(self, *args, **kwargs):
        res = await self.func(*args[1:], **kwargs)
        with self.lock:
            self.medium[args[0]] = res
        return res

# Calculate广播通迅装饰器
class Processbroadcast():
    '''Calculate广播通迅装饰器'''

    def __init__(self, func, queue, medium):
        self.func = func
        self.queue = queue
        self.medium = medium
    
    def __call__(self, *args, **kwargs):
        res = self.func(*args[1:], **kwargs)
        self.queue.put({args[0]:res})
        return res

