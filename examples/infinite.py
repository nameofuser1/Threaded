from threaded import Threaded
from time import sleep

_id = 0


@Threaded.infinite("write_thd")
def write_id(writer_name):
    global _id

    _id += 1
    print(writer_name + ' increased id by one. id = ' + str(_id))

    sleep(1)


@Threaded.before_task("write_thd")
def init_id():
    global _id
    _id = 1
    print("Initialized id with value " + str(_id))


@Threaded.after_task("write_thd")
def finalize_id():
    global _id
    _id += 1
    print("Finalized id. id = " + str(_id))


if __name__ == "__main__":
    write_id("Writer1")
    sleep(3)
    Threaded.pause_thread("write_thd")
    sleep(3)
    Threaded.resume_thread("write_thd")
    sleep(3)
    Threaded.stop_thread("write_thd", join=True)
