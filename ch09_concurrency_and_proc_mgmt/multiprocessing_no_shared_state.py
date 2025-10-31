from multiprocessing import Process, Queue, cpu_count
import time

def increment(n, out_q):
    # do the heavy work locally
    local = 0
    for _ in range(n):
        local = local + 1
    out_q.put(local)

if __name__ == '__main__':
    N_PROC = 4
    N = 1000000000
    queue = Queue()
    procs = [Process(target=increment, args=(N, queue)) for _ in range(N_PROC)]

    start = time.perf_counter()
    for p in procs:
        p.start()

    for p in procs:
        p.join()

    value = sum(queue.get() for _ in range(N_PROC))
    end = time.perf_counter()
    elapsed = end - start
    print(f"Counter value: {value}")
    print(f"High-resolution elapsed time: {elapsed * 1000} milliseconds")

