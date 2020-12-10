from datetime import datetime


def load_data(file_path):
    data = []
    with open(file_path) as fp:
        for line in fp.readlines():
            foo = line.split()
            data.append(list([foo[0], int(foo[1]), False]))
    return data


# problem 1
def find_acc_value_at_infinite_loop(data):
    acc = 0
    i = 0
    infinite_loop = False
    while i < len(data):
        if data[i][2]:
            infinite_loop = True
            break
        data[i][2] = True
        if data[i][0] == 'acc':
            acc += data[i][1]
        elif data[i][0] == 'jmp':
            i += data[i][1]
            continue
        i += 1
    return acc, infinite_loop


# problem 2
def correct_corrupted_instruction_data(data):
    for i in range(len(data)):
        copy = [x.copy() for x in data]
        if copy[i][0] == 'jmp':
            copy[i][0] = 'nop'
        elif copy[i][0] == 'nop':
            copy[i][0] = 'jmp'
        elif copy[i][0] == 'acc':
            continue
        acc, result = find_acc_value_at_infinite_loop(copy)
        if not result:
            print(i)
            break
    return acc


print(find_acc_value_at_infinite_loop(load_data('problem8_data.txt'))[0])
time = datetime.now()
print(correct_corrupted_instruction_data(load_data('problem8_data.txt')))
print(datetime.now() - time)
