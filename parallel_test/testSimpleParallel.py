import multiprocessing
import numpy as np 
import random 

def split_list(lst,workers):
    list_ids = []
    for i in np.array_split(lst, workers):
        list_ids.append(i)
    return list_ids

def perform_check(sublist):
    count = 0
    for i in sublist:
        if i > 50:
            count += 1
    print("count: {}".format(count))
    return count

def get_count(lst, poolsize):
    """
    A function to initialize the pool of workers and call the wraper function perform_check 
    Args:
        lst: list of sublists
        poolsize: 
    """
    pool = multiprocessing.Pool(poolsize)
    s = pool.map(perform_check,lst)
    print("Active children count: {}".format(len(multiprocessing.active_children())))
    pool.close()
    pool.join()
    return "done"

def main():
    #get number of workers, each core of cpu is multithreaded so total logical number is cpu_count * 2
    NUM_WORKERS = multiprocessing.cpu_count() * 2
    #define a list of random numbers 
    nums = np.random.randint(0,400,360).tolist()
    list_ids = split_list(nums, NUM_WORKERS)
    count = 0
    count += get_count(list_ids,NUM_WORKERS)
    print("total: {}".format(count))
if __name__ == "__main__":
    main()
