import csv


def parse(fname, letter, nc, pc):
    f = open('c:/Users/omgbe/Documents/smeta/{}.{}.csv'.format(fname, letter), 'r')
    r = csv.reader(f,quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)

    a = {}
    for row in r:
        name = row[nc].strip()
        price = float(row[pc].replace(',', '.'))
        key = (name, price)
        if name == "":
            continue

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

accs = [('108.51',1,5,7,14),
        ('108.52',1,5,7,14),
        ('108.55',1,5,7,14),
        ('108.56',1,5,7,14),
        ]
f = open('c:/Users/omgbe/Documents/smeta/108.C.csv', 'w')
for acc in accs:
    print("processing {} account".format(acc[0]))
    a = parse(acc[0],'A', acc[1], acc[2])
    b = parse(acc[0],'B', acc[3], acc[4])
    c = compare(acc[0], a, b)

    for key_c in c:
        f.write('{}\t{}\t{}\t{}\t{}\n'.format(acc[0],key_c[0], key_c[1], c[key_c]['qnt'], c[key_c]['comments']))

f.close()
