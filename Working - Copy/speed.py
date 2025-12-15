
import time
from math import sqrt

startTime = time.time()

x = 1.0
y = 2.0
z = 3.0

for j in range(1,501):
  for i in range(1, 200001):
    r = sqrt(x*x+y*y+z*z)

endTime = time.time()
print( 'execution time = ', endTime - startTime, 'seconds.' )
