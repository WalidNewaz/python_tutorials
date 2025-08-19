# This program simulates file processing using concurrency.
# At the end of the simulation it compares the performance
# of the various concurrency strategies.
###########################################################

import threading
import time
import queue
from multiprocessing import Pool
import asyncio

q = queue.Queue()   # For thread sync

def process_seq(name):
    print(f"Processing {name}...")
    num_lines = 0
    num_chars = 0
    with open(name, 'r') as f:
        for line in f:
            processed_line = line.strip()
            if len(processed_line) > 0:
                num_lines += 1
                num_chars += len(processed_line)
        time.sleep(2)  # simulates file processing
    return num_lines, num_chars

def process_files_seq(files):
    start = time.perf_counter()
    total_lines = 0
    total_chars = 0
    for file in files:
        seq_lines, seq_chars = process_seq(file)
        total_lines += seq_lines
        total_chars += seq_chars

    dur = f"{(time.perf_counter() - start):.2f} s"
    return dur, total_lines, total_chars

def process_thread(name):
    print(f"Processing {name}...")
    num_lines = 0
    num_chars = 0
    with open(name, 'r') as f:
        for line in f:
            processed_line = line.strip()
            if len(processed_line) > 0:
                num_lines += 1
                num_chars += len(processed_line)
        time.sleep(2)  # simulates file processing
    q.put((num_lines, num_chars))

def process_files_threaded(files):
    start = time.perf_counter()
    threads = []
    total_lines = 0
    total_chars = 0
    for file in files:
        thread = threading.Thread(target=process_thread, args=(file,))
        threads.append(thread)

    # Start all the threads
    for thread in threads:
        thread.start()

    # Join all threads
    for thread in threads:
        thread.join()

    # Parse return values
    while q.qsize() > 0:
        num_lines, num_chars = q.get()
        total_lines += num_lines
        total_chars += num_chars

    dur = f"{(time.perf_counter() - start):.2f} s"
    return dur, total_lines, total_chars

def process_files_multiprocessing(files):
    start = time.perf_counter()
    total_lines = 0
    total_chars = 0
    with Pool(len(files)) as p:
        results = p.map(process_seq, files)

    for result in results:
        num_lines, num_chars = result
        total_lines += num_lines
        total_chars += num_chars

    end = time.perf_counter()
    dur = f"{(end - start):.2f} s"
    return dur, total_lines, total_chars

async def process_file_async(file):
    print(f"Processing {file}...")
    num_lines = 0
    num_chars = 0
    with open(file, 'r') as f:
        for line in f:
            processed_line = line.strip()
            if len(processed_line) > 0:
                num_lines += 1
                num_chars += len(processed_line)
        await asyncio.sleep(2)  # simulates file processing
    return num_lines, num_chars

async def process_files_async(files):
    start = time.perf_counter()
    results = []

    tasks = [asyncio.create_task(process_file_async(file)) for file in files]

    for task in tasks:
        results.append(await task)

    total_lines = sum(r[0] for r in results)
    total_chars = sum(r[1] for r in results)

    dur = f"{(time.perf_counter() - start):.2f} s"
    return dur, total_lines, total_chars

def main():
    files = [f"resources/file-{i}.txt" for i in range(1, 11)]
    # Sequential processing
    print("Starting sequential processing...")
    print( "----------------------------------------------------------")
    seq_dur, total_seq_lines, total_seq_chars = process_files_seq(files)

    # Threaded processing
    print("Starting concurrent thread processing...")
    print("----------------------------------------------------------")
    thread_dur, total_thread_lines, total_thread_chars = process_files_threaded(files)

    # Multiprocessing
    print("Starting concurrent multiprocessing...")
    print("----------------------------------------------------------")
    multi_dur, multi_lines, multi_chars = process_files_multiprocessing(files)

    # Asyncio
    print("Starting concurrent asynchronous processing...")
    print("----------------------------------------------------------")
    asyncio_dur, asyncio_lines, asyncio_chars = asyncio.run(process_files_async(files))

    # Summary
    print( "----------------------------------------------------------")
    print(f"| Strategy        | Duration   | # Lines    | # Chars    |")
    print( "----------------------------------------------------------")
    print(f"| Sequential      | {seq_dur:<10} | {total_seq_lines:<10} | {total_seq_chars:<10} |")
    print(f"| Threaded        | {thread_dur:<10} | {total_thread_lines:<10} | {total_thread_chars:<10} |")
    print(f"| Multiprocessing | {multi_dur:<10} | {multi_lines:<10} | {multi_chars:<10} |")
    print(f"| Asyncio         | {asyncio_dur:<10} | {asyncio_lines:<10} | {asyncio_chars:<10} |")
    print( "----------------------------------------------------------")

if __name__ == '__main__':
    main()