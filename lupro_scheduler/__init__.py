'''
Lupro Scheduler Library
~~~~~~~~~~~~~~~~~~~~~

Lupro Scheduler is a synchronous task chain scheduler support sweeper, multi-thread, multi-process synchronous communication

* `简单使用`

   >>> from lupro_scheduler import scheduler
   >>> task = scheduler()
   >>> task.addIO(func, range(10))
   >>> task.run()

其它 `scheduler.api` 请参考 <https://github.com/luxuncang/lupro_scheduler>.

:copyright: (c) 2021 by ShengXin Lu.
'''

from .Scheduler import Scheduler, Task, IOintensive, Calculation
from .Asyncio import Gevent, Asyncio
from .Process import Process, ProcessPool
from .Thread import Thread, ThreadMap, ThreadPool
from .typing import RunIOintensive, RunCalculation, RunTask
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__
