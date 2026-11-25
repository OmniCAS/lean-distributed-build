"""Pick modules for the thread-scaling replay: the 25 heaviest on the critical path and the 5
heaviest elsewhere. Prints module names (heaviest first). Usage: replay_select.py TRACE"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sim.trace import Trace
t = Trace.load(sys.argv[1])
cp, path = t.critical_path(t.cost)
on = set(path)
a = sorted(path, key=lambda m: -t.cost[m])[:25]
b = [int(m) for m in np.argsort(-t.cost) if int(m) not in on][:5]
print(" ".join(t.mods[m] for m in a + b))
