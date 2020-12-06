def read_data(file):
    data = []
    with open(file) as fp:
        for line in fp.readlines():
            data.append(line.strip())
    return data


def tree_counter(data, right=0, down=1):
    column = 0
    tree_count = 0
    num_columns = len(data[0])
    for row in range(0, len(data), down):
        position = data[row][column]
        if position == '#':
            tree_count += 1
        column = (column + right) % num_columns
    return tree_count


foo = tree_counter(read_data('problem3_data.txt'), 1, 1) * \
      tree_counter(read_data('problem3_data.txt'), 3, 1) * \
      tree_counter(read_data('problem3_data.txt'), 5, 1) * \
      tree_counter(read_data('problem3_data.txt'), 7, 1) \
      * tree_counter(read_data('problem3_data.txt'), 1, 2)

print(foo)
