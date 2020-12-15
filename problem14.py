

def read_data(file_path):
    mem = dict()
    with open(file_path) as fp:
        mask = fp.readline().strip().split(' = ')[1]
        for line in fp.readlines():
            s, val = line.split(" = ")
            s = int(s[s.find('[') + 1:s.find(']')])
            val = int(val.strip())
            mem[s] = '{0:036b}'.format(val)
    return mask, mem


def apply_mask(mask: str, mem: dict):
    for k, v in mem.items():
        mem[k] = "".join([v[j] if mask[j] == 'X' else mask[j] for j in range(len(v))])


def compute_sum(mem: dict):
    return sum([int(x, 2) for x in mem.values()])


if __name__ == "__main__":

    mask, mem = read_data('problem14_data.txt')
    print(mask)
    print(mem)
    apply_mask(mask, mem)
    print(compute_sum(mem))
