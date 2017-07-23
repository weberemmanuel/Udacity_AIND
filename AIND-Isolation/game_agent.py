"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
from isolation import Board

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

# Precompute potential moves for each location to speed up lookup in the
# heuristics

move_dict2 = {}
dummy = Board("a","b")
directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
              (1, -2), (1, 2), (2, -1), (2, 1)]

# all potential hore move list on a clean board
for r in [(x,y) for x in range(7) for y in range(7)]:
    x,y = r
    move_dict2[r] = [(x + dr, y + dc) for dr, dc in directions
                   if dummy.move_is_legal((x + dr, y + dc))]

# All potential "horse" move in a clean board (could be using the previous one
# for the same purpose)
move_dic = {
            (0,0):2,(0,1):3,(0,2):4,(0,3):4,(0,4):4,(0,5):3,(0,6):2,
            (1,0):3,(1,1):4,(1,2):6,(1,3):6,(1,4):6,(1,5):4,(1,6):3,
            (2,0):4,(2,1):6,(2,2):8,(2,3):8,(2,4):8,(2,5):6,(2,6):4,
            (3,0):4,(3,1):6,(3,2):8,(3,3):8,(3,4):8,(3,5):6,(3,6):4,
            (4,0):4,(4,1):6,(4,2):8,(4,3):8,(4,4):8,(4,5):6,(4,6):4,
            (5,0):3,(5,1):4,(5,2):6,(5,3):6,(5,4):6,(5,5):4,(5,6):3,
            (6,0):2,(6,1):3,(6,2):4,(6,3):4,(6,4):4,(6,5):3,(6,6):2,
           }

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    This heuristic looks at all the moves available as well as the number of
    potential move thereafter. Everything is precomputed in a hashtable for
    quick lookup. In adddition to "heuristic2" it checks that the moves are
    actually valid. It also measure the dispersion of the moves and give a
    boost to boards where the 4 quadrants can be reached.

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.

    # inner function to calculate the scoring
    def custom_score(game, player):
        score = 0
        for move in game.get_legal_moves(player):
            quadrant = [0,0,0,0]
            sub_score = 0
            for move2 in move_dict2[move]:
                sub_score
                if game.move_is_legal(move2):
                    if move2[0] < w and move2[1] < h:
                        quadrant[0]=1
                    elif move2[0] < w and move2[1] > h:
                        quadrant[1]=1
                    elif move2[0] > w and move2[1] < h:
                        quadrant[2]=1
                    elif move2[0] > w and move2[1] > h:
                        quadrant[3]=1
                    sub_score += 1
            score += sub_score * sum(quadrant)**0.5
        return score
    #    return sum([move_dic[move] for move in game.get_legal_moves(player)])

    # calculate the score of the players and return the difference.
    own_moves = custom_score(game,player)
    opp_moves = custom_score(game,game.get_opponent(player))
    return float(own_moves - opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    This heuristic looks at all the moves available as well as the number of
    potential move thereafter. Everything is precomputed in a hashtable for
    quick lookup.

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w1,w2,h1,h2 = (1,6,1,6)

    # inner function to calculate the scoring
    # score higher for locations away from the border
    def custom_score(game, player):
        return sum([move_dic[move] for move in game.get_legal_moves(player)])

    # calculate the score of the players and return the difference.
    own_moves = custom_score(game,player)
    opp_moves = custom_score(game,game.get_opponent(player))
    return float(own_moves - opp_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    This heuristic tries to favor dispersion of available moves

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # inner function to calculate the scoring
    def custom_score(game, player):
        w, h = game.width / 2., game.height / 2.
        quadrant = [0,0,0,0]
        for move in game.get_legal_moves(player):
            if move[0] < w and move[1] < h:
                quadrant[0]=1
            elif move[0] < w and move[1] > h:
                quadrant[1]=1
            elif move[0] > w and move[1] < h:
                quadrant[2]=1
            elif move[0] > w and move[1] > h:
                quadrant[3]=1
        return sum(quadrant) * len(game.get_legal_moves(player))

    # calculate the score of the players and return the difference.
    own_moves = custom_score(game,player)
    opp_moves = custom_score(game,game.get_opponent(player))
    return float(own_moves - opp_moves)

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

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

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
            raise SearchTimeout()

        return self.maxvalues(game,depth)[1]

    def maxvalues(self, board, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = board.get_legal_moves()
        if depth == 0 or len(moves) == 0:
            return (self.score(board,self),(-1,-1))
        bestscore = float("-inf")
        bestMove = (-1,-1)
        for move in moves:
            newBoard = board.forecast_move(move)
            newScore = self.minvalues(newBoard,depth-1)[0]
            if newScore > bestscore:
                bestscore = newScore
                bestMove  = move
        return (bestscore,bestMove)

    def minvalues(self, board, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = board.get_legal_moves()
        if depth == 0 or len(moves) == 0:
            return (self.score(board,self),(-1,-1))
        bestscore = float("inf")
        bestMove = (-1,-1)
        for move in moves:
            newBoard = board.forecast_move(move)
            newScore = self.maxvalues(newBoard,depth-1)[0]
            if newScore < bestscore:
                bestscore = newScore
        return (bestscore,bestMove)

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

        dbest_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            for depth in range(25):
                dbest_move = self.alphabeta(game, depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return dbest_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
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
            raise SearchTimeout()

        return self.maxvalues(game,depth,alpha,beta)[1]

    def maxvalues(self, board, depth,alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = board.get_legal_moves()
        if depth == 0 or len(moves) == 0:
            return (self.score(board,self),(-1,-1))
        bestscore = float("-inf")
        bestMove = (-1,-1)
        for move in moves:
            newBoard = board.forecast_move(move)
            newScore = self.minvalues(newBoard,depth-1,alpha,beta)[0]
            if newScore > bestscore:
                bestscore = newScore
                bestMove  = move
                if newScore >= beta:
                    break;
            alpha = max(alpha,newScore)
        return (bestscore,bestMove)

    def minvalues(self, board, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = board.get_legal_moves()
        if depth == 0 or len(moves) == 0:
            return (self.score(board,self),(-1,-1))
        bestscore = float("inf")
        bestMove = (-1,-1)
        for move in moves:
            newBoard = board.forecast_move(move)
            newScore = self.maxvalues(newBoard,depth-1,alpha,beta)[0]
            if newScore < bestscore:
                bestscore = newScore
                bestMove  = move
                if newScore <= alpha:
                    break;
            beta = min(beta,newScore)
        return (bestscore,bestMove)
