

def read_data(file_path):
    mem = dict()
    with open(file_path) as fp:
        line = fp.readline().strip()
        mask = line.split(' = ')[1]
        for line in fp.readlines():
            if 'mask' not in line:
                s, val = line.split(" = ")
                s = int(s[s.find('[') + 1:s.find(']')])
                val = int(val.strip())
                mem[s] = '{0:036b}'.format(val)
            else:
                yield mask, mem
                mask = line.strip().split(' = ')[1]
        yield mask, mem


def apply_mask(mask: str, mem: dict):
    for k, v in mem.items():
        mem[k] = "".join([v[j] if mask[j] == 'X' else mask[j] for j in range(len(v))])


def compute_sum(mem: dict):
    return sum([int(x, 2) for x in mem.values()])


if __name__ == "__main__":

    for mask, mem in read_data('problem14_testdata.txt'):
        apply_mask(mask, mem)
        print(compute_sum(mem))
    print(compute_sum(mem))
