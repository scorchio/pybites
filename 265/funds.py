IMPOSSIBLE = 'Mission impossible. No one can contribute.'


def max_fund(village):
    """Find a contiguous subarray with the largest sum."""
    current, best = (0, 0, 0), (0, 0, 0)
    in_block = False
    for idx, fund in enumerate(village):
        if fund > 0:  # need to start / continue
            if not in_block:
                current = (fund, idx, idx)
                in_block = True
            else:
                current = (current[0] + fund, current[1], idx)
        else:  # need to end
            if in_block:
                if current[0] > best[0]:
                    best = current
                current = (0, 0, 0)
                in_block = False
    if current != (0, 0, 0):
        best = current
    
    if best[0] < 1:  # leave early, no win here
        print(IMPOSSIBLE)
        return (0, 0, 0)

    # extend best - extend to start
    for idx in range(0, best[1]):
        new_sum = sum(village[idx:best[2] + 1])
        if new_sum > best[0]:
            best = (new_sum, idx, best[2])
    for idx in range(best[2], len(village)):
        new_sum = sum(village[best[1]:idx+1])
        if new_sum > best[0]:
            best = (new_sum, best[1], idx)

    return (best[0], best[1] + 1, best[2] + 1)
