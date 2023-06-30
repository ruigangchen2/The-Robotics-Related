from time import monotonic, sleep
from array import array
from statistics import mean
import psutil

# count = psutil.cpu_count()
# p = psutil.Process()
# cpu_lst = p.cpu_affinity() # [0, 1, 2, 3]
# p.cpu_affinity([7])

i = 0
data = array("f")
while i < 2000:
    t0 = monotonic()
    sleep(0.001)
    t1 = monotonic()
    data.append((t1 - t0 - 0.001) * 1000000)
    i += 1
print("AVG: %.2f us" % mean(data))
print("MAX: %.2f us" % max(data))
print("MIN: %.2f us" % min(data))
