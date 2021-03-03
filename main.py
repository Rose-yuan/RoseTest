import _thread
import logging
import threading
from time import sleep, ctime

logging.basicConfig(level=logging.INFO)


def loop0(lock):
    logging.info("start loop0 at " + ctime())
    sleep(4)
    logging.info("end loop0 at " + ctime())
    lock.release()


def loop1(lock):
    logging.info("start loop1 at " + ctime())
    sleep(2)
    logging.info("end loop1 at " + ctime())
    lock.release()


loops = [4, 1]


def loop(nloop, nsec, lock):
    logging.info("start loop" + str(nloop) + " at " + ctime())
    sleep(nsec)
    logging.info("end loop" + str(nloop) + " at " + ctime())
    lock.release()  # 释放锁


def loop2(nloop, nsec):
    logging.info("start loop" + str(nloop) + " at " + ctime())
    sleep(nsec)
    logging.info("end loop" + str(nloop) + " at " + ctime())

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.func=func
        self.args=args
        self.name=name
    def run(self):  # 重写run方法
        self.func(*self.args)



# 单线程的写法
def main():
    logging.info("start all at " + ctime())
    loop0()
    loop1()  # 需要等loop0执行完后再执行
    logging.info("end all at " + ctime())


# 多线程的写法
def main1():
    logging.info("start all at " + ctime())
    _thread.start_new_thread(loop0, ())
    _thread.start_new_thread(loop1, ())
    sleep(6)  # 主线程加sleep是因为，_thread规定，当主线程结束时，所有子线程都会被kill掉
    logging.info("end all at " + ctime())


# 多线程加锁写法
def main2():
    logging.info("start all at " + ctime())
    locks = []  # 声明锁的列表
    nloops = range(len(loops))
    for i in nloops:
        lock = _thread.allocate_lock()  # 声名锁
        # sleep(2)
        lock.acquire()  # 加锁
        locks.append(lock)
        # _thread.start_new_thread(loop, (i, loops[i], locks[i]))  # 创建一个线程
    for i in nloops:
        _thread.start_new_thread(loop, (i, loops[i], locks[i]))  # 创建一个线程
    for i in nloops:
        while locks[i].locked(): pass  # 检查锁状态是否为已锁，是则进入死循环；否则退出主线程
    logging.info("end all at " + ctime())


# 多线程threading写法
def main3():
    logging.info("start all at " + ctime())
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=loop2, args=(i, loops[i]))
        threads.append(t)
    for i in nloops:
        # 放在单独的for循环，目的是让线程并发执行
        threads[i].start()  # 此时才开始执行loop2
    for i in nloops:
        threads[i].join()  # 校验线程是否结束，否，则进行阻塞
    logging.info("end all at " + ctime())

# 多线程面向对象写法(最推荐)
def main4():
    logging.info("start all at " + ctime())
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = MyThread(loop2, (i, loops[i]),loop.__name__)
        threads.append(t)
    for i in nloops:
        # 放在单独的for循环，目的是让线程并发执行
        threads[i].start()  # 此时才开始执行loop2
    for i in nloops:
        threads[i].join()  # 校验线程是否结束，否，则进行阻塞
    logging.info("end all at " + ctime())

if __name__ == '__main__':
    main4()
