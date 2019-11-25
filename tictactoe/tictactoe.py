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
    #init_list = [1,2,3,4,5,6,7,8,9]
    init_set = {1,2,3,4,5,6,7,8,9}
    begin = True
    while begin:
        curr_board = init_board.copy() #Python 直接赋值、浅拷贝和深度拷贝
        curr_set = init_set.copy()
        player1_set = set()
        player2_set = set()
        player1win = 0
        player2win = 0
        winpattern= [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
        begin = False
        os.system('cls')
        choose = input('先 ‘1’ or 后 ‘2’ ？:')
        if choose == '1':
            turn = 'x'
        else:
            turn = 'o'
        os.system('cls')
        print_board(curr_board)
        while curr_set and player1win == 0 and player2win == 0:
            if turn == 'x':
                move = input('轮到%s走棋, 请输入位置: ' % turn)
                move = int(move)
                while curr_board[move] != ' ':
                    move = input('轮到%s走棋, 请输入位置: ' % turn)
                    move = int(move)
                curr_board[move] = turn
                curr_set.remove(move)
                player1_set.add(move)
            else:
                from random import choice
                if 5 in curr_set:
                    move = 5
                else:
                    move = choice(list(curr_set))
                curr_board[move] = turn
                curr_set.remove(move)
                player2_set.add(move)
            if turn == 'x':
                turn = 'o'
            else:
                turn = 'x'
            for pt in winpattern:
                if pt.issubset(player1_set):#don't forget :
                    player1win = 1
                if pt.issubset(player2_set):
                    player2win = 1
            os.system('cls')
            print_board(curr_board)   
        if player1win:
            print('You win') 
        elif player2win:
            print('You lost') 
        else:
            print('draw') 
        choice = input('再玩一局?(yes|no)')
        begin = choice == 'yes'


if __name__ == '__main__':
    main()
