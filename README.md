# Lupro Scheduler

**Lupro Scheduler 是一个任务链同步调度器(支持协程,线程,进程同步通讯)**

## 安装 `Lupro Scheduler`

### 使用 [PyPi](https://pypi.org/) 安装 Lupro

* `pip` Find, install and publish Python packages with the Python Package Index
* `pip install lupro-scheduler`

## 开始使用

1. 导入 `from lupro_scheduler import Scheduler`

### 调度任务Task

```python
from lupro_scheduler import Task
from lupro_scheduler.typing import RunIOintensive
import asyncio

async def main(a, b):
    await asyncio.sleep(2)
    return a+b

task = Task(main, range(10), kwargs = [{'b': i} for i in range(10)], method = RunIOintensive. RunAsync_CREATETASK)
print(task.run())
```

_这样即可使用RunTask调用不同的执行方法_

### 调用方法 RunTask

```python
class RunTask(enum.Enum):
    '''RunTask method'''
    APPLY = 0
    APPLYASYNC = 1
    MAP = 2
    MAPASYNC = 3
    EXECUTOR = 4
    RunAsync_CREATETASK = 10
    RunAsync_GATHER = 11
    RunAsync_ASCOMPLETED = 12
    RunAsync_RUNFOREVER = 13
    RunThreadMap_MAP = 20
    RunTreadPool_POOL = 30
    RunGevent_GEVENT = 40
    RunGevent_MAP = 41
```

### 任务链调度 Scheduler

```python
from lupro_scheduler import Scheduler
from lupro_scheduler.typing import RunIOintensive
import random
import asyncio
import time

async def main(a, b):
    await asyncio.sleep(random.randint(4,8))
    print(f'IOintensive task {a} {b}!')
    return a+b

def main1(a):
    print(f'Calintensive task {a}!')
    time.sleep(random.randint(1,4))
    return a**a

if __name__ == '__main__':
    task = Scheduler()
    # 添加IO密集型任务
    task.addIO(main, range(10), kwargs = [{'b': i} for i in range(10)], method = 10)
    # 添加计算密集型任务
    task.addCal(main1)
    # 大概12s左右完成
    print(task.run())
```

## 特性

* [X] 协程接口
* [X] 线程接口
* [X] 进程接口
* [X] 任务链异步调度
* [X] 任务链同步调度
* [X] Scheduler(IO) 可等待

## api 文档

**完善中**
