from multiprocessing import Process, Value
import time

def increment_batched(counter, n_increments):
    # all local work, no locking here
    local_count = n_increments
    # single critical section
    with counter.get_lock():                     # acquire/release per increment
        counter.value += local_count


if __name__ == '__main__':
    N_PROC = 4
    N = 1000
    counter = Value('i', 0)     # 'i' = 32-bit signed int
    procs = [Process(target=increment_batched, args=(counter, N)) for _ in range(N_PROC)]

    start = time.perf_counter()
    for p in procs:
        p.start()

    for p in procs:
        p.join()

    end = time.perf_counter()
    elapsed = end - start
    print(f"Counter value: {counter.value}")
    print(f"High-resolution elapsed time: {elapsed * 1000} milliseconds")