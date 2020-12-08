import re
from collections import Counter, defaultdict


def read_data(file_path):
    bags = {}
    with open(file_path) as fp:
        for line in fp.readlines():
            foo = re.sub(r'\bcontain\b\s+', "", line.strip())
            bag = " ".join(foo.split()[:2])
            inner = re.findall(f'\d+ [a-z ]+', foo)
            inner = [x.replace('bags', '').replace('bag', '').strip() for x in inner]
            bags[bag] = inner
    return bags


def reformat(bag):
    if len(bag.split()) == 3:
        number, bag = bag.split(" ", 1)
        number = int(number)
    else:
        number, bag = 1, bag

    return number, bag


def traverse(bags, bag, results):
    for inner_bag in bags[bag]:
        _, inner_bag = reformat(inner_bag)
        results[bag] = results[bag].union({inner_bag})
        results[bag] = results[bag].union(traverse(bags, inner_bag, results))
    return results[bag]


# problem 1
def count_bags_which_contain_gold_bags(bags):
    results = defaultdict(lambda: set())
    for bag in bags:
        traverse(bags, bag, results)
    counter = 0
    print(results)
    for k, v in results.items():
        if 'shiny gold' in v:
            counter += 1
            print(k)
    print(counter)


# problem 2
def count_individual_bags(bags):
    bags_contained_in_shiny_gold = bags.pop('shiny gold')
    counter = 0
    for bag in bags_contained_in_shiny_gold:
        counter += traverse2(bags, bag)
    print(counter)


def traverse2(bags, bag):
    number, bag = reformat(bag)
    if len(bags[bag]) == 0:
        return number
    else:
        return number + sum(number * [traverse2(bags, inner_bag) for inner_bag in bags[bag]])


bags = read_data('problem7_data.txt')
count_bags_which_contain_gold_bags(bags)
count_individual_bags(bags)