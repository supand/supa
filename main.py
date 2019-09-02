import csv


def parse(fname, letter, nc, pc):
    print('read {}.{} file'.format(fname, letter))
    f = open('c:/Users/supan/Documents/smeta/{}.{}.csv'.format(fname, letter), 'r')
    r = csv.reader(f, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)

    a = {}
    for row in r:
        # print('{} records'.format(row))
        name = row[nc].strip()
        name = name.strip(', ')
        name = name.strip(',')
        if name == "" or row[pc] == '-':
            continue

        price = float(row[pc].replace(',', '.').replace(' ', '').replace('\xa0', ''))
        key = (name, price)


        if key in a:
            a[key] = a[key] + 1
        else:
            a[key] = 1

    # print('parsed {} records'.format(len(a)))
    return a

def compare(fname, a, b):
    c = {}
    for key_a in a:
        # print("'A: {}'".format(key_a))

        if key_a in b:
            qa = a[key_a]
            qb = b[key_a]
            if qa == qb:
                c[key_a] = {'qnt': 1, 'comments': ''}
            elif qa > qb:
                c[key_a] = {'qnt': 0, 'comments': 'добавить в смету {}'.format(qa - qb)}
            else:
                c[key_a] = {'qnt': 2, 'comments': 'убрать из сметы {}'.format(qb - qa)}
        else:
            c[key_a] = {'qnt': 0, 'comments': ''}

    for key_b in b:
        # print("'B: {}'".format(key_b))
        if key_b not in a:
            c[key_b] = {'qnt': 2, 'comments': ''}

    return c
#       filename, aName,aPrice,bName,bPrice

def fix_doubles(d):
    res = {}
    for key in d:
        res[key] = d[key]
        if d[key] == 1:
            continue

        for key_1 in d:
            if key == key_1:
                continue

            (name, price) = key
            (name_1, price_1) = key_1
            if price == price_1 and (name in name_1 or name_1 in name):
                print('rewrite {} to {}'.format(key, key_1))
                res[(name, price)] = {'qnt': 1, 'comments': ''}

    return res

accs = [
    ('108.51', 1, 5, '108.51', 5, 12),
    # ('108.52', 1, 5, '108.52', 7, 14),
    # ('108.55', 1, 5, '108.55', 7, 14),
    # ('108.56', 1, 5, '108.56', 7, 14),
    # ('108.51', 1, 7, '104.51', 7, 15)
        ]
f = open('c:/Users/supan/Documents/smeta/result.C.csv', 'w')
for acc in accs:
    print("processing {} account".format(acc[0]))
    a = parse(acc[0],'A', acc[1], acc[2])
    b = parse(acc[3],'B', acc[4], acc[5])
    c = compare(acc[0], a, b)
    c = fix_doubles(c)

    f.write('{}\t{}\t{}\t{}\t{}\n'.format('счёт','наименование','стоимость','знач','bebebe'))
    for key_c in c:
        f.write('{}\t{}\t{}\t{}\t{}\n'.format(acc[3],key_c[0], str(key_c[1]).replace('.',','), c[key_c]['qnt'], c[key_c]['comments']))

f.close()
