"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random
import itertools

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    legal_moves = game.get_legal_moves()
    self_is_active = player == game._active_player # flag for whether self is active

    if not legal_moves:
        if self_is_active:
            return float("-inf")
        else:
            return float("inf")

    opponent = game.get_opponent(player)

    w, h = game.get_player_location(opponent)
    y, x = game.get_player_location(player)
    x = float((h - y) ** 2 + (w - x) ** 2) # distance of the player from the opponent

    if self_is_active:
        own_moves = len(legal_moves)
        opp_moves = len(game.get_legal_moves(opponent))
    else:
        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(legal_moves)

    return float(own_moves - opp_moves - x) # farther from the opponent, lower the score


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.moveBook = {}  # Dictionary for symmetrical moves
        self.matchBook = {}
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            for depth in itertools.count():            # Perform iterative deepening
               best_move = self.alphabeta(game, depth) # Record last best move
        except SearchTimeout as instance:
            pass   # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout((-1, -1))

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if not legal_moves or depth == 0:       # return (-1, -1) if terminal state
            return best_move

        n = len(game.get_blank_spaces())
        if n == game.height * game.width:      # Make the first move to be the center if player 1
            return (3, 3)

        game_state = game.hash()
        if game_state in self.matchBook:
            if depth in self.matchBook[game_state]:
                return self.matchBook[game_state][depth]
        else:
            self.matchBook[game_state] = {}

        score = float('-inf')
        for m in legal_moves:

            ss = None
            if n > game.height * game.width - 3: # Until 3 search levels, check for symmetry
                next_game = game.forecast_move(m)
                # Zero out the last three board state indices for storing an appropriate hash value
                next_game._board_state[-1] = next_game._board_state[-2] = next_game._board_state[-3] = 0
                hval = next_game.hash()

                if hval in self.moveBook:
                    ss = self.moveBook[hval]
                else:
                    ss = self.symmetry_score(next_game) # rotate the board to check for symmetry

            if ss is None: # if symmetry is not found, search the nodes
                new_score = self.min_value(game.forecast_move(m), depth - 1, alpha, beta)
                score, best_move = max((score, best_move), (new_score, m))
                if n > game.height * game.width - 3:
                    self.moveBook[hval] = new_score
            else:         # if symmetry is found, use the score from the move_book
                score, best_move = max((score, best_move), (ss, m))
            alpha = max(alpha, score)              # Update alpha
        self.matchBook[game_state][depth] = best_move
        return best_move


    def max_value(self, game, depth, alpha, beta):# Maximizing Player
        if self.time_left() < self.TIMER_THRESHOLD: # If the timer check fails, return the last recorded best move
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if depth == 0  or not legal_moves:          # Terminal state
            return self.score(game, self)           # Return the score from the perspective of the AlphaBetaPlayer

        # Otherwise, get the best score from recursing further
        score = float('-inf')
        for m in legal_moves:
            score = max(score, self.min_value(game.forecast_move(m), depth - 1, alpha, beta))
            if score >= beta: return score          # A score greater than beta won't be selected by the parent min-node, so search can stop here
            alpha = max(alpha, score)               # Update alpha
        return score

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD: # If the timer check fails, return the last recorded best move
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if depth == 0 or not legal_moves:           # Terminal state
            return self.score(game, self)           # Return the score from the perspective of the AlphaBetaPlayer

        # Otherwise, get the best score from recursing further
        score = float('inf')
        for m in legal_moves:
            score = min(score, self.max_value(game.forecast_move(m), depth - 1, alpha, beta))
            if score <= alpha: return score         # A score lesser than alpha will not be selected by the parent max-node, so search can stop here
            beta = min(beta, score)                 # Update alpha
        return score

    def symmetry_score(self, game):
        """
        Converts Board state into 2x2 matrix, rotates the matrix vertically and
        horizontally for checking if the value of the search tree is known.

        Parameters
        ----------
        game : isolation.Board
            An forecast instance of the Isolation game `Board` class representing the
            game state with a certain move applied

        Returns
        -------
        (int, int)
            Score of a symmetrical board state if it already known, else None
        """
        h = game.height; w = game.width
        matrix = [game._board_state[i:i+h] for i in range(0, h * w, h)]
        for i in (0, 1):
            if i == 0:
                m = [m[::-1] for m in matrix]  # vertical flip
            else:
                m = matrix[::-1]               # horizontal flip

            b = self.get_board_state(m, game)
            game._board_state = b
            hval = game.hash()

            if hval in self.moveBook:         # if a hash value is found by rotating the board,
                return self.moveBook[hval]    # return the recorded state
        return None

    def get_board_state(self, matrix, game):
        """
        Converts a 2x2 matrix into a Board state 1D-array, zeroing out the last
        three values for getting the equivalent hash value.
        """
        h = game.height; w = game.width
        b = [0] * (h * w + 3)
        for i, u in enumerate(matrix):
            for j, v in enumerate(u):
                b[i * h + j] = matrix[i][j]  # Fill up the 1D array

        b[-1] = b[-2] = b[-3] = 0
        return b
