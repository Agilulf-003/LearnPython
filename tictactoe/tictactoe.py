import os


def print_board(board):
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])


def main():
    init_board = {
        7: ' ', 8: ' ', 9: ' ',
        4: ' ', 5: ' ', 6: ' ',
        1: ' ', 2: ' ', 3: ' '
    }#dic
    init_list = {1,2,3,4,5,6,7,8,9}
    begin = True
    while begin:
        curr_board = init_board.copy() #Python 直接赋值、浅拷贝和深度拷贝
        curr_list = init_list.copy()
        begin = False
        turn = 'x'
        counter = 0
        os.system('cls')
        print_board(curr_board)
        while counter < 9:
            if turn == 'x':
                move = input('轮到%s走棋, 请输入位置: ' % turn)
                move = int(move)
                if curr_board[move] == ' ':
                    curr_board[move] = turn
                    curr_list.remove(move)      
                curr_board[move] = turn
                if turn == 'x':
                    turn = 'o'
                else:
                    turn = 'x'
            os.system('cls')
            print_board(curr_board)
        choice = input('再玩一局?(yes|no)')
        begin = choice == 'yes'


if __name__ == '__main__':
    main()
