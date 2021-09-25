'''自定义类型'''

from typing import Union, Callable, Awaitable, Iterable, List
import enum


class RunAsync(enum.Enum):
    '''Asyncio method'''
    CREATETASK = 0
    GATHER = 1
    ASCOMPLETED = 2
    RUNFOREVER = 3

class RunThreadMap(enum.Enum):
    '''ThreadMap method'''
    MAP = 0 # 暂不支持关键字参数

class RunTreadPool(enum.Enum):
    '''RunTreadPool method'''
    POOL = 0 # 暂不支持关键字参数

class RunGevent(enum.Enum):
    '''Gevent method'''
    GEVENT = 0
    MAP = 1

class RunCalculation(enum.Enum):
    '''Calculation method'''
    APPLY = 0
    APPLYASYNC = 1
    MAP = 2
    MAPASYNC = 3
    EXECUTOR = 4

class RunIOintensive(enum.Enum):
    '''RunIOintensive method'''
    RunAsync_CREATETASK = RunAsync.CREATETASK.value + 10
    RunAsync_GATHER = RunAsync.GATHER.value + 10
    RunAsync_ASCOMPLETED = RunAsync.ASCOMPLETED.value + 10
    RunAsync_RUNFOREVER = RunAsync.RUNFOREVER.value + 10
    RunThreadMap_MAP = RunThreadMap.MAP.value + 20
    RunTreadPool_POOL = RunTreadPool.POOL.value + 30
    RunGevent_GEVENT = RunGevent.GEVENT.value + 40
    RunGevent_MAP = RunGevent.MAP.value + 40

class RunTask(enum.Enum):
    '''RunTask method'''
    APPLY = 0
    APPLYASYNC = 1
    MAP = 2
    MAPASYNC = 3
    EXECUTOR = 4
    RunAsync_CREATETASK = RunAsync.CREATETASK.value + 10
    RunAsync_GATHER = RunAsync.GATHER.value + 10
    RunAsync_ASCOMPLETED = RunAsync.ASCOMPLETED.value + 10
    RunAsync_RUNFOREVER = RunAsync.RUNFOREVER.value + 10
    RunThreadMap_MAP = RunThreadMap.MAP.value + 20
    RunTreadPool_POOL = RunTreadPool.POOL.value + 30
    RunGevent_GEVENT = RunGevent.GEVENT.value + 40
    RunGevent_MAP = RunGevent.MAP.value + 40


RUNASYNC = (RunIOintensive.RunAsync_GATHER, RunIOintensive.RunAsync_CREATETASK, RunIOintensive.RunAsync_ASCOMPLETED, RunIOintensive.RunAsync_RUNFOREVER)

RUNTHREADMAP = (RunIOintensive.RunThreadMap_MAP,)

RUNTHREADPOOL = (RunIOintensive.RunTreadPool_POOL,)

RUNGEVENT = (RunIOintensive.RunGevent_GEVENT, RunIOintensive.RunGevent_MAP)

RUNTASK = (0, 1, 2, 3, 4, 10, 11, 12, 13, 20, 30, 40 ,41)

