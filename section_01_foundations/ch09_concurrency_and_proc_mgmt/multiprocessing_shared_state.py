from multiprocessing import Process, Value

def increment(counter):
    for _ in range(1000):
        counter.value += 1

if __name__ == '__main__':
    counter = Value('i', 0)
    processes = [Process(target=increment, args=(counter,)) for _ in range(4)]

    # Start the processes
    for p in processes:
        p.start()

    # Join the processes
    for p in processes:
        p.join()

    print(f"Counter value: {counter.value}")