from datetime import datetime
from functools import lru_cache
from pprint import pprint


def read_data(file_path):
    seats = []
    with open(file_path) as fp:
        for line in fp.readlines():
            seats.append([x for x in line.strip()])
    return seats


def get_four_neighborhood(row: int, col: int, seats: list):
    neighborhood = []
    if row > 0:
        neighborhood.append(seats[row - 1][col])
    if col > 0:
        neighborhood.append(seats[row][col - 1])
    if row < len(seats) - 1:
        neighborhood.append(seats[row + 1][col])
    if col < len(seats[row]) - 1:
        neighborhood.append(seats[row][col + 1])
    return neighborhood


def get_diagonal_neighborhood(row: int, col: int, seats: list):
    neighborhood = get_top_diagonal(row, col, seats) + get_bottom_diagonal(row, col, seats)
    return neighborhood


def get_adjacent_neighborhood(row: int, col: int, seats: list):
    return get_four_neighborhood(row, col, seats) + get_diagonal_neighborhood(row, col, seats)


def get_top_diagonal(row: int, col: int, seats: list):
    neighborhood = []
    if row > 0:
        if col > 0:
            neighborhood.append(seats[row - 1][col - 1])
        if len(seats[row]) - 1 > col:
            neighborhood.append(seats[row - 1][col + 1])
    return neighborhood


def get_bottom_diagonal(row: int, col: int, seats: list):
    neighborhood = []
    if row < len(seats) - 1:
        if col > 0:
            neighborhood.append(seats[row + 1][col - 1])
        if col < len(seats[row]) - 1:
            neighborhood.append(seats[row + 1][col + 1])
    return neighborhood


def cache(func):
    cached = dict()
    def inner(row: int, col: int, seats: list):
        if (row, col) in cached:
            return [seats[_row][_col] for _row, _col in cached[(row, col)]]
        else:
            coords, neighborhood = func(row, col, seats)
            cached[(row, col)] = [(_row, _col) for _row, _col in coords if _row is not None and _col is not None]
            return neighborhood
    return inner


@cache
def get_full_neighborhood(row: int, col: int, seats: list):
    neighborhood = []
    coords = []
    # get left seats
    left_coords, left_value = next((((row, _col),
                                     seats[row][_col]) for _col in range(col - 1, -1, -1) if seats[row][_col] in ['L', '#']), ((None, None), []))
    if left_value:
        neighborhood.append(left_value)
        coords.append(left_coords)
    # get right
    right_coords, right_value = next((((row, _col), seats[row][_col]) for _col in range(col+1, len(seats[row])) if seats[row][_col] in ['L', '#']), ((None, None), []))
    if right_value:
        neighborhood.append(right_value)
        coords.append(right_coords)

    # get above seats
    above_coords, above_value = next((((_row, col), seats[_row][col]) for _row in range(row + 1, len(seats)) if seats[_row][col] in ['L', '#']), ((None, None), []))
    # get below seats
    if above_value:
        neighborhood.append(above_value)
        coords.append(above_coords)
    below_coords, below_value = next((((_row, col), seats[_row][col]) for _row in range(row - 1, -1, -1) if seats[_row][col] in ['L', '#']), ((None, None), []))
    if below_value:
        neighborhood.append(below_value)
        coords.append(below_coords)

    left_row, left_col, right_row, right_col, top_diag = get_all_top_diagonal(row, col, seats)
    coords.extend([(left_row, left_col), (right_row, right_col)])
    neighborhood.extend(top_diag)
    left_row, left_col, right_row, right_col, bottom_diag = get_all_bottom_diagonal(row, col, seats)
    neighborhood.extend(bottom_diag)
    coords.extend([(left_row, left_col), (right_row, right_col)])
    return coords, neighborhood


def get_all_top_diagonal(row: int, col: int, seats: list):
    neighborhood = []
    left_col = col - 1
    right_col = col + 1
    found_left = False
    found_right = False
    left_row = None
    right_row = None
    row -= 1
    while row >= 0:
        if left_col >= 0 and not found_left:
            if seats[row][left_col] in ['L', '#']:
                neighborhood.append(seats[row][left_col])
                found_left = True
                left_row = row
            else:
                left_col -= 1
        if right_col < len(seats[row]) and not found_right:
            if seats[row][right_col] in ['L', '#']:
                neighborhood.append(seats[row][right_col])
                found_right = True
                right_row = row
            else:
                right_col += 1
        if found_left and found_right:
            break
        row -= 1
    return left_row, left_col, right_row, right_col, neighborhood

def get_all_bottom_diagonal(row: int, col: int, seats: list):
    neighborhood = []
    left_col = col - 1
    right_col = col + 1
    found_left = False
    found_right = False
    left_row = None
    right_row = None
    row += 1
    while row < len(seats):
        if left_col >= 0 and not found_left:
            if seats[row][left_col] in ['L', '#']:
                neighborhood.append(seats[row][left_col])
                found_left = True
                left_row = row
            else:
                left_col -= 1
        if right_col < len(seats[row]) and not found_right:
            if seats[row][right_col] in ['L', '#']:
                neighborhood.append(seats[row][right_col])
                found_right = True
                right_row = row
            else:
                right_col += 1
        if found_left and found_right:
            break
        row += 1
    return left_row, left_col, right_row, right_col, neighborhood

def apply_seats_rules(seats: list, get_neighborhood: callable = get_adjacent_neighborhood, tolerance: int = 4):
    seats_copy = [seat.copy() for seat in seats]
    for row in range(len(seats)):
        for column in range(len(seats[row])):
            if seats[row][column] == 'L':
                neighborhood = get_neighborhood(row, column, seats)
                if not any(neighbor for neighbor in neighborhood if neighbor == '#'):
                    seats_copy[row][column] = '#'
            elif seats[row][column] == '#':
                neighborhood = get_neighborhood(row, column, seats)
                if sum(1 for neighbor in neighborhood if neighbor == '#') >= tolerance:
                    seats_copy[row][column] = 'L'
    return seats_copy


def iterate_until_stable(seats: list, get_neighborhood: callable, tolerance: int):
    prev_seats = seats
    curr_seats = apply_seats_rules(seats, get_neighborhood, tolerance)
    counter = 1
    while prev_seats != curr_seats:
        prev_seats = curr_seats
        curr_seats = apply_seats_rules(curr_seats, get_neighborhood, tolerance)
        counter += 1
    return curr_seats


def count_occupied(seats):
    counter = 0
    for row in seats:
        counter += sum(1 for seat in row if seat == '#')
    return counter


if __name__ == "__main__":
    seats = read_data('problem11_data.txt')
    now = datetime.now()
    final_seating_arrangement = iterate_until_stable(seats, get_full_neighborhood, 5)
    print(datetime.now() - now)
    print(count_occupied(final_seating_arrangement))
