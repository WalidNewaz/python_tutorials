from multiprocessing import Process

def greet(name):
    print("Hello, %s" % name)

if __name__ == '__main__':
    p = Process(target=greet, args=('Walid',))
    p.start()
    p.join()
