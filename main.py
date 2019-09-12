import csv


def parse(fname, letter, nc, pc):
    print('read {}.{} file'.format(fname, letter))
    f = open('c:/Users/supan/Documents/smeta/{}.{}.csv'.format(fname, letter), 'r')
    r = csv.reader(f, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)

    a = {}
    for row in r:
        # print('{} records'.format(row))
        name = row[nc].strip().replace('\xa0', ' ')
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
        qa = a[key_a]
        if key_a in b:
            qb = b[key_a]
            if qa == qb:
                c[key_a] = {'qnt': 1, 'comments': '', 'qa': qa, 'qb': qb}
            elif qa > qb:
                c[key_a] = {'qnt': 0, 'comments': 'добавить в смету {}'.format(qa - qb), 'qa': qa, 'qb': qb}
            else:
                c[key_a] = {'qnt': 2, 'comments': 'убрать из сметы {}'.format(qb - qa), 'qa': qa, 'qb': qb}
        else:
            c[key_a] = {'qnt': 0, 'comments': '', 'qa': qa, 'qb': 0}

    for key_b in b:
        qb = b[key_b]
        if key_b not in a:
            c[key_b] = {'qnt': 2, 'comments': '', 'qa': 0, 'qb': qb}

    return c
#       filename, aName,aPrice,bName,bPrice

def fix_doubles(d):
    res = {}
    cc = d.copy()
    to_del = None
    for key in d:
        res[key] = d[key]
        if d[key] == 1:
            continue

        for key_1 in cc:
            if d[key] == 1:
                continue

            if key == key_1:
                continue

            (name, price) = key
            (name_1, price_1) = key_1
            if price == price_1:
                min_q  = min(d[key]['qa'], d[key]['qb'])
                min_q1 = min(d[key_1]['qa'], d[key_1]['qb'])
                max_q  = max(d[key]['qa'], d[key]['qb'])
                max_q1 = max(d[key_1]['qa'], d[key_1]['qb'])
                if ((max_q - max_q1) == 0) and (name in name_1 or name_1 in name):
                    print("key: {}\nkey_1: {}\nmax_q: {}\nmax_q1: {}\n\n".format(key, key_1, max_q, max_q1))
                    # max_qa = max(d[key]['qa'], d[key_1]['qa'])
                    # max_qb = max(d[key]['qb'], d[key_1]['qb'])
                    res[key] = {'qnt': 1, 'comments': '', 'qa': 0, 'qb': 0}
                    # print("found {} - {} with same price/name".format(key, key_1))
                    to_del = key_1
                    break
        if to_del:
            del cc[to_del]
            to_del = None
            
    return res

accs = [
    ('108.52', 1, 5, '108.52', 5, 12),
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

    fmt = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
    f.write(fmt.format('счёт','наименование','стоимость','знач','комментарий','qa','qb','сумма'))
    for key_c in c:
        qa = c[key_c]['qa']
        qb = c[key_c]['qa']
        qnt = c[key_c]['qnt']
        (name, price) = key_c
        total = -(price * qb) if qnt == 2 else (price * qa)
        f.write(fmt.format(acc[3],key_c[0], str(key_c[1]).replace('.',','), c[key_c]['qnt'], c[key_c]['comments'], c[key_c]['qa'], c[key_c]['qb'], total))

f.close()
