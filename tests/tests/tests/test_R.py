def compute_R(dep, cond):
    if cond == 0:
        return 0
    return abs(dep) / abs(cond)

def test_R_positive():
    R = compute_R(2, 1)
    assert R >= 0
