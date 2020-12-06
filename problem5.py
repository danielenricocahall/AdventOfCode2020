row_range = [i for i in range(128)]
col_range = [i for i in range(8)]


def read_data(file_path):
    with open(file_path) as fp:
        for line in fp.readlines():
            yield line


def split_range(vals, chars, lower_range, upper_range):
    if chars == '':
        return vals[0]
    if chars[0] == lower_range:
        return split_range(vals[0:len(vals) // 2], chars[1:], lower_range, upper_range)
    if chars[0] == upper_range:
        return split_range(vals[len(vals) // 2:len(vals)], chars[1:], lower_range, upper_range)


def get_rows(file_path):
    return [split_range(row_range, chars.strip()[:-3], 'F', 'B') for chars in read_data(file_path)]


def get_columns(file_path):
    return [split_range(col_range, chars.strip()[-3:], 'L', 'R') for chars in read_data(file_path)]


rows = get_rows('problem5_data.txt')
cols = get_columns('problem5_data.txt')
ids = [8 * row + column for row, column in zip(rows, cols)]
ids = sorted(ids)
diff_ids = [y - x for x, y in zip(ids[0::], ids[1::])]
result = [x for x, y in zip(ids, diff_ids) if y > 1]
print([id for id in ids if id > result[0]])
print(diff_ids)
