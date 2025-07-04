#!/usr/bin/env python3
"""
6.101 Lab:
Mice-sleeper
"""

# import typing  # optional import
# import pprint  # optional import
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game, all_keys=False):
    """
    Prints a human-readable version of a game (provided as a dictionary)

    By default uses only "board", "dimensions", "state", "visible" keys (used
    by doctests). Setting all_keys=True shows all game keys.
    """
    if all_keys:
        keys = sorted(game)
    else:
        keys = ("board", "dimensions", "state", "visible")
        # Use only default game keys. If you modify this you will need
        # to update the docstrings in other functions!

    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(nrows, ncolumns, mice):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mice (list): List of mouse locations as (row, column) tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2,4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    dimensions = (nrows, ncolumns)
    board = [[0 for _ in range(ncolumns)] for _ in range(nrows)]
    visible = [[False for _ in range(ncolumns)] for _ in range(nrows)]

    # Place mice
    for x, y in mice:
        board[x][y] = 'm'

    # Count neighboring mice
    for i in range(nrows):
        for j in range(ncolumns):
            if board[i][j] == 'm':
                continue
            mice_count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < nrows and 0 <= nj < ncolumns:
                        if board[ni][nj] == 'm':
                            mice_count += 1
            board[i][j] = mice_count

    return {
        "dimensions": dimensions,
        "board": board,
        "state": "ongoing",
        "visible": visible,
        "first_click": True
    } 


        


def reveal_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mice (including diagonally), then recursively reveal its eight
    neighbors.  Return an integer indicating how many new squares were revealed
    in total, including neighbors, and neighbors of neighbors, and so on.

    The state of the game should be changed to 'lost' when at least one mouse
    is visible on the board, 'won' when all safe squares (squares that do not
    contain a mouse) and no mice are visible, and 'ongoing' otherwise.

    If the game is not ongoing, or if the given square has already been
    revealed, reveal_2d should not reveal any squares.

    Parameters:
       game (dict): Game state
       row (int): Where to start revealing cells (row)
       col (int): Where to start revealing cells (col)

    Returns:
       int: the number of new squares revealed

    >>> game = new_game_2d(2, 4, [(0,0), (1, 0), (1, 1)])
    >>> reveal_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, True, True]
        [False, False, True, True]
    >>> reveal_2d(game, 0, 1)
    1
    >>> dump(game)
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2, 4)
    state: won
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = new_game_2d(2, 4, [(0,0), (1, 0), (1, 1)])  # restart game
    >>> reveal_2d(game, 0, 3)
    4
    >>> reveal_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2, 4)
    state: lost
    visible:
        [True, False, True, True]
        [False, False, True, True]
    """
    board = game["board"]
    dimensions = game["dimensions"]
    nrows, ncols = dimensions
    if game["state"] != "ongoing" or game["visible"][row][col] or (("bed" in game and game["bed"][row][col])):
        return 0
    
    visited = set()
    def helper(r, c):
        if "bed" in game and (0 <= r < nrows and 0 <= c < ncols) and game["bed"][r][c]:
            return 0
        if game["first_click"]:
            game["first_click"] = False
            neighbors = get_neighbors((r, c), game["dimensions"])
            neighbors.append((r, c))  # include the clicked cell itself
            for coord in neighbors:
                if get_cell(game["board"], coord) == "m":
                    relocate_mice(game, (r, c))
                    break
        if (r, c) in visited or not (0 <= r < nrows and 0 <= c < ncols):
            return 0
        visited.add((r,c))
        if game["visible"][r][c]:
            return 0
        if board[r][c] == "m":
            game["visible"][r][c] = True
            game["state"] = "lost"
            return 1
            
        game["visible"][r][c] = True
        count = 1
        if board[r][c] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    count += helper(r + dx, c+ dy)
        return count
    total_revealed = helper(row, col)

    if game["state"] == "ongoing":
        won = True
        for i in range(nrows):
            for j in range(ncols):
                if board[i][j] != "m" and not game["visible"][i][j]:
                    won = False
                    break
            if not won:
                break
        if won:
            game["state"] = "won"

    return total_revealed



def render_2d(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    'm' (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mice).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored and
    all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = new_game_2d(2, 4, [(0,0), (1, 0), (1, 1)])
    >>> render_2d(game, False)
    [['_', '_', '_', '_'], ['_', '_', '_', '_']]
    >>> render_2d(game, True)
    [['m', '3', '1', ' '], ['m', 'm', '1', ' ']]
    >>> reveal_2d(game, 0, 3)
    4
    >>> render_2d(game, False)
    [['_', '_', '1', ' '], ['_', '_', '1', ' ']]
    """
    nrow, ncol = game["dimensions"]
    board = [[0 for _ in range(ncol)] for _ in range(nrow)]
    if(all_visible == True):
        for i in range(nrow):
            for j in range(ncol):
                if(game["board"][i][j] == 0):
                    board[i][j] = " "
                else:
                    board[i][j] = str(game["board"][i][j])
    else:
        for i in range(game["dimensions"][0]):
            for j in range(game["dimensions"][1]):
                if(game["visible"][i][j] == False and 'bed' in game and game["bed"][i][j] == True):
                    board[i][j] = 'B'
                elif(game["visible"][i][j] == False):
                    board[i][j] = "_"
                else:
                    if(game["board"][i][j] == 0):
                        board[i][j] = ' '
                    else:
                        board[i][j] = str(game["board"][i][j])
    return board

def toggle_bed_2d(game, row, col):
    """
    Toggle a "bed" (flag) on the cell at (row, col).

    Beds mark suspected mouse locations and can only be placed or removed on unrevealed cells.
    They have no effect on win/loss conditions but prevent reveal actions when present.

    Returns:
        True if a bed was placed,
        False if a bed was removed,
        None if the cell was revealed or the game is no longer ongoing.
    """
    # Check if game is ongoing
    if game["state"] != "ongoing":
        return None

    # Ensure the bed grid exists
    if "bed" not in game:
        nrows, ncols = game["dimensions"]
        game["bed"] = [[False for _ in range(ncols)] for _ in range(nrows)]

    bed = game["bed"]
    visible = game["visible"]

    # Cannot toggle bed on a revealed cell
    if visible[row][col]:
        return None

    # Toggle bed state
    if not bed[row][col]:
        bed[row][col] = True
        return True
    else:
        bed[row][col] = False
        return False

        
    
    


# N-D IMPLEMENTATION
def create_board(dimensions, fill_value):
    """
    Recursively creates an N-dimensional board with the given fill_value.

    Parameters:
        dimensions (tuple): Dimensions of the board
        fill_value (any): Initial value for each cell

    Returns:
        A nested list representing the N-dimensional board
    """
    if len(dimensions) == 0:
        return fill_value
    return [create_board(dimensions[1:], fill_value) for _ in range(dimensions[0])]


def in_bounds(coord, dimensions):
    """
    Checks if a coordinate is within the board dimensions.

    Parameters:
        coord (list or tuple): N-dimensional coordinate
        dimensions (tuple): Size of each dimension

    Returns:
        True if coordinate is valid, False otherwise
    """
    return all(0 <= coord[i] < dimensions[i] for i in range(len(coord)))

def set_cell(board, coord, value):
    """
    Sets the value at the given coordinate in the nested board.

    Parameters:
        board (list): N-dimensional board
        coord (list or tuple): Coordinate to update
        value (any): New value to set
    """
    if len(coord) == 1:
        board[coord[0]] = value
    else:
        set_cell(board[coord[0]], coord[1:], value)
    
def get_cell(board, coord):
    """
    Retrieves the value at the given coordinate in the nested board.

    Parameters:
        board (list): N-dimensional board
        coord (list or tuple): Coordinate to retrieve

    Returns:
        Value stored at the coordinate
    """
    if len(coord) == 1:
        return board[coord[0]]
    else:
        return get_cell(board[coord[0]], coord[1:])

def get_neighbors(coord, dimensions):
    """
    Computes all valid neighboring coordinates of a given cell in N-dimensions.

    Parameters:
        coord (list or tuple): Center coordinate
        dimensions (tuple): Board dimensions

    Returns:
        List of neighboring coordinates (excluding out-of-bounds and self)
    """
    neighbors = []
    def backtrack(pos, idx):
        if idx == len(coord):
            if pos != coord and in_bounds(pos, dimensions):
                neighbors.append(pos)
            return
        for d in [-1,0,1]:
            backtrack(pos + [coord[idx] + d], idx + 1)
    backtrack([], 0)
    return neighbors        

def update_counts(board, dimensions):
    """
    Updates each non-mouse cell with the count of neighboring mice.

    Parameters:
        board (list): N-dimensional board with mice marked as 'm'
        dimensions (tuple): Board dimensions
    """
    def recurse(coord=[], depth=0):
        if depth == len(dimensions):
            if get_cell(board, coord) != 'm':
                count = 0
                for neighbor in get_neighbors(coord, dimensions):
                    if get_cell(board, neighbor) == 'm':
                        count += 1
                set_cell(board, coord, count)
            return
        for i in range(dimensions[depth]):
            recurse(coord + [i], depth + 1)

    recurse()
def new_game_nd(dimensions, mice):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       dimensions (tuple): Dimensions of the board
       mice (list): mouse locations as a list of tuples, each an
                    N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, 'm'], [3, 3], [1, 1], [0, 0]]
        [['m', 3], [3, 'm'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """

    board = create_board(dimensions, 0)
    visible = create_board(dimensions, False)

    for mouse in mice:
        set_cell(board, mouse, 'm')

    update_counts(board, dimensions)

    return {
        'dimensions': dimensions,
        'board': board,
        'state': 'ongoing',
        'visible': visible,
        "first_click" : True
    }
    
def game_won(game):
    """
    Checks whether the game has been won and updates the game state accordingly.

    A game is considered won if all non-mouse squares on the board have been revealed,
    and no mice are visible. If the condition is met, the game state's 'state' field 
    is updated to 'won'.

    Parameters:
        game (dict): The game state dictionary, containing:
                     - 'board': N-dimensional board (with 'm' for mice, ints elsewhere)
                     - 'visible': N-dimensional visibility board (True if cell is revealed)
                     - 'dimensions': tuple representing the size of the board
                     - 'state': current game state ('ongoing', 'won', 'lost')

    Returns:
        bool: True if the game is won, False otherwise.
    """
    if game["state"] != "ongoing":
        return False

    for coord in all_possible_coordinates(game["dimensions"]):
        if get_cell(game["board"], coord) != "m" and not get_cell(game["visible"], coord):
            return False

    return True

        

def all_possible_coordinates(dimensons):
    """
    Generates all possible coordinates for an N-dimensional grid.

    Each coordinate is represented as a list of integers, where the ith element
    is an index in the ith dimension. This function recursively constructs all
    combinations of valid indices from 0 up to (but not including) the size of
    each dimension.

    Parameters:
        dimensions (tuple): A tuple of integers representing the size of the grid
                            in each dimension (e.g., (2, 3) for a 2x3 grid)

    Returns:
        list of list of int: A list of all possible N-dimensional coordinates,
                             where each coordinate is a list of integers.

    Example:
        >>> all_possible_coordinates((2, 2))
        [[0, 0], [0, 1], [1, 0], [1, 1]]

        >>> all_possible_coordinates((3,))
        [[0], [1], [2]]
    """
    neighbors = []
    def backtrack(pos, idx):
        if idx == len(dimensons):
            neighbors.append(pos)
            return
        for d in range(dimensons[idx]):
            backtrack(pos + [d], idx + 1)
    backtrack([], 0)
    return neighbors

    
def reveal_nd(game, coordinates):
    """
    Recursively reveal square at coords and neighboring squares.

    Update the visible to reveal square at the given coordinates; then
    recursively reveal its neighbors, as long as coords does not contain and is
    not adjacent to a mouse.  Return a number indicating how many squares were
    revealed.  No action should be taken (and 0 should be returned) if the
    incoming state of the game is not 'ongoing', or if the given square has
    already been revealed.

    The updated state is 'lost' when at least one mouse is visible on the
    board, 'won' when all safe squares (squares that do not contain a mouse)
    and no mice are visible, and 'ongoing' otherwise.

    Parameters:
       coordinates (tuple): Where to start revealing squares

    Returns:
       int: number of squares revealed

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, 'm'], [3, 3], [1, 1], [0, 0]]
        [['m', 3], [3, 'm'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> reveal_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, 'm'], [3, 3], [1, 1], [0, 0]]
        [['m', 3], [3, 'm'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: lost
    visible:
        [[False, True], [False, False], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    """
    board = game["board"]
    dimensions = game["dimensions"]
    if (
    game["state"] != "ongoing"
    or get_cell(game["visible"], coordinates)
    or ("bed" in game and get_cell(game["bed"], coordinates))
):
        return 0
    
    visited = set()
    def helper(coordinates):
        if "bed" in game and get_cell(game["bed"], coordinates):
            return 0
        if game["first_click"]:
            game["first_click"] = False
            neighbors = get_neighbors(coordinates, game["dimensions"])
            neighbors.append(coordinates)  # include the clicked cell itself
            for coord in neighbors:
                if get_cell(game["board"], coord) == "m":
                    relocate_mice(game, coordinates)
                    break
        if (tuple(coordinates)) in visited or not (in_bounds(coordinates, game["dimensions"])):
            return 0
        visited.add(tuple(coordinates))
        if get_cell(game["visible"], coordinates):
            return 0
        if get_cell(game["board"], coordinates) == "m":
            set_cell(game["visible"],coordinates, True)
            game["state"] = "lost"
            return 1
        set_cell(game["visible"], coordinates, True)
        count = 1
        if get_cell(game["board"], coordinates) == 0:
            neighbors = get_neighbors(coordinates, game["dimensions"])
            for i in neighbors:
                if (i == coordinates):
                    continue
                count += helper(i)
        return count
    total_revealed = helper(coordinates)

    if(game_won(game)):
        game["state"] = "won"

    return total_revealed



def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), 'm'
    (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring mice).
    The game['visible'] array indicates which squares should be visible.  If
    all_visible is True (the default is False), the game['visible'] array is
    ignored and all cells are shown.

    Parameters:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', 'm'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['m', '3'], ['3', 'm'], ['1', '1'], [' ', ' ']]]
    """
    board = create_board(game["dimensions"], 0)
    if(all_visible == True):
        for i in all_possible_coordinates(game["dimensions"]):
            if(get_cell(game["board"], i) == 0):
                set_cell(board, i, " ")
            else:
                set_cell(board, i, str(get_cell(game["board"], i)))
    else:
        for i in all_possible_coordinates(game["dimensions"]):
            if(get_cell(game["visible"], i) == False and "bed" in game and get_cell(game["bed"], i)):
                set_cell(board, i, "B") 
            elif(get_cell(game["visible"], i) == False):
                set_cell(board, i, "_")  
            else:
                if(get_cell(game["board"], i) == 0):
                    set_cell(board, i, " ")
                else:
                    set_cell(board, i, str(get_cell(game["board"], i)))
    return board

def relocate_mice(game, clicked_coord):
    """
    Moves mice away from the clicked cell and its neighbors, and updates board counts.
    Only called on the first reveal.
    """
    board = game["board"]
    dims = game["dimensions"]
    neighbors = get_neighbors(clicked_coord, dims)
    mice_to_move = []
    for coord in neighbors:
        if get_cell(board, coord) == "m":
            mice_to_move.append(coord)
            set_cell(board, coord, 0)
    update_counts(board, dims)

    rand_gen = random_coordinates(dims)
    placed = 0
    while(placed < len(mice_to_move)):
        d = next(rand_gen)
        if d == clicked_coord or list(d) in neighbors or get_cell(board, d) == "m":
            continue
        set_cell(board, d , "m")
        placed += 1

    update_counts(board, dims)

def toggle_bed_nd(game, coordinates):
    """
    Toggle a "bed" (flag) on the cell at the given N-dimensional coordinates.

    Beds can only be toggled on hidden (unrevealed) cells in an ongoing game.
    Returns:
        True if a bed was placed,
        False if a bed was removed,
        None if the cell is already revealed or the game is not ongoing.
    """
    if game["state"] != "ongoing":
        return None
    
    if "bed" not in game:
        dims = game["dimensions"]
        game["bed"] = create_board(dims, False)
    if (get_cell(game["visible"], coordinates)):
        return None
    current_bed = get_cell(game["bed"], coordinates)
    if not current_bed:
        set_cell(game["bed"], coordinates, True)
        return True
    else:
        set_cell(game["bed"], coordinates, False)
        return False
    

def random_coordinates(dimensions):
    """
    Given a tuple representing the dimensions of a game board, return an
    infinite generator that yields pseudo-random coordinates within the board.
    For a given tuple of dimensions, the output sequence will always be the
    same.
    """

    def prng(state):
        # see https://en.wikipedia.org/wiki/Lehmer_random_number_generator
        while True:
            yield (state := state * 48271 % 0x7FFFFFFF) / 0x7FFFFFFF

    prng_gen = prng(sum(dimensions) + 61016101)
    for _ in zip(range(1), prng_gen):
        pass
    while True:
        yield tuple(int(dim * val) for val, dim in zip(prng_gen, dimensions))


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so,
    # comment out the above line, and uncomment the below line of code.  This
    # may be useful as you write/debug individual doctests or functions.  Also,
    # the verbose flag can be set to True to see all test results, including
    # those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
