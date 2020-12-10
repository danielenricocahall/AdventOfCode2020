from problem1 import find_two_sum


def read_data(file_path):
    results = []
    with open(file_path) as fp:
        for line in fp.readlines():
            results.append(int(line))
    return results


def examine_nums(nums: list, preamble: int):
    for i in range(preamble, len(nums) - 1):
        window = nums[i - preamble: i]
        current_value = nums[i]
        result = find_two_sum(window, current_value)
        if not result:
            return current_value


def find_contiguous_list(nums: list, value: int):
    foo = []
    found = False
    for i in range(len(nums)):
        agg = nums[i]
        foo = [nums[i]]
        for j in range(i + 1, len(nums)):
            agg += nums[j]
            foo.append(nums[j])
            if agg == value:
                found = True
                break
        if found:
            break
    return foo


def find_encryption_weakness(nums: list):
    nums.sort()
    return nums[0] + nums[-1]


data = read_data('problem9_data.txt')
result = examine_nums(data, 25)
contiguous_list = find_contiguous_list(data, result)
print(find_encryption_weakness(contiguous_list))
