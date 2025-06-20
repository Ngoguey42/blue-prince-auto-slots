import pandas as pd
import collections
import os

PREFIX = os.path.dirname(__file__)




def board_value_pattern(board):
    assert isinstance(board, str)
    assert len(board) == 4
    c = collections.Counter()
    for letter in board:
        c[letter] += 1
    if c['s'] > 0 and c['n'] == 0:
        return 'uncaught-snake'
    tot = 0
    pat = []
    # print('COMPUTING VALUE:', c)

    # c - coin
    if c['c'] == 3:
        tot += 3
        pat += [f'3-coins']
    if c['c'] == 4:
        pat += [f'4-coints']
        tot += 5
    # p - pile
    if c['p'] == 3:
        pat += [f'3-piles']
        tot += 9
    if c['p'] == 4:
        pat += [f'4-piles']
        tot += 15
    # t - tref
    tot += c['t'] * 10
    if c['t'] > 0:
        pat += [f'{c["t"]}-clover']
    # s - snak / n - net
    # tot += c['s'] * c['n'] * 3 # This is wrong, observed ig
    diff = c['s'] * min(1, c['n']) * 3
    tot += diff
    if diff > 0:
        pat += [f'{c["s"]}-snake-caught']
    # w - crown
    if c['w'] == 4:
        tot += 100
        pat += [f'4-crowns']
    # x - 2x # SHOULD BE LAST
    fact = 2 ** c['x']
    tot = tot * fact
    if fact != 1:
        pat += [f'x{fact:.0f}']
    if tot == 0:
        return 'zero'
    else:
        return ' + '.join(pat)



def board_value(board):
    assert isinstance(board, str)
    assert len(board) == 4
    c = collections.Counter()
    for letter in board:
        c[letter] += 1
    if c['s'] > 0 and c['n'] == 0:
        return 0
    tot = 0
    # print('COMPUTING VALUE:', c)

    # c - coin
    if c['c'] == 3:
        tot += 3
    if c['c'] == 4:
        tot += 5
    # p - pile
    if c['p'] == 3:
        tot += 9
    if c['p'] == 4:
        tot += 15
    # t - tref
    tot += c['t'] * 10
    # s - snak / n - net
    # tot += c['s'] * c['n'] * 3 # This is wrong, observed ig
    tot += c['s'] * min(1, c['n']) * 3
    # w - crown
    if c['w'] == 4:
        tot += 100
    # x - 2x # SHOULD BE LAST
    tot = tot * 2 ** c['x']
    return tot


prev = None
rows = []
for ev in open('events.txt').read().strip().split('\n'):
    if not ev.startswith('b:'):
        continue
    ev = ev[2:]
    assert len(ev) == 4
    if '.' not in ev:
        if rows:
            rows[-1]['last'] = True
        rows.append(dict(board=ev))
        prev = bytearray(ev.encode())
    else:
        for i, letter in enumerate(ev):
            if letter == '.': continue
            prev[i] = ord(letter)
        rows.append(dict(board=bytes(prev).decode()))
    # print(rows[-1])
df = pd.DataFrame(rows)
df['last'].fillna(False, inplace=True)
print(df)

NAMES = dict(
    c= 'coin',
    p= 'pile',
    t= 'clover',
    x= '2x',
    s= 'snake',
    n= 'net',
    w= 'crown',
    d= 'dash',
)

for k in NAMES:
    df[k] = df.board.apply(lambda x: x.count(k))

df['val'] = df.board.apply(board_value)
df = df.sort_values('val', ascending=False)
print(df)

indices = set(i + d for i in sorted(df[df.val == 80].index) for d in range(-5, 1))
print(df[df.apply(lambda row: row.name in indices, axis=1)].sort_index())


# d = df[df['last']].copy()
# d['bs'] = df.board.apply(lambda x: ''.join(sorted(x)))
# d = d.groupby(['bs']).agg(dict(board='first', val='first', bs='count')).rename(columns=dict(bs='count'))
# d = d.sort_values('val')
# d['proba'] = d['count'] / d['count'].sum()
# print(d)
# x = (d.val * d.proba).sum()
# print(f'average return per session (between 2 arm pulls): {x:.2f} (includes the cost of pulling the arm and rolling its slots)')
# d['x'] = (d.val * d.proba)
# d['y'] = d.val * d['count']
# d = d.sort_values('y', ascending=False)
# d['z'] = d.y / d.y.sum()
# i = 0
# for _, row in d.iterrows():
#     i += 1
#     if i >= 10: break
#     x = []
#     for k, v in collections.Counter(row.board).items():
#         x.append(f'{v} {NAMES[k]}')
#     x = ' + '.join(x)
#     print(f'- Source of revenue #{i}: {row.z:.1%} of revenue: {x}')
# print(d)


d = df[df['last']].copy()
d['bs'] = df.board.apply(board_value_pattern)
d = d.groupby(['bs']).agg(dict(board='first', val='first', bs='count')).rename(columns=dict(bs='count'))
d = d.sort_values('val')
d['proba'] = d['count'] / d['count'].sum()
print(d)
x = (d.val * d.proba).sum()
print(f'average return per session (between 2 arm pulls): {x:.2f} (includes the cost of pulling the arm and rolling its slots)')
d['x'] = (d.val * d.proba)
d['y'] = d.val * d['count']
d = d.sort_values('y', ascending=False)
d['z'] = d.y / d.y.sum()
i = 0
print('rank,pattern,% of revenue,% of cash outs')
for name, row in d.iterrows():
    i += 1
    x = []
    # print(f'- Source of revenue #{i}: {name} | {row.z:.1%} of revenue | {row.proba:.2%} of cash outs')
    print(f'#{i},{name},{row.z:.1%},{row.proba:.2%}')
# print(d)


path = os.path.join(PREFIX, 'events.txt')
events = open(path).read().strip().split('\n')
if events == ['']:
    events = []

stats = collections.Counter()
for ev in events:
    if ev.startswith('p:'): continue
    assert ev.startswith('b:')
    ev = ev[2:]
    assert len(ev) == 4
    for letter in ev:
        if letter == '.': continue
        assert letter in NAMES
        stats[letter] += 1

tot = sum(stats.values())

for k, v in stats.items():
    print(f'- {NAMES[k]} {v / tot:.1%}')



#
