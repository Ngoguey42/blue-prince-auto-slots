import time
import numpy as np
import pyautogui
import mss
import os
import numpy as np
import collections

from main_model import peek, infer
from config import *


def peek_spins(img):
    assert img.shape == (SCREEN_H, SCREEN_W, 3)
    assert img.dtype.name == 'float32'

    res = []
    for x in MACHINE.SPIN_XS:
        v = img[MACHINE.SPIN_Y, x]
        assert v.shape == (3,)
        v = v.mean()
        assert 0 <= v <= 1
        # OFF: 51, 65, 64
        # ON-: 158, 255, 223
        res.append(bool(v > 0.5))
    match res:
        case [False, False, False, False, False]:
            return 0
        case [False, False, False, False, True]:
            return 1
        case [False, False, False, True, True]:
            return 2
        case [False, False, True, True, True]:
            return 3
        case [False, True, True, True, True]:
            return 4
        case [True, True, True, True, True]:
            return 5

        case [False, False, False]:
            return 0
        case [False, False, True]:
            return 1
        case [False, True, True]:
            return 2
        case [True, True, True]:
            return 3

        case _:
            assert False, res


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


def get_probas():
    probas = {
        # Consider that probability of sampling a certain letter is 0%, until we've seen that letter 27 times
        letter: stats[letter] if stats[letter] > 27 else 0
        for letter in NAMES.keys()
    }
    tot = sum(probas.values())
    if len([v for v in probas.values() if v != 0]) <= 2:
        # If we're too early in the probability estimation process, just use 50-50 for dash and coin.
        probas['d'] = 5000 # dash
        probas['c'] = 5000 # coin
        tot = sum(probas.values())

    probas = {
        k: v / tot
        for k, v in probas.items()
    }
    return probas

print('stats', stats, get_probas())


def choose_action(actions, root=False):
    if len(actions) == 1:
        assert actions[0][0] == 'reroll'
        return actions[0]
    assert len(actions) == 5, actions
    if actions[0][0] == 'reroll':
        return actions[0] # Skipping the print

    reroll_val, = [
        v
        for k, v in actions
        if k == 'reroll'
    ]
    delta = actions[0][1] - reroll_val
    assert delta >= 0
    # if delta < 0.2: # Moved from 0.01 to 0.2
    #     if root:
    #         print('  \033[31mchoosing reroll over slightly better option\033[0m', f'{delta}')
    #     return ('reroll', reroll_val) # Favor reroll when it's close. It's suboptimal on the long run but it also kills some of the noise
    return actions[0]


memo_age = 0
memo = {}
def get_best_action(board0, spin_left, probas, depth=0):
    assert isinstance(board0, bytearray)
    assert spin_left >= 0
    if spin_left == 0:
        return [('reroll', board_value(board0.decode()))]
    # print('HEY', probas)

    global memo_age
    global memo
    if depth == 0:
        memo_age += 1
        print(f'  {memo_age=:} {len(memo)=:}')
        if memo_age >= 40: # Reset memoisation every 40 actions, to refresh probabilities
            memo_age = 0
            memo = {}
    key = (bytes(board0), spin_left)
    if key in memo:
        actions = memo[key]
        if depth == 0:
            print(' ', actions)
        return actions

    actions = {}
    actions['reroll'] = board_value(board0.decode())
    for i in range(4): # for each slot to reroll
        # sum_weighted_value = -1 # Start at -1 because spinning costs 1
        sum_weighted_value = -1.1 # Penalize spinning. Penilize risk.
        board = board0.copy()
        for dst_letter, proba in probas.items(): # explore every outcome
            board[i] = ord(dst_letter)
            next_best_actions = get_best_action(board, spin_left - 1, probas, depth=depth+1)
            next_best_action_, down_value = choose_action(next_best_actions)
            sum_weighted_value += proba * down_value
        actions[i] = sum_weighted_value # remember score of action
    actions = [
        (k, actions[k])
        for k in sorted(actions, key=lambda k: -actions[k])
    ]
    assert actions[0][1] >= actions[0][-1]
    if depth == 0:
        print(' ', actions)
    memo[key] = actions
    return actions

action_count = 0

path = os.path.join(PREFIX, 'events.txt')
with open(path, 'a') as event_stream:
    event_stream.write('p:start\n')
    just_had_movement = True
    prev_img = None
    last_action = None
    while True:
        # time.sleep(1) # TODO: Remove
        t0 = time.monotonic()
        # print('Polling')

        with mss.mss() as sct:
            monitor = sct.monitors[MSS_SCREEN_ID]
            img = sct.grab(monitor)
            img = np.asarray(img)[:, :, [2, 1, 0]]
            # print('  Snapshoted!', img.shape)
            assert img.shape == (SCREEN_H, SCREEN_W, 3)
            assert img.dtype.name == 'uint8'
            img = (img.astype('float32') / 255.)
            assert img.shape == (SCREEN_H, SCREEN_W, 3)
            assert 0 <= img.min() < img.max() <= 1.0

        if prev_img is None:
            print('Case 1 - First loop')
            prev_img = img
            continue

        diff = (prev_img - img) > 0.10
        assert diff.shape == (SCREEN_H, SCREEN_W, 3)
        diff = diff.any(axis=-1)
        assert diff.shape == (SCREEN_H, SCREEN_W)
        count = diff.flatten().sum() # number of pixels that changed significantly since last refresh
        if count > 200:
            print('Case 2 - There\'s movement')
            prev_img = img
            just_had_movement = True
            continue
        if not just_had_movement:
            print('Case 3 - Screen didn\'t move since last check')
            prev_img = img
            continue

        print('Case 4 - No movements after movements')
        just_had_movement = False
        prev_img = img

        board = ''
        for i in range(4):
            a = peek(img, i, plot=False)
            letter = infer(a)
            board += letter
            print(f'  {i} -> {NAMES[letter]}')


        if last_action is None:
            # Don't save if we don't know what was just done
            pass
        elif last_action == 'reroll':
            for letter in board:
                stats[letter] += 1
            event_stream.write(f'b:{board}\n')
        elif isinstance(last_action, int):
            assert last_action in [0, 1, 2, 3]
            new_letter = board[last_action]
            stats[new_letter] += 1
            tok = bytearray(b'....')
            tok[last_action] = ord(new_letter)
            tok = tok.decode()
            event_stream.write(f'b:{tok}\n')
        else:
            assert False
        if action_count % 10 == 1:
            print('stats', stats, get_probas())

        val = board_value(board)
        print(f'  value: {val}')
        spin_used = peek_spins(img)
        spin_left = MACHINE.SPIN_COUNT - spin_used
        print(f' {spin_left=:}')
        next_best_actions = get_best_action(bytearray(board.encode()), spin_left, get_probas())
        next_best_action, down_value = choose_action(next_best_actions, root=True)
        # next_best_action, down_value = get_best_action(bytearray(board.encode()), min(spin_left, 4), get_probas())
        # next_best_action, down_value = get_best_action(bytearray(board.encode()), 3, get_probas())
        print(f'  {next_best_action=:} {down_value=:}')

        if next_best_action == 'reroll':
            print(f'  \033[32m REROLL \033[0m')
            MACHINE.CLICK_LEVER()
        elif next_best_action == 0:
            MACHINE.CLICK_B0()
        elif next_best_action == 1:
            MACHINE.CLICK_B1()
        elif next_best_action == 2:
            MACHINE.CLICK_B2()
        elif next_best_action == 3:
            MACHINE.CLICK_B3()
        else:
            assert False
        last_action = next_best_action
        action_count += 1


        # t1 = time.monotonic()
        # print('process took', t1 - t0)

        # test_input = np.random.rand(144, 1, 3).astype(np.float32)
        # predicted_label = infer(test_input)

        # l = []

        #     l.append(a)

        # a = np.hstack(l)
        # print(a.shape, a.min(), a.max())
        # a = (a * 255).astype('uint8')
        # iio.imwrite(os.path.join(PREFIX, 'res.png'), a)

        # cptxsncd
        # cptx..cd





        # CLICK_LEVER()
        # time.sleep(3)
        # CLICK_B0()
        # time.sleep(3)
        # CLICK_B1()
        # time.sleep(3)
        # CLICK_B2()
        # time.sleep(3)
        # CLICK_B3()

        # for _ in range(10):
            # CLICK_LEVER()
            # time.sleep(1)
            # CLICK()
            # pyautogui.click()
            # print('clicked')


        # CLICK_LEVER()

        # pyautogui.click()






        #
