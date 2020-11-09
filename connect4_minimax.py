def get_board(state):
    board = [[' ' for i in range(7)] for j in range(6)]
    for idx,chip in enumerate(state):
        row = idx//7
        col = idx%7
        board[abs(row-5)][col] = chip
    return board

def is_valid_push(board,push_col):
    col = [row[push_col] for row in board]
    if ' ' in col:
        return True
    else:
        return False

def push(state,chip,push_col):
    for idx,pushed_chip in enumerate(state):
        if idx%7 == push_col and pushed_chip == ' ':
            state = state[:idx]+chip+state[idx+1:]
            return state

def show_board(state):
    board = get_board(state)
    for idx,row in enumerate(board):
        print(str(abs(idx-6))+" | "+" | ".join(row)+" |")
    print('  --1---2---3---4---5---6---7--')
    print('\n')

def space_count(window):
    count = 0
    for block in window:
        if block == ' ':
            count += 1
    return count

def horizontal_seq(board,chip,length):
    before = False
    count = 0
    seq_check = chip*length
    space_check = 4-length
    for r in range(6):
        for c in range(4):
            window = str(board[r][c])+str(board[r][c+1])+str(board[r][c+2])+str(board[r][c+3])
            if seq_check in window and space_count(window) == space_check:
                if before == False:
                    count += 1
                    before = True
            else:
                before = False
    return count

def vertical_seq(board,chip,length):
    before = False
    count = 0
    seq_check = chip*length
    space_check = 4-length
    for r in range(3,6):
        for c in range(0,7):
            window = str(board[r][c])+str(board[r-1][c])+str(board[r-2][c])+str(board[r-3][c])
            if seq_check in window and space_count(window) == space_check:
                if before == False:
                    count += 1
                    before = True
            else:
                before = False
    return count

def pos_diagonal_seq(board,chip,length):
    before = False
    count = 0
    seq_check = chip*length
    space_check = 4-length
    for r in range(3,6):
        for c in range(0,4):
            window = str(board[r][c])+str(board[r-1][c+1])+str(board[r-2][c+2])+str(board[r-3][c+3])
            if seq_check in window and space_count(window) == space_check:
                if before == False:
                    count += 1
                    before = True
            else:
                before = False
    return count

def neg_diagonal_seq(board,chip,length):
    before = False
    count = 0
    seq_check = chip*length
    space_check = 4-length
    for r in range(3,6):
        for c in range(3,7):
            window = str(board[r][c])+str(board[r-1][c-1])+str(board[r-2][c-2])+str(board[r-3][c-3])
            if seq_check in window and space_count(window) == space_check:
                if before == False:
                    count += 1
                    before = True
            else:
                before = False
    return count

def count_seq(board,chip,length):
    return horizontal_seq(board,chip,length)+vertical_seq(board,chip,length)+pos_diagonal_seq(board,chip,length)+neg_diagonal_seq(board,chip,length)

def is_win(board,chip):
    if count_seq(board,chip,4) >= 1:
        return True
    else:
        return False

def evaluate(board):

    if count_seq(board,'B',4) >= 1:
        return 1000000

    human_score = count_seq(board,'H',4)*10000+count_seq(board,'H',3)*1000+count_seq(board,'H',2)*100
    bot_score = count_seq(board,'B',4)*10000+count_seq(board,'B',3)*1000+count_seq(board,'B',2)*100
    return bot_score-human_score

def count_chip(state):
    return sum([1 for char in state if char != ' '])

def alpha_beta_decision(state):
    max_value = float('-inf')
    a = float('-inf')
    b = float('inf')
  
    #handle max _depth
    global max_depth
    n_chip = count_chip(state)
    if n_chip < 12:
        max_depth = 6
    elif n_chip < 24:
        max_depth = 8
    else:
        max_depth = 10

    #handle first play of Bot(B)
    if n_chip == 0:
        return 3
    board = get_board(state)
    for push_col in range(7):
        if not is_valid_push(board,push_col):
            continue
        new_state = push(state,'B',push_col)
        ret = min_value(new_state,a,b,0)
        if ret > max_value:
            max_value = ret
            action = push_col
    print('Bot move is:',action+1)
    return action

def min_value(state,a,b,level):

    #terminate
    board = get_board(state)
    if is_win(board,'B'):
        return 10000000

    #cutoff 
    if level >= max_depth:
        return evaluate(board)

    v = float('inf')

    for push_col in range(7):
        if not is_valid_push(board,push_col):
            continue
        new_state = push(state,'H',push_col)
        v = min(v,max_value(new_state,a,b,level+1))
        if v <= a:
            return v
        if b == float('inf'):
            b = v
        b = min(b,v)
    return v

def max_value(state,a,b,level):

    #terminate
    board = get_board(state)
    if is_win(board,'H'):
        return -10000000

    v = float('-inf')
    
    for push_col in range(7):
        if not is_valid_push(board,push_col):
            continue
        new_state = push(state,'B',push_col)
        new_board = get_board(new_state)
        if is_win(new_board,'B'):
            return 10000000
    
    for push_col in range(7):
        if not is_valid_push(board,push_col):
            continue
        new_state = push(state,'B',push_col)
        v = max(v,min_value(new_state,a,b,level+1))
        if v >= b:
            return v
        if a == float('-inf'):
            a = v
        a = max(a,v)
    return v

def main():
    is_human_turn = False
    state = ' '*42

    while ' ' in state:
        if is_human_turn:
            c = int(input('Please enter your column:'))
            board = get_board(state)
            while not is_valid_push(board,c-1):
                print('You cannot put in column',c)
                c = int(input('Please enter your column:'))
            state = push(state,'H',c-1)
            board = get_board(state)
            show_board(state)
            if is_win(board,'H'):
                print('Human win!!!')
                show_board(state)
                break
            is_human_turn = False
        else:
            c = alpha_beta_decision(state)
            state = push(state,'B',c)
            board = get_board(state)
            show_board(state)
            if is_win(board,'B'):
                print('Bot win!!!')
                show_board(state)
                break
            is_human_turn = True

main()