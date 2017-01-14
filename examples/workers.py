from threaded import Threaded
from time import sleep

_id = 0


@Threaded.infinite("write_thd")
def write_id(writer_name):
    global _id

    _id += 1
    print(writer_name + ' increased id by one. id = ' + str(_id))

    sleep(1)


if __name__ == "__main__":
    write_id("Writer0", _id=0)
    sleep(3)

    Threaded.pause_thread("write_thd", _id=0)
    write_id("Writer1", _id=1)
    sleep(3)

    Threaded.resume_thread("write_thd", _id=0)
    sleep(3)

    Threaded.stop_thread("write_thd", _id=0)
    Threaded.stop_thread("write_thd", _id=1)

    Threaded.join_thread("write_thd", _id=0)
    Threaded.join_thread("write_thd", _id=1)
