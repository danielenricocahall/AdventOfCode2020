

with open('problem2_data.txt') as fp:
    valid_counter = 0
    for line in fp.readlines():
        min_max, char, password = line.split(' ')
        min, max = min_max.split('-')
        char = char[:-1]
        min, max = int(min), int(max)
        if password[min - 1] == char and not password[max - 1] == char:
            valid_counter += 1
        if password[max - 1] == char and not password[min - 1] == char:
            valid_counter += 1
    print(valid_counter)

