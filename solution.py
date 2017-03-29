from collections import Counter
assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    # Use this function to cross rows and cols
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal1 = [a[0]+a[1] for a in zip(rows, cols)]
diagonal2 = [a[0]+a[1] for a in zip(rows, cols[::-1])]
diag_units = [diagonal1, diagonal2]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    # Assign a value to given box
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    '''
    Use this function to eliminate values using naked twins strategy.
    Args : values(dict)
    Returns : values(dict)
    Algorithm :
        Find all boxes that have 2 values.
        If two boxes are in same unit and have same values, it is called 'naked twins'.
        You can eliminate that values in that unit.
    '''
    for unit in unitlist:
        len_two_values = Counter([values[box] for box in unit if len(values[box]) == 2])
        naked_Twins = [val for val, count in len_two_values.items() if count == 2]
        for naked_Twin in naked_Twins:
            digits = str.maketrans('', '', naked_Twin)
            for box in unit:
                if values[box] != naked_Twin:
                    assign_value(values, box, values[box].translate(digits))
    return values

def grid_values(grid):
    '''
    A function to convert the string representation of a puzzle into a dictionary form.
    Args : grid(String)
    Returns : dict(zip(boxes, chars))
    '''
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    '''
    Display the values as 2-D grid.
    Args : values(dict)
    Returns : None
    '''
    if values == False:
        pass
    else:
        width = 1+max(len(values[s]) for s in boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                          for c in cols))
            if r in 'CF': print(line)
        print

def eliminate(values):
    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    '''
    Finalize all values that are the only choice for a unit.
    
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    
    Args : values(dict)
    Returns : values(dict)
    '''
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    '''
    Use functions to reduce puzzle.
    '''
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # If before values equals after values, return values.
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    '''
    Args : values(dict)
    '''
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    '''
    Use grid_values function and search function to solve sudoku problems.
    '''
    values = grid_values(grid)
    result = search(values)
    return result

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')