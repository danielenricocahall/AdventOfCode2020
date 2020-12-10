from typing import List


def find_two_sum(nums: List, value: int) -> tuple:
    nums.sort()
    l = 0
    r = len(nums) - 1
    while l < r:
        if nums[l] + nums[r] < value:
            l += 1
        elif nums[l] + nums[r] > value:
            r -= 1
        else:
            return nums[l], nums[r]
    return tuple()


def find_three_sum(nums: List, value: int) -> tuple:
    for num in nums:
        value -= num
        result = find_two_sum(nums, value)
        if result:
            return (num,) + result


if __name__ == "__main__":
    with open('problem1_data.txt') as fp:
        data = []
        for line in fp.readlines():
            data.append(int(line))
        x, y = find_two_sum(data, 2020)
        print(x * y)
        x, y, z = find_three_sum(data, 2020)
        print(x * y * z)
