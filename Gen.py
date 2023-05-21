import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk

def process_words(batch_size, lines, invalid_chars):
    results = []
    while len(results) < batch_size and not terminate_processing:
        words = random.sample(lines[:2000], 12)
        words = [word for word in words if not any(char in invalid_chars for char in word)]
        if len(words) == 12:
            results.append(words)
            print(' '.join(words))
    return results

def start_processing_thread():
    global terminate_processing
    terminate_processing = False
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    
    with open("words.txt", "r") as file:
        lines = [line.strip() for line in file]

    invalid_chars = {' ', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    random_words_file = "random_words.txt"

    num_threads = 100  # Number of worker threads
    batch_size = 1000  # Number of word sets to generate in each batch

    lock = threading.Lock()
    results_queue = []
    generated_count = 0

    while not terminate_processing:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(process_words, batch_size, lines, invalid_chars)]
            for future in as_completed(futures):
                results = future.result()
                with lock:
                    results_queue.extend(results)

        if len(results_queue) >= batch_size:
            with open(random_words_file, "a") as file:
                for words in results_queue[:batch_size]:
                    file.write(' '.join(words) + '\n')
                results_queue = results_queue[batch_size:]
                generated_count += batch_size
                generated_label.config(text=f"Word Sets Generated: {generated_count}")
                print(' '.join(words))

        # Set the termination condition based on your requirements

    print("Processing complete.")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def start_processing():
    global processing_thread
    processing_thread = threading.Thread(target=start_processing_thread)
    processing_thread.start()

def stop_processing():
    global terminate_processing
    terminate_processing = True

root = tk.Tk()
root.title("Word Processing")
root.geometry("200x100")

start_button = tk.Button(root, text="Start", command=start_processing)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_processing, state=tk.DISABLED)
stop_button.pack()

generated_label = tk.Label(root, text="Word Sets Generated: 0")
generated_label.pack()

root.mainloop()
