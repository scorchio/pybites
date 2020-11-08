from typing import List

def _split_into_frames(frames_str: str) -> List[str]:
    frames = []
    frames_without_space = frames_str.replace(' ', '')
    intra_frame_count = 0
    frame_scores = []    
    for score_idx, score in enumerate(frames_without_space):
        intra_frame_count += 1

        is_frame_finished = (
            score_idx == len(frames_without_space)-1 or  # we're at the last roll
            len(frames) < 9 and 
            (
                score == '/' or  # it's a spare
                score == 'X'  or  # strike ends frame
                intra_frame_count == 2  # no strike, no spare, but end of frame
            )
        )

        if is_frame_finished:
            frame_scores.append(score)
            frames.append(frame_scores)
            intra_frame_count = 0
            frame_scores = []
        else:
            frame_scores.append(score)
    return frames


def _char_to_score(char: str) -> int:
    if char in ['X', '/']: return 10
    if char == '-': return 0
    return int(char)


def _sum_frame(frame: List[str]) -> int:   
    frame_sum = 0
    for idx, score in enumerate(frame):
        if frame[idx] in ['/', 'X'] or (idx+1 < len(frame) and frame[idx+1] != '/') or idx == len(frame)-1:
            frame_sum += _char_to_score(score)
    return frame_sum
  

def _calculate_frame_score(frames: List[str], frame_idx: int) -> int:
    current_frame = frames[frame_idx]

    if 'X' not in current_frame and '/' not in current_frame:
        sum_points = _sum_frame(current_frame)
        return sum_points

    if frame_idx == len(frames)-1:  # final frame
        sum_points = _sum_frame(current_frame)
        return sum_points

    if '/' in current_frame:
        spare_sum = 10 + _char_to_score(frames[frame_idx + 1][0])
        return spare_sum

    if 'X' in current_frame:
        score_from_first_next = _char_to_score(frames[frame_idx + 1][0])
        if len(frames[frame_idx + 1]) > 1:
            if frames[frame_idx + 1][1] == '/':
                # first follow-up hit a few pins, after that, a spare - we need to reset the score for the first
                score_from_first_next = 0
            score_from_second_next = _char_to_score(frames[frame_idx + 1][1])
        else:
            score_from_second_next = _char_to_score(frames[frame_idx + 2][0])
        strike_sum = 10 + score_from_first_next + score_from_second_next
        return strike_sum


def calculate_score(frames: str) -> int:
    """Calculates a total 10-pin bowling score from a string of frame data."""
    
    """
    X: 10 + a következő 2 roll
    /: 10 + a következő roll
    második gurítás spare úgy van számolva, hogy a következő frame elsője van mellé, ilyenkor az első gurítás tökmindegy:
    2/ 2 -> 14
    4/ 2 -> 14
    """
    frames = _split_into_frames(frames)
    score = 0
    for frame_idx, _ in enumerate(frames):
        score += _calculate_frame_score(frames, frame_idx)
    return score
