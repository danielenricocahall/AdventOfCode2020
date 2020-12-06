from functools import reduce


def read_data(file_path):
    count = 0
    results = []
    with open(file_path) as fp:
        for line in fp.readlines():
            line = line.strip()
            if line == '':
                reduced = reduce(lambda x, y: x & y, results)
                count += len(reduced)
                results = []
            else:
                results.append(set(line))
    reduced = reduce(lambda x, y: x & y, results)
    count += len(reduced)
    return count

count = read_data('problem6_data.txt')
print(count)
