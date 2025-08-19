# This program simulates file processing using concurrency.
# At the end of the simulation it compares the performance
# of the various concurrency strategies.
###########################################################

import threading
import time

def process_seq(name):
    print(f"Processing {name}...")
    with open(name, 'r') as f:
        line = f.readline()
        print(line)
        time.sleep(2)  # simulates file processing
    print(f"Done processing {name}")

def process_thread(name):
    print(f"Processing {name}...")
    with open(name, 'r') as f:
        line = f.readline()
        print(line)
        time.sleep(2)
    print(f"Done processing {name}")

def main():
    files = [f"resources/file-{i}.txt" for i in range(1, 11)]
    # Sequential processing
    seq_start = time.perf_counter()
    for file in files:
        process_seq(file)
    seq_end = time.perf_counter()
    seq_dur = f"{(seq_end - seq_start):.2f} s"

    # Threaded processing
    thread_start = time.perf_counter()
    threads = []
    for file in files:
        thread = threading.Thread(target=process_thread, args=(file,))
        threads.append(thread)

    # Start all the threads
    for thread in threads:
        thread.start()

    # Join all threads
    for thread in threads:
        thread.join()

    thread_end = time.perf_counter()
    thread_dur = f"{(thread_end - thread_start):.2f} s"


    # Summary
    print("-----------------------------------------------------")
    print(f"| Strategy   | Duration   | # Files    | # Chars    |")
    print("-----------------------------------------------------")
    print(f"| Sequential | {seq_dur:<10} | --         | --         |")
    print(f"| Threaded   | {thread_dur:<10} | --         | --         |")
    print(f"| Sequential | --         | --         | --         |")
    print(f"| Sequential | --         | --         | --         |")
    print("-----------------------------------------------------")

if __name__ == '__main__':
    main()