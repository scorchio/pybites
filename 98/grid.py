DOWN, UP, LEFT, RIGHT = '⇓', '⇑', '⇐', '⇒'
START_VALUE = 1
DIRECTION_MOVES = {
    UP: (-1, 0),
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1)
}

def convert_grid_to_matrix(grid):
    i = 0
    matrix = []
    for line in grid.splitlines():
        if i % 2 == 1:
            values = line.replace(' - ', ',').replace('   ', ',').split(',')
            matrix.append([int(x) for x in values])
        i += 1
    return matrix


def find_starting_coord(matrix, starting_value=START_VALUE):
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == starting_value:
                return (i, j)


def find_next_in_matrix(matrix, current_coord):
    current_value = matrix[current_coord[0]][current_coord[1]]
    for direction, coord in DIRECTION_MOVES.items():
        new_row = current_coord[0] + coord[0]
        new_col = current_coord[1] + coord[1]
        if new_row >= 0 and new_row < len(matrix) and new_col >= 0 and new_col < len(matrix[0]):
            if matrix[new_row][new_col] == current_value + 1:
                return (new_row, new_col), direction
    assert False, "Could not find shit man!"


def print_sequence_route(grid):
    """Receive grid string, convert to 2D matrix of ints, find the
       START_VALUE coordinates and move through the numbers in order printing
       them.  Each time you turn append the grid with its corresponding symbol
       (DOWN / UP / LEFT / RIGHT). See the TESTS for more info."""
    matrix = convert_grid_to_matrix(grid)
    steps = []
    steps_row = []
    current_coord = find_starting_coord(matrix)
    current_direction = None
    last_item = len(matrix) * len(matrix)
    for step in range(1, last_item + 1):
        steps_row.append(str(step))
        if step != last_item:
            current_coord, direction = find_next_in_matrix(matrix, current_coord)
            if current_direction is None:
                current_direction = direction
            elif current_direction != direction:
                steps_row.append(direction)
                steps.append(steps_row)
                steps_row = []
                current_direction = direction
        else:
            steps.append(steps_row)
    for line in steps:
        print(' '.join(line))
