from abc import abstractmethod, ABCMeta
from threading import Event, Thread


class CustomThread(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._task = None
        self._before_task = self.dummy_task
        self._after_task = self.dummy_task

        self._task_args = []
        self._task_kwargs = {}

        self.thread = None

    @property
    def task_args(self):
        return self._task_args

    @task_args.setter
    def task_args(self, args):
        self._task_args = args

    @property
    def task_kwargs(self):
        return self._task_kwargs

    @task_kwargs.setter
    def task_kwargs(self, kwargs):
        self._task_kwargs = kwargs

    @property
    def before_task(self):
        """
        Called before infinite loop
        """
        return self._before_task

    @before_task.setter
    def before_task(self, task):
        self._before_task = task

    @property
    def after_task(self):
        """
        Called after loop
        """
        return self._after_task

    @after_task.setter
    def after_task(self, task):
        self._after_task = task

    def join(self):
        self.thread.join()

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, task):
        self._task = task

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def start(self):
        pass


class InfiniteThread(CustomThread):

    def __init__(self):
        CustomThread.__init__(self)
        self._pause = Event()
        self.running = False

    def start(self):
        if (not self.running) and (self._task):
            self.running = True
            self._pause.set()
            self.thread = Thread(target=self.loop)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False

    def pause(self):
        self._pause.clear()

    def resume(self):
        self._pause.set()

    def loop(self):
        self._before_task()

        while self.running:
            self._pause.wait()
            self._task(*self._task_args, **self._task_kwargs)

        self._after_task()

    def dummy_task(self):
        pass
