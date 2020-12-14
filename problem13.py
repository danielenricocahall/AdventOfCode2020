import math
from datetime import datetime
from functools import lru_cache
from math import ceil


def read_data(file_path):
    with open(file_path) as fp:
        return int(fp.readline()), [x for x in fp.readline().split(",")]


def get_bus_and_offset(time, buses):
    buses = [int(bus) for bus in buses if bus.isdigit()]
    closest_time = min([bus * ceil(time / bus) for bus in buses])
    bus_id = next(bus for bus in buses if bus * ceil(time / bus) == closest_time)
    return (closest_time - time) * bus_id


def next_step(invalids: list):
    max_ = max(invalids)
    invalids = [y for y in invalids if y > 1 and y != max_]
    next_possible_location = max_ + 1
    factors = tuple(sorted([x for x in invalids if next_possible_location % x == 0]))
    return compute_next_possible_location(next_possible_location, factors) if factors else next_possible_location


@lru_cache(None)
def compute_next_possible_location(next_possible_location: int, factors: tuple):
    i = 2
    while any(next_possible_location % x == 0 for x in factors):
        next_possible_location = i * next_possible_location + 1
        i += 1
    return next_possible_location


def compute_timestamp(buses):
    bus_to_offset = {int(bus): t_offset for t_offset, bus in enumerate(buses) if bus.isdigit()}
    t = 2
    while True:
        invalids = []
        for k, v in bus_to_offset.items():
            if not (t + v) % k == 0:
                invalids.append(v)
        if not invalids:
            break
        t += next_step(invalids)
    print(t)


if __name__ == "__main__":
    time, buses = read_data('problem13_testdata.txt')
    print(get_bus_and_offset(time, buses))
    start = datetime.now()
    compute_timestamp(buses)
    print(datetime.now() - start)
