from multiprocessing import Process, Manager

def add_value(shared_list):
    shared_list.append(42)

if __name__ == '__main__':
    with Manager() as manager:
        shared = manager.list()
        p = Process(target=add_value, args=(shared,))
        p.start()
        p.join()
        print(shared)