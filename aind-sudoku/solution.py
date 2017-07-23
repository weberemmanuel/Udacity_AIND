import sys, os, random,collections #, pygame
sys.path.append(os.path.join("objects"))

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

cols = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, cols)

# Setup some data structures that whill be used by the sudoku solver
row_units      = [cross(r, cols) for r in rows]
column_units   = [cross(rows, c) for c in cols]
square_units   = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# setup diagonal units for diagonal sudokus
diagonal_units = []
diagonal_units += [[rows[i]+cols[i] for i in range(len(cols))]]
diagonal_units += [[rows[i]+cols[len(cols)-i-1] for i in range(len(cols))]]

assignments = []

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    try:
        if values[box] == value:
            return values
    except KeyError:
        pass

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
    for unit in unitlist:
        # create a set of twins.
        # Isolate items that have a size of two and exactly and that are found twice
        unit_values = [values[unit[i]] for i in range(len(unit))]
        unit_doubles = set([item for item, count in collections.Counter(unit_values).items() if count == 2 and len(item) == 2])
        for twin in unit_doubles:
            # walk the cells in the unit and for the one that are not the twin, remove the twin values
            for cell in range(len(unit)):
                if values[unit[cell]] != twin:
                    val = values[unit[cell]]
                    #print('Before val to ' + str(unit[cell] + ' '+ str(val)))
                    val = val.replace(twin[0],'')
                    val = val.replace(twin[1],'')
                    assign_value(values,unit[cell],val);
                    #print('Updated val to ' + str(unit[cell] + ' '+ str(val)))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert(len(grid) == 9*9)
    nextElement = 0
    values = {}
    for r in row_units:
        for box in r:
            if grid[nextElement] == '.':
                entry = cols
            else:
                entry = grid[nextElement]
            assign_value(values,box,entry)
            nextElement+=1
    return values

def display(values):
    """
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

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for k in values:
        val = values[k]
        if len(val) == 1:
            for peer in peers[k]:
                assign_value(values,peer,values[peer].replace(val,''))
    return values;

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for n in '123456789':
            hit = 0
            cellhit = None
            for cell in unit:
                if n in values[cell]:
                    hit += 1
                    cellhit = cell
            if hit == 1:
                assign_value(values,cellhit,str(n))
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
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
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    newvalues = reduce_puzzle(values)
    if newvalues == False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    searchcell = None
    for i in range(2,9):
        for cell in newvalues:
            if len(newvalues[cell]) == i:
                searchcell = cell
                break
        if searchcell != None:
            break;

    if searchcell != None:
        # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        for i in newvalues[searchcell]:
            copyvalues = values.copy()
            copyvalues[searchcell] = copyvalues[searchcell].replace(i,'')
            result = search(copyvalues)
            if result != False:
                return result
        return False
    return newvalues

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    #display(solve('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..',diag=False))
    #display(solve('8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..',diag=False))
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #display(solve(diag_sudoku_grid))
    #display(solve('8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..',diag=False))
    sudoku_grid ='.8..794...........3..5..9........1..........2..........72......8.1.....7...4.7.1.'
    display(solve(sudoku_grid))
    #sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    #display(solve(sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
