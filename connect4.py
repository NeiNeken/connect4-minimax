import threading
import time

def get_board(state):
    board = [['X' for i in range(7)] for j in range(6)]
    for idx,chip in enumerate(state):
        row = idx//7
        col = idx%7
        board[abs(row-5)][col] = chip
    return board

def count_space(item):
    space = 0
    for char in item:
        if char == 'X':
            space += 1
    return space

def countSeries(board,chip,length):
    count = 0
    compare = chip*length
    space = 4-length
    for c in range(7):
        for r in range(6):

            # Horizontal 
            if c < 7 and r > 2 and r < 6:
                item = board[r][c]+board[r-1][c]+board[r-2][c]+board[r-3][c]
                if compare in item and count_space(item) == space:
                    count+=1
            
            # Vertical 
            if c < 4 and r < 6:
                item = board[r][c]+board[r][c+1]+board[r][c+2]+board[r][c+3]
                if compare in item and count_space(item) == space:
                    count+=1
            
            # Positive diagonal 
            if c < 4 and r > 2 and r < 6:
                item = board[r][c]+board[r-1][c+1]+board[r-2][c+2]+board[r-3][c+3]
                if compare in item and count_space(item) == space:
                    count+=1
            
            # Negative diagonal 
            if c < 4 and r < 3:
                item = board[r][c]+board[r+1][c+1]+board[r+2][c+2]+board[r+3][c+3]
                if compare in item and count_space(item) == space:
                    count+=1
    return count
    

def is_win(board,chip):
    connect4 = countSeries(board,chip,4)
    if connect4 > 0:
        return True
    else:
        return False
    
def evaluate(state):
    board = get_board(state)

    p_connect2 = countSeries(board,'P',2)
    p_connect3 = countSeries(board,'P',3)
    p_connect4 = countSeries(board,'P',4)
    
    a_connect2 = countSeries(board,'A',2)
    a_connect3 = countSeries(board,'A',3)
    a_connect4 = countSeries(board,'A',4)

    p_score = (p_connect2)*10 + (p_connect3)*100 + (p_connect4)*10000
    a_score = (a_connect2)*10 + (a_connect3)*100 + (a_connect4)*10000

    score = a_score - p_score 

    return score

    
def is_valid_push(board,push_col):
    col = [row[push_col] for row in board]
    if 'X' in col:
        return True
    else:
        return False

def push(state,chip,push_col):
    for idx,pushed_chip in enumerate(state):
        if idx%7 == push_col and pushed_chip == 'X':
            state = state[:idx]+chip+state[idx+1:]
            return state

def max_value(state,a,b,level):
    board = get_board(state)
    
    if is_win(board,'A'):
        return float('-inf')

    if level >= max_depth:
        return evaluate(state)
    
    v = float('-inf')
    for push_col in range(7):
        if not is_valid_push(board,push_col):
            continue
        
        new_state = push(state,'P',push_col)
        if is_win(board,'p'):
            return float('inf')
        v = max(v,min_value(new_state,a,b,level+1))
        if v >= b: 
            return v
        if a == -10:
            a = v
        else:
            a = max(a,v)
    return v

def min_value(state,a,b,level):
    board = get_board(state)
    
    if is_win(board,'P'):
        return float('inf')
        
    v = float('inf')
    for push_col in range(7):
        if not is_valid_push(board,push_col):
            continue
        new_state = push(state,'A',push_col)
        v = min(v,max_value(new_state,a,b,level+1))
        if v <= a: 
            return v
        if b == 10:
            b = v
        else:
            b = min(b,v)
    return v

def minimax_decision(state):
    global max_depth
    max_value = float('-inf')
    a,b=-10,10
    board = get_board(state)

    chips = count_chip(state)

    if chips == 0:
        return 3

    if chips < 5:
        max_depth = 6
    elif chips < 12:
        max_depth = 8
    elif chips < 24:
        max_depth = 10
    else:
        max_depth = 10
    
    for push_col in range(7):
        if not is_valid_push(board,push_col):
            continue
        state = push(state,'P',push_col)
        ret = min_value(state,a,b,0)
        if ret > max_value:
            max_value=ret
            action = push_col
    print(action+1)
    return action        

def show_board(state):
    board = get_board(state)
    for row in board:
        new_row = []
        for char in row:
            if char == 'X':
                new_row.append(' ')
            else:
                new_row.append(char)
        print("| "+" | ".join(new_row)+" |")
    print('-----------------------------')
    print('\n')

def count_chip(state):
    return sum([1 for char in state if char != 'X'])
    
is_ai_turn = False
state = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
show_board(state)
while 'X' in state:
    if is_ai_turn:
        c = int(input('Please enter your column:'))
        board = get_board(state)
        while not is_valid_push(board,c-1):
            print('You cannot put in column',c)
            c = int(input('Please enter your column:'))
        state = push(state,'A',c-1)
        board = get_board(state)
        show_board(state)
        if is_win(board,'A'):
            print('Perfext AI win!')
            show_board(state)
            break
        is_ai_turn = False
    else:
        c = minimax_decision(state)
        state = push(state,'P',c)
        board = get_board(state)
        show_board(state)
        if is_win(board,'P'):
            print('My minimax win!!!')
            show_board(state)
            break
        is_ai_turn = True