"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


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
    
    """
    This heuristic function is based on the number of legal moves available
    and each player's distance to the center of the board.
    
    10* (own_moves - opp_moves) + (own_distance_x + own_distance_y) -
    (opp_distance_x + opp_distance_y)
    
    This calculates the sum of the absolute number of squares from the player's
    position to the center of the board along x and y axes.
    This puts a positive coefficient to the player's distance to the center,
    effectively pusshing it towards the edges of the board.
    """
    
    if game.is_loser(player):
        return float("-inf")
    
    if game.is_winner(player):
        return float("inf")
    
    center = game.width/2
    
    own_position = game.get_player_location(player)
    opp_position = game.get_player_location(game.get_opponent(player))
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    own_distance_x = abs(center - own_position[0])
    own_distance_y = abs(center - own_position[1])
    
    opp_distance_x = abs(center - opp_position[0])
    opp_distance_y = abs(center - opp_position[1])
    
    return float(10* (own_moves - opp_moves) + (own_distance_x + own_distance_y) -
                 (opp_distance_x + opp_distance_y))


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
    """
    Weighted chance heuristic which takes the difference of the square of 
    the number of my legal moves and 1.5 times the square of the
    opponent's legal moves.
    """
    
    if game.is_loser(player):
        return float("-inf")
    
    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return own_moves**2 - 1.5*opp_moves**2


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
    
    """
    Maximize the distance between the player and the opponent.
    This strategy is basically to run away from the opponent.
    Returns the absolute difference between the sum of the location vectors,
    
    """
    
    if game.is_loser(player):
        return float("-inf")
    
    if game.is_winner(player):
        return float("inf")
    
    opp_location = game.get_player_location(game.get_opponent(player))
    if opp_location == None:
        return 0
    
    own_location = game.get_player_location(player)
    if own_location == None:
        return 0
    
    return float(abs(sum(opp_location) - sum(own_location)))


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
            print("Search timed out at MiniMaxPlayer.minimax")

        move = (-1, -1)
        
        # Determining whether there are any legal moves to play. If not, then player loses.
        # Getting the legal moves for the active player.
        legal_moves = game.get_legal_moves()
        
        if not legal_moves:
            return move
        
        val, move = max((self.minVal(game, move, depth - 1), move) for move in legal_moves)
        return move
        
        
    
    def maxVal(self, game, move, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            print("Search timed out at minimax maxVal")
        
        game_temp = game.forecast_move(move)
        
        legal_moves = game_temp.get_legal_moves()
        
        val = float("-inf")
        
        if depth == 0:
            return self.score(game_temp, self)
        
        for move in legal_moves:
            val = max(val, self.minVal(game_temp, move, depth - 1))     
        return val
    
    
    def minVal(self, game, move, depth):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            print("Search timed out at minimax minVal")
        
        game_temp = game.forecast_move(move)
        
        legal_moves = game_temp.get_legal_moves()
        
        val = float("inf")
        
        if depth == 0:
            return self.score(game_temp, self)

        for move in legal_moves:
            val = min(val, self.maxVal(game_temp, move, depth - 1))
        return val
    


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
        
        legal_moves = game.get_legal_moves()
        
        if not legal_moves:
            return (-1, -1)
        
        try:
            # The search method should happen in here in order to avoid SearchTimeout.
            # The try/except block will automatically catch the exception raised by
            # the search method when the timer is near to expiring.

            depth = 1
            while time_left() > self.TIMER_THRESHOLD:
                best_move = self.alphabeta(game, depth, alpha=float("-inf"), beta=float("inf"))
                depth += 1
            return best_move
                
        except SearchTimeout:
            # Handle any actions required at timeout, if necessary
            print("Search timed out")
            return best_move
        
     

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
            print("Timed out at AlphaBetaPlayer.alphabeta")
        
        if depth == 0:
            return self.score(game, self), (-1, -1)
        
        
        
        # Determining whether there are any legal moves to play. If not, then player loses.
        # Getting the legal moves for the active player.
        legal_moves = game.get_legal_moves()
            
        if not legal_moves:
            return (-1, -1)
        
        val, move = min((self.maxVal(game, move, depth, alpha, beta), move) for move in legal_moves)
        return move
        
        
      
        
    def maxVal(self, game, move, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            print("Timed out at alphabeta maxVal")
        
        game_temp = game.forecast_move(move)
        
        legal_moves = game_temp.get_legal_moves()
        
        val = float("-inf")
            
        if depth == 0:
            return self.score(game_temp, self)
        
        for move in legal_moves:
            val = max(val, self.minVal(game_temp, move, depth - 1, alpha, beta))
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val
    
    
    def minVal(self, game, move, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            print("Timed out at alphabeta minVal")
        
        game_temp = game.forecast_move(move)
        
        legal_moves = game_temp.get_legal_moves()
        
        val = float("inf")
            
        if depth == 0:
            return self.score(game_temp, self)
        
        for move in legal_moves:
            val = min(val, self.maxVal(game_temp, move, depth - 1, alpha, beta))
            if val <= alpha:
               return val
            beta = min(beta, val)
        return val
            
    
            
        
