# Monte Carlo Tree Search

Requirements:
* Must be able to solve the games Nim and Ledge


## How does MCTS work?

#### General purpose
The purpose is to find the most promising next move, 
but this is not guaranteed to be the universally best move of all. 
Often it is used to solve a game that has a finite number of possible
moves, is two-player strictly competitive and sequential.

#### Tree representation
Each node in the tree represents a certain state of the game, and 
transitions between a parent node and child node represents an action/move.
A leaf node represents a final state of the game (no more possible moves).
 
 
#### Choosing the best move 
It is impossible to guarantee choosing the best move always, as one cannot 
know what tactic/policy the opponent is going to use. MCTS uses elements from 
the strategy of minimax, which assumes that the opponent will always play 
optimal (not make mistakes).
But unlike minimax, MCTS does not expand the complete tree, as this would
take up enormous amounts of memory in a game with high branching factor 
(many possible moves, like Chess) Instead, MCTS expands only some nodes until
termination, but repeats this process many times, called simulations.

#### Performing a tree search
A search is a traversal down the game tree. A search starts at the root node
(current game state), then to a child node that is not fully expanded, meaning that not all
child nodes have been visited. Then one of the unvisited children is chosen as
root for the simulation. Then random actions are chosen until termination, 
and the result is propagated back to game root to update node statistics. 
The nodes get updated values of Q and N, that will help determine how 
promising the node is. When simulations for all child nodes of the root have
been calculated, we choose the next starting state i.e. move by using UCT 
(Upper Confidence Bound). UCT uses both win/lose ratio and an exploration 
component to choose the next move. The exploration component makes sure
infrequently visited nodes also can be chosen. By termination, nodes with 
highest number of visits often are the best, and are therefore chosen. Next, it
is the other player's turn to repeat the whole process to choose *their* best move.  

* Simulation: Single act of a game play, from current state to termination
* Default rollout policy: Uniform random
* Visited: A node is visited if a simulation has been started in that node 
(note that nodes visited during a simulation remain unvisited)
* Q(s,a): Total simulation reward 
* N(s,a): Total number of visits
* c: Constant that controls exploration vs exploitation


  
