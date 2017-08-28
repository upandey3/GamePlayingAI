"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import itertools

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    def __init__(self, value = {-1, -1}): # initializing an instance
        self.last_best_move = value


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    y, x = game.width / 2., game.height / 2.
    x = float((h - y) ** 2 + (w - x) ** 2) # opponent distance from center

    if self_is_active:
        own_moves = len(legal_moves)
        opp_moves = len(game.get_legal_moves(opponent))
    else:
        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(legal_moves)

    return float(own_moves - opp_moves + x) # if opponent is farther from the center,
                                            # the score is higher

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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

    if self_is_active:
        own_moves = len(legal_moves)
        opp_moves = len(game.get_legal_moves(opponent))
    else:
        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(legal_moves)

    return float(own_moves - 2 * opp_moves) # aggressively outstep the opponent


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.moveBook = {}  # Dictionary for symmetrical moves

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

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
            return self.minimax(game, self.search_depth)

        except SearchTimeout as instance:
            # Handle any actions required after timeout as needed
            best_move = instance.last_best_move # get the last recorded best move

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout((-1, -1))

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return best_move

        score = float('-inf')
        for m in legal_moves: # Get the move with the best score
            score, best_move = max((score, best_move),(self.min_value(game.forecast_move(m), depth - 1, best_move), m))
        return best_move

    def max_value(self, game, depth, last_best_move):# Maximizing Player
        if self.time_left() < self.TIMER_THRESHOLD:  # If the timer check fails, return the last recorded best move
            raise SearchTimeout(last_best_move)

        legal_moves = game.get_legal_moves()
        if (depth == 0 or not legal_moves):          # Terminal state
            return self.score(game, self)            # Return the score from the perspective of the MinimaxPlayer

        # Otherwise, get the best score from recursing further
        scores = [self.min_value(game.forecast_move(m), depth - 1, last_best_move) for m in legal_moves]
        best_score = max(scores) if scores else float('-inf')
        return best_score

    def min_value(self, game, depth, last_best_move):# Minimizing player
        if self.time_left() < self.TIMER_THRESHOLD:  # If the timer check fails, return the last recorded best move
            raise SearchTimeout(last_best_move)

        legal_moves = game.get_legal_moves()
        if (depth == 0 or not legal_moves):          # Terminal state
            return self.score(game, self)            # Return the score from the perspective of the MinimaxPlayer

        # Otherwise, get the worst score from recursing further
        scores = [self.max_value(game.forecast_move(m), depth - 1, last_best_move) for m in legal_moves]
        best_score = min(scores) if scores else float("inf")
        return best_score


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
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
        """Implement depth-limited minimax search with alpha-bet0a pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout((-1, -1))

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if not legal_moves or depth == 0:       # return (-1, -1) if terminal state
            return best_move

        n = len(game.get_blank_spaces())
        if n == game.height * game.width:      # Make the first move to be the center if player 1
            return (3, 3)

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
