from collections import defaultdict
from datetime import datetime


def read_data(file_path):
    data = []
    with open(file_path) as fp:
        for line in fp.readlines():
            data.append(int(line))
    return data


def compute_joltage_differences(data: list):
    data.append(0)
    data.append(max(data) + 3)
    data = sorted(data)
    adjacent_diff = [y - x for x, y in zip(data, data[1:])]
    return adjacent_diff


def multiply_joltage_diffs(data: list):
    from collections import Counter
    counter = Counter(data)
    return counter[1] * counter[3]


def cache(func):
    cached = dict()

    def inner(data: list, n: int):
        data = tuple(data)
        if data not in cached:
            cached[data] = defaultdict()
        if n not in cached[data]:
            cached[data][n] = func(data, n)
        return cached[data][n]
    inner.cache = cached
    return inner


def find_combinations(data):
    data = sorted(data)

    @cache
    def helper(data: list, n: int):
        if n + 1 > len(data) - 1:
            return 1
        elif n + 4 < len(data) - 1 and data[n + 4] - data[n] == 4:
            copy = [*data]
            del copy[n+1]
            copy2 = [*data]
            del copy2[n+2]
            copy7 = [*data]
            del copy7[n+3]
            copy3 = [*data]
            del copy3[n+1:n+3]
            copy5 = [*data]
            del copy5[n+1:n+4:2]
            copy6 = [*data]
            del copy6[n+2:n+4]
            # 7
            return helper(copy, n) + \
                   helper(copy2, n) + \
                   helper(copy3, n) + \
                   helper(copy5, n) + \
                   helper(copy6, n) + \
                   helper(copy7, n) + \
                   helper(data, n + 1)
        elif n + 3 < len(data) - 1 and data[n + 3] - data[n] == 3:
            copy = [*data]
            del copy[n+1]
            copy2 = [*data]
            del copy2[n+2]
            copy3 = [*data]
            del copy3[n+1:n+3]
            # 4
            return helper(copy, n) + helper(copy2, n) + helper(copy3, n) + helper(data, n + 1)
        elif n + 2 < len(data) - 1 and data[n + 2] - data[n] == 2:
            copy = [*data]
            del copy[n+1]
            # 2
            return helper(copy, n) + helper(data, n + 1)
        else:
            return helper(data, n + 1)

    helper(data, 0)
    return len(helper.cache.keys())


if __name__ == "__main__":
    # problem 1
    data = read_data('problem10_testdata.txt')
    adjacent_diff = compute_joltage_differences(data)
    print(multiply_joltage_diffs(adjacent_diff))
    now = datetime.now()
    print(find_combinations(data))
    print(datetime.now() - now)
