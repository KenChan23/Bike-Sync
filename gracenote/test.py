import math

nums = [100, 200, -300, 300, -100]
tot = 0.0
logs = 0.0
prod = 1.0

for num in nums:
    tot += abs(num)

print tot

for num in nums:
    logs += math.log(1 + tot**num)
    prod *= 1 + tot**num

print tot, math.exp(logs)%tot, prod%tot

logs <= np
2**int(logs) in np digits
need logs accurate to log(1/2**np)?
