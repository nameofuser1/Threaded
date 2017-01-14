from threads import InfiniteThread


class Threaded(object):

    INFINITE_THD = 'infinite'
    ONE_TIME_THD = 'one_time'

    THREADS = {}
    JOINABLE = {}

    def __init__(self):
        pass

    @staticmethod
    def infinite(_id, prefix=None):
        thd_name = Threaded.get_thd_name(_id, prefix)

        thd = InfiniteThread()
        Threaded.THREADS[thd_name] = thd

        def infinite_decorator(f):
            def wrapper(*args, **kwargs):
                thd.task = f
                thd.task_args = args
                thd._task_kwargs = kwargs

                thd.start()

            return wrapper

        return infinite_decorator

    @staticmethod
    def before_task(_id, prefix=None):
        thd_name = Threaded.get_thd_name(_id, prefix)
        thd = Threaded.THREADS.get(thd_name, None)

        if not thd:
            raise KeyError("Thread with id " + str(_id) + " and prefix " +
                           str(prefix) + " not found")

        def before_task_decorator(f):
            if thd:
                thd.before_task = f

            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped

        return before_task_decorator

    @staticmethod
    def after_task(_id, prefix=None):
        thd_name = Threaded.get_thd_name(_id, prefix)
        thd = Threaded.THREADS.get(thd_name, None)

        if not thd:
            raise KeyError("Thread with id " + str(_id) + " and prefix " +
                           str(prefix) + " not found")

        def after_task_decorator(f):
            if thd:
                thd.after_task = f

            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapped

        return after_task_decorator

    @staticmethod
    def start_thread(_id, prefix=None):
        thd = Threaded.get_thd(_id, prefix)
        thd.start()

    @staticmethod
    def stop_thread(_id, prefix=None, join=False):
        thd_name = Threaded.get_thd_name(_id, prefix)
        thd = Threaded.THREADS.pop(thd_name, None)

        if thd:
            thd.stop()

            if join:
                thd.join()
            else:
                Threaded.JOINABLE[thd_name] = thd
        else:
            raise KeyError("Thread with id " + str(_id) + " and prefix " +
                           str(prefix) + " not found")

    @staticmethod
    def resume_thread(_id, prefix=None):
        thd = Threaded.get_thd(_id, prefix)
        thd.resume()

    @staticmethod
    def pause_thread(_id, prefix=None):
        thd = Threaded.get_thd(_id, prefix)
        thd.pause()

    @staticmethod
    def join_thread(_id, prefix=None):
        thd = Threaded.get_thd(_id, prefix)
        thd.join()

    @staticmethod
    def get_thd_name(_id, prefix):
        return str(prefix) + '_' + str(_id)

    @staticmethod
    def get_thd(_id, prefix):
        name = Threaded.get_thd_name(_id, prefix)
        thd = Threaded.THREADS.get(name, None)

        if not thd:
            raise KeyError("Thread with id " + str(_id) + " and prefix " +
                           str(prefix) + " not found")

        return thd

    def stop_all_threads(self):
        for thd in self.threads:
            thd.stop()

        for thd in self.threads:
            thd.join()
