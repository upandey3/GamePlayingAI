from sample_players import *
from game_agent import *
from isolation import *
import time
TIME_LIMIT_MILLIS = 150


def check_symmetry(game):
    l = game._board_state
    h = game.height; w = game.width
    matrix = [l[i:i+h] for i in range(0, h * w, h)]
    #for i in (90, 180, 270):
    m = matrix[::-1]
    m2 = [i[::-1] for i in matrix]
    return m2

def get_board_state(matrix, game):
    h = game.height; w = game.width
    b = [0] * (h * w + 3)
    for i, u in enumerate(matrix):
        for j, v in enumerate(u):
            b[i * h + j] = matrix[i][j]

    b[-1] = 0 #game._board_state[-1]
    b[-2] = 0 #game._board_state[-2]
    b[-3] = 0 #game._board_state[-3]
    return b

def rotate(matrix):
    return list(zip(*matrix[::-1]))

def hash(b):
    return str(b.__hash__())

start_time = time.time()
# create an isolation board (by default 7x7)
player1 = AlphaBetaPlayer(score_fn= custom_score_3)
# player1 = AlphaBetaPlayer(score_fn=improved_score)
player2 = AlphaBetaPlayer(score_fn = improved_score)
game = Board(player1, player2)

# place player 1 on the board at row 2, column 3, then place player 2 on
# the board at row 0, column 5; display the resulting board state.  Note
# that the .apply_move() method changes the calling object in-place.
game.apply_move((3, 3))
new_game = game.forecast_move((0, 1))
new_game2 = game.forecast_move((6, 1))

print(new_game.to_string())
print(new_game2.to_string())


x = check_symmetry(new_game2)
b = get_board_state(x, new_game2)
new_game2._board_state = b
print(new_game2.to_string())

# x = rotate(x)
# b = get_board_state(x, new_game2)
# new_game2._board_state = b
# print(new_game2.to_string())
#
# x = rotate(x)
# new_game2._board_state = b
# print(new_game2.to_string())
#
# x = rotate(x)
# new_game2._board_state = b
# print(new_game2.to_string())
#
# b = get_board_state(x, new_game2)
#
# new_game._board_state[-1] = 0 #game._new_game._board_state[-1]
# new_game._board_state[-2] = 0 #game._new_game._board_state[-2]
# new_game._board_state[-3] = 0 #game._new_gameoard_state[-3]
#
# print(new_game._board_state)
# print(b)
# print(b == new_game._board_state)
#
# new_game2._board_state = b
# print(new_game2.to_string())
#
# # x = rotate(x)
# # print(game._board_state)
# # b = get_board_state(x, game)
# # print(b)
# #
# # print(b == game._board_state)
# # new_game = game.forecast_move((0 , 0))
# # new_game._board_state = b
# # print( game.hash())
# # print (new_game.hash())
# print("--- %s seconds ---" % (time.time() - start_time))
