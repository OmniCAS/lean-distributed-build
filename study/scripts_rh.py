"""closure sizes (bitsets), shared helper."""
import numpy as np


def closure_sizes(t):
    reach = [0] * t.n
    for m in t.order():
        m = int(m)
        acc = 0
        for u in t.imports[m]:
            acc |= reach[u] | (1 << u)
        reach[m] = acc
    return np.array([r.bit_count() for r in reach], dtype=np.float64)
