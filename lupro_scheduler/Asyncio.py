'''协程接口'''
import asyncio
from .typing import Union, Callable, RunAsync, RunGevent
from .publictool import SeparateArgs, init_task

class Gevent():
    '''gevent method'''

    def __init__(self, func : Union[list, Callable], *args, kwargs = []):
        init_task(self, func = func, args = args, kwargs = kwargs)

    def run(self, method : Union[RunGevent, int], *args, **kwargs):
        if method in [RunGevent.GEVENT, RunGevent.GEVENT.value]:
            return self.gevent()
        elif method in [RunAsync.GATHER, RunAsync.GATHER.value]:
            return self.map(*args, **kwargs)
        else:
            raise TypeError(
                f"Asyncio.{self}({method}) not in Enum RunAsync!")

    def gevent(self):
        '''gevent.spawn method'''
        import gevent
        from gevent import monkey
        monkey.patch_all()  # 先引用
        if isinstance(self.func, Callable):
            self.task = [gevent.spawn(self.func, *self.d['args'][i], **self.d['kwargs'][i]) for i in range(self.l)]
        else:
            self.task = [gevent.spawn(self.func[i], *self.d['args'][i], **self.d['kwargs'][i]) for i in range(self.l)]
        gevent.joinall(self.task)
        return [i.value for i in self.task]

    def map(self, size=None, greenlet_class=None):
        '''gevent.pool.Pool.map method'''
        import gevent.pool
        from gevent import monkey
        monkey.patch_all()  # 先引用
        pool = gevent.pool.Pool(size=size, greenlet_class=greenlet_class)
        if isinstance(self.func, Callable):
            self.task = pool.map(SeparateArgs(self.func), self.d['args'])
        else:
            self.task = pool.map(SeparateArgs(self.func[0]), self.d['args'])
        return self.task

class Asyncio():
    '''asyncio method'''

    def __init__(self, func : Union[list, Callable], *args, kwargs = []):
        init_task(self, func = func, args = args, kwargs = kwargs)

    def run(self, method : Union[RunAsync, int]):
        '''Asyncio run method'''
        if method in [RunAsync.CREATETASK, RunAsync.CREATETASK.value]:
            return asyncio.run(self.create_task())
        elif method in [RunAsync.GATHER, RunAsync.GATHER.value]:
            return asyncio.run(self.gather())
        elif method in [RunAsync.ASCOMPLETED, RunAsync.ASCOMPLETED.value]:
            return asyncio.run(self.as_completed())
        elif method in [RunAsync.RUNFOREVER, RunAsync.RUNFOREVER.value]:
            return asyncio.run(self.get_event_loop())
        else:
            raise TypeError(
                f"Asyncio.{self}({method}) not in Enum RunAsync!")

    async def create_task(self):
        '''asyncio.create_task method'''
        if isinstance(self.func, Callable):
            self.task = [asyncio.create_task(self.func(*self.d['args'][i], **self.d['kwargs'][i])) for i in range(self.l)]
        else:
            self.task = [asyncio.create_task(self.func[i](*self.d['args'][i], **self.d['kwargs'][i])) for i in range(self.l)]
        await self.wait()
        return [i.result() for i in self.task]
    
    async def gather(self):
        '''asyncio.gather method'''
        if isinstance(self.func, Callable):
            self.task = await asyncio.gather(*(self.func(*self.d['args'][i], **self.d['kwargs'][i]) for i in range(self.l)))
        else:
            self.task = await asyncio.gather(*(self.func[i](*self.d['args'][i], **self.d['kwargs'][i]) for i in range(self.l)))
        return self.task

    async def as_completed(self):
        '''asyncio.as_completed method'''
        # 返回值无序
        if isinstance(self.func, Callable):
            for i in asyncio.as_completed([self.func(*self.d['args'][i], **self.d['kwargs'][i]) for i in range(self.l)]):
                self.task.append(await i)
        else:
            for i in asyncio.as_completed([self.func[i](*self.d['args'][i], **self.d['kwargs'][i]) for i in range(self.l)]):
                self.task.append(await i)
        return self.task 

    async def get_event_loop(self):
        '''asyncio.get_event_loop().create_task method'''
        loop = asyncio.get_event_loop()
        if isinstance(self.func, Callable):
            self.task = [loop.create_task(self.func(*self.d['args'][i], **self.d['kwargs'][i])) for i in range(self.l)]
        else:
            self.task = [loop.create_task(self.func[i](*self.d['args'][i], **self.d['kwargs'][i])) for i in range(self.l)]
        await self.wait()
        return self.task
    
    async def wait(self):
        for i in self.task:
            await i
