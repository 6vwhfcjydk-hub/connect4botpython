# Claude's Connect 4 bot, v2
# negamax + alpha-beta, transposition table, iterative deepening,
# forced-move extensions, and a Connect 4 threat-aware evaluation.
#
# Interface: choose_move(board, s, depth=8) -> column index 0-6
# Board: 6 lists of 7 cells, row 0 = top, '.' = empty, 'X'/'O' = pieces.

ROWS, COLS = 6, 7
EMPTY = '.'
ORDER = [3, 2, 4, 1, 5, 0, 6]   # centre first: better pruning
WIN = 1_000_000
MATE_BAND = 1_000               # scores this close to WIN are forced wins/losses
INF = float('inf')
EXTEND_FORCED = True            # forced blocks don't use up depth

EXACT, LOWER, UPPER = 0, 1, 2
TT = {}


def _all_windows():
    # every group of 4 cells that could make a connect 4 (69 in total)
    w = []
    for r in range(ROWS):
        for c in range(COLS - 3):
            w.append([(r, c + i) for i in range(4)])        # horizontal
    for r in range(ROWS - 3):
        for c in range(COLS):
            w.append([(r + i, c) for i in range(4)])        # vertical
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            w.append([(r + i, c + i) for i in range(4)])    # diagonal down
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            w.append([(r - i, c + i) for i in range(4)])    # diagonal up
    return w


WINDOWS = _all_windows()


def _other(s):
    return 'O' if s == 'X' else 'X'


def _drop_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def _would_win(board, row, col, p):
    # would p make four by playing at (row, col)? the cell itself is not read
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        count = 1
        for sign in (1, -1):
            r, c = row + dr * sign, col + dc * sign
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == p:
                count += 1
                r += dr * sign
                c += dc * sign
        if count >= 4:
            return True
    return False


def _threat_value(mine, theirs, first):
    # value of a player's threats (empty cells that would complete four)
    v = 0
    for r, c in mine:
        if any(cc == c and rr > r for rr, cc in theirs):
            v += 4          # opponent has a lower threat in this column: this one rarely matters
            continue
        odd = (ROWS - r) % 2 == 1          # row counted from the bottom, starting at 1
        good = odd if first else not odd   # first player wants odd rows, second wants even
        v += 60 if good else 15
        if (r - 1, c) in mine:
            v += 120        # two threats stacked vertically: usually a forced win
    return v


def _score(board, s):
    # heuristic from the point of view of s (the player to move)
    o = _other(s)
    n_s = sum(row.count(s) for row in board)
    n_o = sum(row.count(o) for row in board)
    s_first = (n_s == n_o)   # s is to move, so equal counts means s started

    score = 0
    for r in range(ROWS):
        for c, wt in ((3, 4), (2, 2), (4, 2)):
            if board[r][c] == s:
                score += wt
            elif board[r][c] == o:
                score -= wt

    ts, to = set(), set()
    for win in WINDOWS:
        m = t = 0
        gap = None
        for r, c in win:
            v = board[r][c]
            if v == s:
                m += 1
            elif v == o:
                t += 1
            else:
                gap = (r, c)
        if m and t:
            continue            # blocked window
        if m == 3:
            ts.add(gap)
        elif t == 3:
            to.add(gap)
        elif m == 2:
            score += 3
        elif t == 2:
            score -= 3

    score += _threat_value(ts, to, s_first)
    score -= _threat_value(to, ts, not s_first)
    return score


def _to_tt(v, ply):
    if v > WIN - MATE_BAND:
        return v + ply
    if v < -WIN + MATE_BAND:
        return v - ply
    return v


def _from_tt(v, ply):
    if v > WIN - MATE_BAND:
        return v - ply
    if v < -WIN + MATE_BAND:
        return v + ply
    return v


def _key(board, s):
    return ''.join(''.join(row) for row in board) + s


def _negamax(board, depth, alpha, beta, s, ply):
    # s = player to move; returns score from s's point of view
    o = _other(s)
    valid = [c for c in ORDER if board[0][c] == EMPTY]
    if not valid:
        return 0                            # draw
    drops = {c: _drop_row(board, c) for c in valid}

    # 1. win right now if we can
    for c in valid:
        if _would_win(board, drops[c], c, s):
            return WIN - ply

    # 2. opponent threatens to win next move?
    must = [c for c in valid if _would_win(board, drops[c], c, o)]
    if len(must) > 1:
        return -(WIN - ply - 1)             # can only block one
    if must:
        moves = must
        child_depth = depth if EXTEND_FORCED else depth - 1
    else:
        # never play directly under a cell the opponent wins on
        moves = [c for c in valid
                 if not (drops[c] > 0 and _would_win(board, drops[c] - 1, c, o))]
        if not moves:
            return -(WIN - ply - 1)         # every move hands them the win
        if depth <= 0:
            return _score(board, s)
        child_depth = depth - 1

    # 3. transposition table
    key = _key(board, s)
    entry = TT.get(key)
    if entry is not None:
        e_depth, e_val, e_flag, tt_move = entry
        if e_depth >= depth:
            v = _from_tt(e_val, ply)
            if e_flag == EXACT:
                return v
            if e_flag == LOWER and v >= beta:
                return v
            if e_flag == UPPER and v <= alpha:
                return v
        if tt_move in moves:
            moves = [tt_move] + [c for c in moves if c != tt_move]

    # 4. search
    orig_alpha = alpha
    best, best_move = -INF, moves[0]
    for c in moves:
        r = drops[c]
        board[r][c] = s
        val = -_negamax(board, child_depth, -beta, -alpha, o, ply + 1)
        board[r][c] = EMPTY
        if val > best:
            best, best_move = val, c
        if best > alpha:
            alpha = best
        if alpha >= beta:
            break

    if best <= orig_alpha:
        flag = UPPER
    elif best >= beta:
        flag = LOWER
    else:
        flag = EXACT
    TT[key] = (depth, _to_tt(best, ply), flag, best_move)
    return best


def choose_move(board, s, depth=20):
    # returns a column index 0-6
    board = [row[:] for row in board]       # work on a copy
    o = _other(s)
    valid = [c for c in ORDER if board[0][c] == EMPTY]
    if not valid:
        return None
    drops = {c: _drop_row(board, c) for c in valid}

    for c in valid:                         # immediate win
        if _would_win(board, drops[c], c, s):
            return c
    must = [c for c in valid if _would_win(board, drops[c], c, o)]
    if must:                                # forced block
        return must[0]
    moves = [c for c in valid
             if not (drops[c] > 0 and _would_win(board, drops[c] - 1, c, o))]
    if not moves:
        return valid[0]                     # lost whatever we do
    if len(moves) == 1:
        return moves[0]

    TT.clear()
    best_col = moves[0]
    for d in range(1, depth + 1):           # iterative deepening
        order = [best_col] + [c for c in moves if c != best_col]
        alpha, best_val, iter_best = -INF, -INF, order[0]
        for c in order:
            r = drops[c]
            board[r][c] = s
            val = -_negamax(board, d - 1, -INF, -alpha, o, 1)
            board[r][c] = EMPTY
            if val > best_val:
                best_val, iter_best = val, c
            alpha = max(alpha, val)
        best_col = iter_best
        if abs(best_val) > WIN - MATE_BAND:
            break                           # forced result found; deeper won't change it
    return best_col