import csv


def parse(fname, letter, nc, pc):
    f = open('c:/Users/supan/Documents/smeta/{}.{}.csv'.format(fname, letter), 'r')
    r = csv.reader(f, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)

    a = {}
    for row in r:
        name = row[nc].strip()
        if name == "" or row[pc] == '-':
            continue

        print(row[pc])
        price = float(row[pc].replace(',', '.').replace(' ', '').replace('\xa0', ''))
        key = (name, price)


        if key in a:
            a[key] = a[key] + 1
        else:
            a[key] = 1

    return a


def compare(fname, a, b):
    c = {}
    for key_a in a:
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
        if key_b not in a:
            c[key_b] = {'qnt': 2, 'comments': ''}

    return c
#       filename, aName,aPrice,bName,bPrice
accs = [
    ('108.51', 1, 5, '108.51', 7, 14),
    ('108.52', 1, 5, '108.52', 7, 14),
    ('108.55', 1, 5, '108.55', 7, 14),
    ('108.56', 1, 5, '108.56', 7, 14),
    ('108.51', 1, 7, '104.51', 7, 15)
        ]
f = open('c:/Users/supan/Documents/smeta/result.C.csv', 'w')
for acc in accs:
    print("processing {} account".format(acc[0]))
    a = parse(acc[0],'A', acc[1], acc[2])
    b = parse(acc[3],'B', acc[4], acc[5])
    c = compare(acc[0], a, b)

    for key_c in c:
        f.write('{}\t{}\t{}\t{}\t{}\n'.format(acc[3],key_c[0], key_c[1], c[key_c]['qnt'], c[key_c]['comments']))

f.close()
