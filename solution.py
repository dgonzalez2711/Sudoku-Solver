import math
import string

assignments = []

def cross(A, B):
    return ([s+t for s in A for t in B])

diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
board_size = int(math.sqrt(len(diag_sudoku_grid)))
rows = string.ascii_uppercase[:board_size]
cols = string.digits[1:(board_size+1)]
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [
  ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9'],
  ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Loop through each unit in the list
    for unit in unitlist:
      # Create a new naked_twin list for each unit
      naked_twin = []
      # Check every box in the unit
      for box in unit:
        #Check every box in the unit
        for twin in unit:
          # If the box has two values the same as any other unit but isn't the same unit, its a twin
          if (len(values[box]) == 2) and (values[box] == values[twin]) and twin != box:
            # Store the twin
            naked_twin.append(twin)
      # Make sure we found a twin before continueing
      if(naked_twin):
        # For each of the values in any twin...
        for number in values[naked_twin[0]]:
            # Check every box in the unit
            for box in unit:
                # Get the value for every box in the unit
                vals = values[box]
                # Check if the values of that box contain twin numbers
                if number in vals and box not in naked_twin:
                    # If they do, remove them from the box
                    assign_value(values, box, values[box].replace(number, ''))
    # Return the values after the twins have been removed
    return values

def grid_values(grid):
    """
    ----------------------------------------------------------------------
    This section was taken from the previous lesson "Applying AI to Sudoku"
    -----------------------------------------------------------------------
    Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def eliminate(values):
    """
    ----------------------------------------------------------------------
    This section was taken from the previous lesson "Applying AI to Sudoku"
    -----------------------------------------------------------------------
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    ----------------------------------------------------------------------
    This section was taken from the previous lesson "Applying AI to Sudoku"
    -----------------------------------------------------------------------
    Finalize all values that are the only choice for a unit.
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    ----------------------------------------------------------------------
    This section was taken from the previous lesson "Applying AI to Sudoku"
    -----------------------------------------------------------------------
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # ADDED NAKED TWINS
        values = naked_twins(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def display(values):
    """
    ----------------------------------------------------------------------
    This section was taken from the previous lesson "Applying AI to Sudoku"
    -----------------------------------------------------------------------
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def search(values):
    """
    ----------------------------------------------------------------------
    This section was taken from the previous lesson "Applying AI to Sudoku"
    -----------------------------------------------------------------------
    """ 
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)
    filled_board = search(values)
    return filled_board


if __name__ == '__main__':
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

