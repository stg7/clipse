#!/usr/bin/env python3
import os
import sys
import numpy as np
import json
import timeit

if len(sys.argv) < 2:
    print("usage: ./avgtime.py <N> <CMD>")
    sys.exit(1)

number = int(sys.argv[1])
cmd = " ".join(sys.argv[2:])
measurements = []
for n in range(number):
    measurements.append(
        timeit.timeit(f"import os; os.system('{cmd}')", number=1)
    )

measurements = np.array(measurements)

res = {
    "cmd": cmd,
    "avgtime": measurements.mean(),
    "stdtime": measurements.std()
}

print(json.dumps(res))

