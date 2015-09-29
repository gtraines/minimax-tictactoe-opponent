## MiniMax Algorithm
### Graham Traines

Context:
The minimax algorithm belongs to the class of algorithms used to perform path-finding searches. Specifically, minimax addresses the problem posed by a game tree, where two players take turns until one wins or the game results in a draw. The AI solution for creating a computer opponent in the game tic-tac-toe is an example of a game which can be solved by finding an optimal solution for a given state using a game tree, and we use minimax to find the solution (Heineman, G., et al., p. 172). 
Put abstractly, in minimax the computer plays out every possible move using the given game state against a perfect hypothetical opponent and selects the move that will lead to the best outcome for the computer. This is reminiscent of the intelligent military supercomputer WOPR playing thousands of games of tic-tac-toe against itself in the 1980s movie WarGames, except that instead of concluding that tic-tac-toe is futile and shouldn't be played at all, minimax ultimately allows the computer to make a move regardless of the futility of the situation. 

Definition:
Minimax is a recursive algorithm which takes a current game state to be evaluated (in the case of our tic-tac-toe game, the current board with the last move completed by the human player) and then recursively evaluates the outcomes of each legal move which could be performed by the computer against a hypothetical opponent, who is also attempting to maximize its score. The algorithm is therefore evaluating the best move available for the “active” player, which represents either the computer or the opponent at each possible move. The game state evaluation function checks the board at each recursive iteration for a win or draw. If there is no winner and additional moves are possible, the recursion continues. If a winning move has been made, minimax checks to see whether the computer or its opponent is being currently evaluated. If the computer's move is being evaluated, the evaluation function returns a positive score; if it is the opponent, it returns a negative score. Ultimately, the algorithm will chose the move which returns the highest positive score once the theoretical game has been played to completion. 
	
Running Time:
The number of game states which minimax generates in its search for a move for a given game state can be expressed as the summation of d iterations (where d is the depth to which the algorithm will search) of the value of the expression b!/(b-i!) where I is the current iteration (starting with 1).
This gives a best, average, and worst running time of O(b^d) which will quickly become intractable as the size of the board increases modestly (Heineman, G., et al., pp. 208-209).  

Using My Code:
To use my original implementation file (“Traines_900824397_CSCI_7130_F2014_HM3_RubyToPython”) may be executed as an argument to the Python interpreter at the command line or from an IDE. My implementation uses NumPy 2-dimensional arrays to represent the board so NumPy must be accessible by the Python environment. The interface uses the terminal text interface to interact with the user. The first prompt asks for the dimensions of the board to played. Although this allows the user to set the board to an arbitrarily large size, my implementation of minimax has a difficult time handling games over 3x3. The prompts then ask for the symbol preference (X or O) of the player and whether the player would like to go first. Allowing the computer to go first increases the speed of the game as its first choice of squares is random and then by the computer's next turn, the number of game states which must be evaluated has decreased significantly. 

I also include Dr. Vargas's Python implementation with a slight change to make it a 4x4 grid. I found that this increase in board size also reduces the speed of the computer player's decision.

Sources:
Heineman, G., Pollice, G., and Selkow, S. (2009). Algorithms in a Nutshell. O'Reilly: Sebastopol, CA.
