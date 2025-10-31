from multiprocessing import Process, Value
import time

def increment(counter, n_increments):
    for _ in range(n_increments):
        with counter.get_lock():                     # acquire/release per increment
            counter.value += 1

if __name__ == '__main__':
    N_PROC = 4
    N = 1000000
    counter = Value('i', 0)     # 'i' = 32-bit signed int
    procs = [Process(target=increment, args=(counter, N)) for _ in range(N_PROC)]

    start = time.perf_counter()
    for p in procs:
        p.start()

    for p in procs:
        p.join()

    end = time.perf_counter()
    elapsed = end - start
    print(f"Counter value: {counter.value}")
    print(f"High-resolution elapsed time: {elapsed * 1000} milliseconds")
