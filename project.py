# ========================
# 1. Import Libraries
# ========================
import numpy as np
import time
from colorama import Fore, Back, Style, init
init()  # Initialize colorama

# ========================
# 2. Initialize Constants
# ========================
EMPTY = " "
AI_PLAYER = "X"
HUMAN_PLAYER = "O"
COLORS = {
    'X': Fore.RED,
    'O': Fore.BLUE,
    'empty': Fore.WHITE,
    'board': Fore.YELLOW,
    'highlight': Back.CYAN
}

# ========================
# 3. Board Functions
# ========================
def create_board():
    """Initialize a 3x3 Tic-Tac-Toe board."""
    return np.full((3, 3), EMPTY, dtype=str)

def print_board(board, last_move=None):
    """Display the current board state with colors and highlighting."""
    print(COLORS['board'] + "-" * 13)
    for i, row in enumerate(board):
        print(COLORS['board'] + "| ", end="")
        for j, cell in enumerate(row):
            if last_move and last_move == (i, j):
                print(COLORS['highlight'], end="")
            if cell == EMPTY:
                print(COLORS['empty'] + " " + str(i) + "," + str(j) + " ", end="")
            else:
                print(COLORS[cell] + "  " + cell + "  ", end="")
            if last_move and last_move == (i, j):
                print(Style.RESET_ALL + COLORS['board'], end="")
            print(" | ", end="")
        print("\n" + COLORS['board'] + "-" * 13)

# ========================
# 4. Game State Checks
# ========================
def check_win(board, player):
    """Check if a player has won."""
    win_conditions = [
        # Rows
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        # Columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # Diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions

def check_draw(board):
    """Check if the game is a draw."""
    return np.all(board != EMPTY)

# ========================
# 5. Max-Min Algorithm Core (Optimized)
# ========================
def max_min(board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    """
    Optimized Max-Min algorithm with Alpha-Beta pruning.
    Returns:
        score (int): +1 (AI wins), -1 (Human wins), 0 (draw)
    """
    if check_win(board, AI_PLAYER):
        return 1
    if check_win(board, HUMAN_PLAYER):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i, j in np.argwhere(board == EMPTY):
            board[i][j] = AI_PLAYER
            score = max_min(board, depth + 1, False, alpha, beta)
            board[i][j] = EMPTY
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Alpha-Beta pruning
        return best_score
    else:
        best_score = float('inf')
        for i, j in np.argwhere(board == EMPTY):
            board[i][j] = HUMAN_PLAYER
            score = max_min(board, depth + 1, True, alpha, beta)
            board[i][j] = EMPTY
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha-Beta pruning
        return best_score

# ========================
# 6. AI Move Selection
# ========================
def find_best_move(board):
    """Determine the AI's optimal move using Max-Min with Alpha-Beta pruning."""
    best_score = -float('inf')
    best_move = None
    for i, j in np.argwhere(board == EMPTY):
        board[i][j] = AI_PLAYER
        score = max_min(board, 0, False)
        board[i][j] = EMPTY
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move

# ========================
# 7. Parameter Settings
# ========================
def show_parameters():
    """Display the current game parameters."""
    params = {
        "Parameter": ["Board Size", "AI Player", "Human Player", "Algorithm", "Optimization"],
        "Value": ["3×3", "X (Maximizer)", "O (Minimizer)", "Max-Min with Alpha-Beta", "Enabled"]
    }
    
    print("\n" + Fore.GREEN + "=" * 40)
    print(Fore.GREEN + "PARAMETER SETTINGS".center(40))
    print(Fore.GREEN + "=" * 40)
    for param, value in zip(params["Parameter"], params["Value"]):
        print(Fore.YELLOW + f"{param:<20}" + Fore.WHITE + f"{value:>20}")
    print(Fore.GREEN + "=" * 40 + "\n")

# ========================
# 8. Performance Analysis
# ========================
class PerformanceTracker:
    def __init__(self):
        self.ai_move_times = []
        self.total_moves = 0
        self.ai_wins = 0
        self.human_wins = 0
        self.draws = 0
    
    def record_move_time(self, time_taken):
        self.ai_move_times.append(time_taken)
    
    def record_result(self, winner):
        self.total_moves += 1
        if winner == AI_PLAYER:
            self.ai_wins += 1
        elif winner == HUMAN_PLAYER:
            self.human_wins += 1
        else:
            self.draws += 1
    
    def show_performance(self):
        avg_time = sum(self.ai_move_times)/len(self.ai_move_times) if self.ai_move_times else 0
        max_time = max(self.ai_move_times) if self.ai_move_times else 0
        min_time = min(self.ai_move_times) if self.ai_move_times else 0
        
        print("\n" + Fore.CYAN + "=" * 40)
        print(Fore.CYAN + "PERFORMANCE ANALYSIS".center(40))
        print(Fore.CYAN + "=" * 40)
        print(Fore.YELLOW + f"{'Total Games Played:':<25}" + Fore.WHITE + f"{self.total_moves:>15}")
        print(Fore.YELLOW + f"{'AI Wins:':<25}" + Fore.WHITE + f"{self.ai_wins:>15}")
        print(Fore.YELLOW + f"{'Human Wins:':<25}" + Fore.WHITE + f"{self.human_wins:>15}")
        print(Fore.YELLOW + f"{'Draws:':<25}" + Fore.WHITE + f"{self.draws:>15}")
        print(Fore.YELLOW + f"{'Avg. AI Move Time (s):':<25}" + Fore.WHITE + f"{avg_time:.6f:>15}")
        print(Fore.YELLOW + f"{'Max AI Move Time (s):':<25}" + Fore.WHITE + f"{max_time:.6f:>15}")
        print(Fore.YELLOW + f"{'Min AI Move Time (s):':<25}" + Fore.WHITE + f"{min_time:.6f:>15}")
        print(Fore.CYAN + "=" * 40 + "\n")

# ========================
# 9. Algorithm Comparison
# ========================
def compare_algorithms():
    """Compare Max-Min with other algorithms."""
    algorithms = [
        {"Name": "Max-Min with Alpha-Beta", "Win Rate": "100%*", "Draw Rate": "100%*", "Complexity": "O(b^d)"},
        {"Name": "Random Choice", "Win Rate": "~60%", "Draw Rate": "~30%", "Complexity": "O(1)"},
        {"Name": "Rule-Based", "Win Rate": "~80%", "Draw Rate": "~20%", "Complexity": "O(n)"}
    ]
    
    print("\n" + Fore.MAGENTA + "=" * 80)
    print(Fore.MAGENTA + "ALGORITHM COMPARISON".center(80))
    print(Fore.MAGENTA + "=" * 80)
    print(Fore.YELLOW + f"{'Algorithm':<30}{'Win Rate':<15}{'Draw Rate':<15}{'Complexity':<20}")
    print(Fore.MAGENTA + "-" * 80)
    for algo in algorithms:
        print(Fore.WHITE + f"{algo['Name']:<30}{algo['Win Rate']:<15}{algo['Draw Rate']:<15}{algo['Complexity']:<20}")
    print(Fore.MAGENTA + "=" * 80)
    print(Fore.WHITE + "* Against optimal play, AI never loses")
    print(Fore.MAGENTA + "=" * 80 + "\n")

# ========================
# 10. Game Loop
# ========================
def play_game():
    """Main game loop for human vs. AI."""
    # performance = PerformanceTracker()
    
    while True:
        board = create_board()
        current_player = HUMAN_PLAYER  # Human starts first
        last_move = None
        
        # show_parameters()
        # compare_algorithms()
        
        while True:
            print_board(board, last_move)
            
            # Human turn
            if current_player == HUMAN_PLAYER:
                print(Fore.BLUE + "Your turn (O):")
                try:
                    row, col = map(int, input(Fore.WHITE + "Enter row and column (0-2): ").split())
                    if board[row][col] != EMPTY:
                        print(Fore.RED + "Invalid move! Try again.")
                        continue
                except (ValueError, IndexError):
                    print(Fore.RED + "Invalid input! Please enter two numbers between 0 and 2 separated by a space.")
                    continue
                board[row][col] = HUMAN_PLAYER
                last_move = (row, col)
            
            # AI turn
            else:
                print(Fore.RED + "AI's turn (X):")
                start_time = time.time()
                row, col = find_best_move(board)
                board[row][col] = AI_PLAYER
                move_time = time.time() - start_time
                # performance.record_move_time(move_time)
                last_move = (row, col)
                print(Fore.GREEN + f"AI moved to ({row}, {col}) in {move_time:.6f} seconds")
            
            # Check game state
            if check_win(board, current_player):
                print_board(board, last_move)
                print(Fore.YELLOW + f"{current_player} wins!")
                # performance.record_result(current_player)
                break
            if check_draw(board):
                print_board(board, last_move)
                print(Fore.YELLOW + "It's a draw!")
                # performance.record_result(None)
                break
            
            # Switch player
            current_player = AI_PLAYER if current_player == HUMAN_PLAYER else HUMAN_PLAYER
        
        # performance.show_performance()
        
        # Ask to play again
        play_again = input(Fore.WHITE + "Play again? (y/n): ").lower()
        if play_again != 'y':
            print(Fore.GREEN + "\nFinal Performance Summary:")
            # performance.show_performance()
            print(Fore.CYAN + "Thanks for playing!")
            break

# ========================
# 11. Run the Game
# ========================
if __name__ == "__main__":
    print(Fore.YELLOW + "=== Tic-Tac-Toe with Optimized Max-Min Algorithm ===")
    play_game()
