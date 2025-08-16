import threading
import time

def crawl(url):
    print(f"Visiting {url}...")
    time.sleep(2)  # Sleep for 2 seconds
    print(f"Finished visiting {url}.")


threads = []
links = [
    "https://www.google.com/",
    "https://www.youtube.com/",
    "https://www.mit.edu/"
]

if __name__ == "__main__":
    start = time.time()
    # Create the threads
    for link in links:
        thread = threading.Thread(target=crawl, args=(link,))
        threads.append(thread)

    # Start all the threads
    for thread in threads:
        thread.start()

    # Join all threads
    for thread in threads:
        thread.join()

    print(f"Time taken to visit {len(links)} links: {time.time() - start:.2f} seconds.")
