from multiprocessing import Process, Value, Lock
import time

def increment(counter, n_increments, lock):
    for _ in range(n_increments):
        with lock:                     # use shared lock
            counter.value += 1

if __name__ == '__main__':
    N_PROC = 4
    N = 100000
    lock = Lock()
    counter = Value('i', 0, lock=False) # no per-Value lock; we use our own
    procs = [Process(target=increment, args=(counter, N, lock)) for _ in range(N_PROC)]

    start = time.perf_counter()
    for p in procs:
        p.start()

    for p in procs:
        p.join()

    end = time.perf_counter()
    elapsed = end - start
    print(f"Counter value: {counter.value}")
    print(f"High-resolution elapsed time: {elapsed * 1000} milliseconds")