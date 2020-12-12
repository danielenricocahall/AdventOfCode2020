import re


def read_data(file_path):
    with open(file_path) as fp:
        data = []
        for line in fp.readlines():
            line = line.strip()
            direction, spaces = re.match(r'([A-Z]{1})([0-9]+)', line).groups()
            data.append((direction, int(spaces)))
        return data


def update_position(current_pos, starting_direction, direction, spaces):
    rotations_dict = {'N': 'E',
                      'E': 'S',
                      'S': 'W',
                      'W': 'N'}
    if direction == 'F':
        starting_direction, current_pos = update_position(current_pos, starting_direction, starting_direction, spaces)
    elif direction == 'N':
        current_pos = (current_pos[0], current_pos[1] + spaces)
    elif direction == 'S':
        current_pos = (current_pos[0], current_pos[1] - spaces)
    elif direction == 'E':
        current_pos = (current_pos[0] + spaces, current_pos[1])
    elif direction == 'W':
        current_pos = (current_pos[0] - spaces, current_pos[1])
    elif direction == 'R':
        for theta in range(spaces // 90):
            starting_direction = rotations_dict[starting_direction]
    elif direction == 'L':
        reverse_rotations_dict = {v: k for k, v in rotations_dict.items()}
        for theta in range(spaces // 90):
            starting_direction = reverse_rotations_dict[starting_direction]
    return starting_direction, current_pos


def navigate(directions: list, starting_direction: str = 'E', starting_pos: tuple = (0, 0)):
    current_pos = starting_pos
    current_direction = starting_direction
    for direction, spaces in directions:
        current_direction, current_pos = update_position(current_pos, current_direction, direction, spaces)
    return current_direction, current_pos


def navigate_waypoint(directions: list, starting_waypoint: tuple = (10, 1),
                      starting_direction: str = 'E', starting_pos: tuple = (0, 0)):
    current_pos = starting_pos
    current_direction = starting_direction
    current_waypoint = starting_waypoint
    for direction, spaces in directions:
        current_direction, current_pos, current_waypoint = \
            update_position_waypoint(current_pos, current_direction, direction, spaces, current_waypoint)
    return current_direction, current_pos


def update_position_waypoint(current_pos, starting_direction, direction, spaces, waypoint):
    if direction == 'F':
        current_pos = (spaces * waypoint[0] + current_pos[0], spaces * waypoint[1] + current_pos[1])
    elif direction == 'N':
        waypoint = (waypoint[0], waypoint[1] + spaces)
    elif direction == 'S':
        waypoint = (waypoint[0], waypoint[1] - spaces)
    elif direction == 'E':
        waypoint = (waypoint[0] + spaces, waypoint[1])
    elif direction == 'W':
        waypoint = (waypoint[0] - spaces, waypoint[1])
    elif direction == 'R':
        for theta in range(spaces // 90):
            waypoint = (waypoint[1], -waypoint[0])
    elif direction == 'L':
        for theta in range(spaces // 90):
            waypoint = (-waypoint[1], waypoint[0])
    return starting_direction, current_pos, waypoint


def compute_distance(ending_pos: tuple, starting_pos: tuple = (0, 0)):
    return abs(ending_pos[0] - starting_pos[0]) + abs(ending_pos[1] - starting_pos[1])


if __name__ == "__main__":
    data = read_data('problem12_testdata.txt')
    ending_direction, ending_position = navigate_waypoint(data)
    print(compute_distance(ending_position))
