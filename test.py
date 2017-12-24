import numpy as np
nums = range(0, 10)
a = [[num, num+1] for num in nums]
a.append([100, 100])
a = np.asarray(a).T
print(a)
