from typing import List


def pascal(N: int) -> List[int]:
    if N == 0:
        return []
    if N == 1:
        return [1]

    l = [0]
    l.extend(pascal(N-1))
    l.append(0)

    result = []
    for i in range(len(l)-1):
        result.append(l[i] + l[i+1])
    return result