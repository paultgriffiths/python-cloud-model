import numpy as np

def kid_case1_updraft(t: float, w1: float, t1: float, t2: float) -> float:
    if t < t2:
        return w1 * np.sin(np.pi * t / t2)
    return 0.0
