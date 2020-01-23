#from IPython.display import clear_output
import random

def display_board(board):
    #clear_output()
    print(f'  {board[7]}  |  {board[8]}  |  {board[9]}')
    print(' --- | --- | ---')
    print(f'  {board[4]}  |  {board[5]}  |  {board[6]}')
    print(' --- | --- | ---')
    print(f'  {board[1]}  |  {board[2]}  |  {board[3]}')

def player_input():
    player1 = ''
    player2 = ''
    while player1 not in ['X','O']:
        player1 = input("\nPlayer 1, please pick a marker 'X' or 'O' ")
    if player1 == 'X':
        player2 = 'O'
    else:
        player2 = 'X'
    return (player1,player2)

def place_marker(board, marker, position):
    board[position] = marker

def win_check(board, mark):
    for i in range(1,8,3):
        if(mark == board[i] == board[i+1] == board[i+2]):
            return True
    for i in range(1,4,1):
        if(mark == board[i] == board[i+3] == board[i+6]):
            return True
    if mark == board[1] == board[5] == board[9]:
        return True
    if mark == board[3] == board[5] == board[7]:
        return True
    return False 

def choose_first():
    return random.randint(1,2)

def space_check(board, position):
    return board[position] == ' '

def full_board_check(board):
    for position in board:
        if position == ' ':
            return True
    return False

def player_choice(board, player):
    position = 0
    while position == 0:
        position = int(input(f'\nPlayer {player} enter your position: '))
        if position >=1 and position <=9 and space_check(board,position):
            return position
        else:
            position = 0
            print('\nPosition invalid')
            
def toggle_player(player):
    if player == 1:
        return 2
    return 1 

def replay():
    playAgain = input('\nDo you want to play again? Yes or No ')
    return playAgain.lower() == 'yes'

print('\nWelcome to Tic Tac Toe!\n')

playAgain = True
player1 , player2 = player_input()
markers = [player1, player2]

while playAgain:
    #Initialize board
    board = [' ']*10
    board[0] = '#'
    
    #Pick which player starts
    player = choose_first()
    print(f'\nPlayer {player} plays first')

    #Check if the board is full
    while full_board_check(board):
        #Get position from player
        position = player_choice(board,player)
        #Place the marker on the board at the position
        place_marker(board,markers[player-1],position)
        #Display the game board
        display_board(board)
        #Check if the latest move makes a winner
        if win_check(board,markers[player-1]):
            print(f'\nPlayer {player} wins!')
            break
        #If no one wins, continue the game by taking turns
        player = toggle_player(player)   
    else:
        print('\nIts a tie!')
    #Continue if the player wants to play again
    playAgain = replay()
else:
    print('\nThanks for playing!')