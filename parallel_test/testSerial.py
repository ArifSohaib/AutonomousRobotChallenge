import numpy as np
import time

nums = np.random.randint(0,400,10000).tolist()
start = time.time()
more = [num>50 for num in nums]
end = time.time()
print(len(more))
print("calculated in {}".format(end-start))
