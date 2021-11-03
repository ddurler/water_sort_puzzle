import time
import queue
import collections

N = 1_000_0000


def time_it(f):
    def inner():
        time_start = time.time()
        f()
        print(f"Execution: {time.time() - time_start:.03f}")

    return inner


@time_it
def test_list():
    print("test_list")
    ll = []
    for i in range(N):
        ll.append(i)


@time_it
def test_queue():
    print("test_queue")
    qq = queue.SimpleQueue()
    for i in range(N):
        qq.put(i)


@time_it
def test_deque():
    print("test_deque")
    qq = collections.deque()
    for i in range(N):
        qq.append(i)


test_list()
test_queue()
test_deque()
