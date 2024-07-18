import multiprocessing
import time

def calculate_square_sum(start, end, output_queue):
    square_sum = 0
    for num in range(start, end):
        square_sum += num * num
    output_queue.put(square_sum)

def sum_of_squares_multiprocessing(limit, num_processes):
    output_queue = multiprocessing.Queue()

    chunk_size = limit // num_processes
    processes = []

    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i != num_processes - 1 else limit + 1
        p = multiprocessing.Process(target=calculate_square_sum, args=(start, end, output_queue))
        p.start()
        processes.append(p)

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Collect results from the queue
    total_sum = 0
    while not output_queue.empty():
        total_sum += output_queue.get()

    return total_sum

if __name__ == "__main__":
    start_time = time.time()

    limit = 90000000  # Range from 1 to 90,000,000
    num_processes = 4  # Number of processes to use

    total_sum = sum_of_squares_multiprocessing(limit, num_processes)
    print(f"Sum of squares from 1 to {limit}: {total_sum}")
    print("--- %s seconds ---" % (time.time() - start_time))
