from threads import InfiniteThread
import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Threaded(object):

    THREADS = {}
    JOINABLE = {}

    def __init__(self):
        pass

    @staticmethod
    def infinite(name, prefix=None):
        try:
            thd_pool = Threaded.get_thd_pool(name, prefix)
        except KeyError:
            logger.debug("Creating new pool for " + str(prefix) + "_" + str(name))
            thd_pool = {}
            pool_name = Threaded.get_pool_name(name, prefix)
            Threaded.THREADS[pool_name] = thd_pool

        thd = InfiniteThread()
        thd_pool[0] = thd

        def infinite_decorator(f):
            def wrapper(*args, **kwargs):
                _id = kwargs.pop('_id', None)
                if not _id:
                    _id = 0

                worker_thd = thd_pool.get(_id)

                if not worker_thd:
                    logger.debug("Worker with id " + str(_id) + "not found")
                    worker_thd = InfiniteThread()
                    thd_pool[_id] = worker_thd

                worker_thd.task = f
                worker_thd.task_args = args
                worker_thd._task_kwargs = kwargs

                worker_thd.start()

            return wrapper

        return infinite_decorator

    @staticmethod
    def before_task(name, prefix=None):
        thd = Threaded.get_thd(name, prefix, 0)

        def before_task_decorator(f):
            if thd:
                thd.before_task = f

            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped

        return before_task_decorator

    @staticmethod
    def after_task(name, prefix=None):
        thd = Threaded.get_thd(name, prefix, 0)

        def after_task_decorator(f):
            if thd:
                thd.after_task = f

            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapped

        return after_task_decorator

    @staticmethod
    def start_thread(name, prefix=None, _id=0):
        thd = Threaded.get_thd(name, prefix, _id)
        thd.start()

    @staticmethod
    def stop_thread(name, prefix=None, join=False, _id=0):
        thd_pool = Threaded.get_thd_pool(name, prefix)
        thd = thd_pool.pop(_id, None)

        if thd:
            thd.stop()

            if join:
                thd.join()
            else:
                pool_name = Threaded.get_pool_name(name, prefix)
                joinable_pool = Threaded.JOINABLE.get(pool_name)

                if not joinable_pool:
                    joinable_pool = {}
                    Threaded.JOINABLE[pool_name] = joinable_pool

                joinable_pool[_id] = thd
        else:
            raise KeyError("Thread with id " + str(_id) + " and prefix " +
                           str(prefix) + " not found")

    @staticmethod
    def resume_thread(name, prefix=None, _id=0):
        thd = Threaded.get_thd(name, prefix, _id)
        thd.resume()

    @staticmethod
    def pause_thread(name, prefix=None, _id=0):
        thd = Threaded.get_thd(name, prefix, _id)
        thd.pause()

    @staticmethod
    def join_thread(name, prefix=None, _id=0):
        pool = Threaded.get_joinable_pool(name, prefix)
        thd = pool.pop(_id, None)

        if not thd:
            raise KeyError("Thread with name " + str(name) + ", prefix " +
                           str(prefix) + " and id " + str(_id) + " not found")

        thd.join()

    @staticmethod
    def get_pool_name(name, prefix):
        return str(prefix) + '_' + str(name)

    @staticmethod
    def get_thd_pool(name, prefix):
        pool_name = Threaded.get_pool_name(name, prefix)
        thd_pool = Threaded.THREADS.get(pool_name)

        if not thd_pool:
            raise KeyError("Thread pool with name " + str(name) +
                           " andr prefix " + str(prefix) + " not found")

        return thd_pool

    @staticmethod
    def get_thd(name, prefix, _id):
        thd_pool = Threaded.get_thd_pool(name, prefix)
        thd = thd_pool.get(_id, None)

        if not thd:
            raise KeyError("Thread with name " + str(name) + ", prefix " +
                           str(prefix) + " and id " + str(_id) + " not found")

        return thd

    @staticmethod
    def get_joinable_pool(name, prefix):
        pool_name = Threaded.get_pool_name(name, prefix)
        pool = Threaded.JOINABLE.get(pool_name)

        if not pool:
            raise KeyError("No joinable pool with name " + str(name) +
                           " and prefix " + str(prefix) + " found")

        return pool

    def stop_all_threads(self):
        for thd in self.threads:
            thd.stop()

        for thd in self.threads:
            thd.join()
