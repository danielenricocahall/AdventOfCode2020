def read_passenger_data(file_path):
    with open(file_path) as fp:
        result = []
        for line in fp.readlines():
            line = line.strip()
            if line == '':
                yield transform_data(result)
                result = []
            else:
                result.append(line)
        yield transform_data(result)


def transform_data(record):
    transformed_result = {}
    for line in record:
        transformed_result.update(dict([foo.split(':') for foo in line.split()]))
    return transformed_result


def validate_data(record):
    def validate_years(record):
        record['byr'] = int(record['byr'])
        record['iyr'] = int(record['iyr'])
        record['eyr'] = int(record['eyr'])
        return (1920 <= record['byr'] <= 2002) and \
               (2010 <= record['iyr'] <= 2020) and \
               (2020 <= record['eyr'] <= 2030)

    def validate_height(record):
        if record['hgt'].endswith('cm'):
            return 150 <= int(record['hgt'][:-2]) <= 193
        if record['hgt'].endswith('in'):
            return 59 <= int(record['hgt'][:-2]) <= 76

    def validate_eyecolor(record):
        return record['ecl'] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    def validate_pid(record):
        return record['pid'].isdigit() and len(record['pid']) == 9

    def validate_haircolor(record):
        import re
        foo = record['hcl']
        return len(foo) == 7 and bool(re.search('^#[a-f0-9.-]*$', foo))

    return validate_years(record) and \
           validate_height(record) and \
           validate_eyecolor(record) and \
           validate_pid(record) and \
           validate_haircolor(record)


valid_counter = 0
total_counter = 0

required_fields = {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}
for passenger in read_passenger_data('problem4_data.txt'):
    total_counter += 1
    if required_fields - passenger.keys():
        continue
    if validate_data(passenger):
        valid_counter += 1
print(total_counter)
print(valid_counter)
