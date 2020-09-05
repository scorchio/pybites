def binary_search(sequence, target):
    def _recurse(enumerated_seq, target):
        if len(enumerated_seq) == 1:
            return enumerated_seq[0][0] if enumerated_seq[0][1] == target else None       
        i = len(enumerated_seq) // 2
        if enumerated_seq[i][1] > target:
            return _recurse(enumerated_seq[0:i], target)
        elif enumerated_seq[0][1] == target:
            return enumerated_seq[0][0]
        else:
            return _recurse(enumerated_seq[i:], target)

    
    enumerated_seq = list(enumerate(sequence))
    return _recurse(enumerated_seq, target)
