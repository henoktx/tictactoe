class TicTacToe3D:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [[[" " for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.current_player = "X"
        self.winner = None
        self.game_over = False
        self.moves = 0

    def make_move(self, quadrant, row, col):
        if self.is_valid_move(quadrant, row, col):
            self.board[quadrant][row][col] = self.current_player
            self.moves += 1
            self._check_victory(quadrant, row, col)
            self._switch_player()
            return True
        return False
    
    def is_valid_move(self, quadrant, row, col):
        return (
            0 <= quadrant < 4 and
            0 <= row < 4 and
            0 <= col < 4 and
            self.board[quadrant][row][col] == " " and
            not self.game_over
        )
    
    def _switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def _check_line(self, cells):
        if all(cell == "X" for cell in cells) or all(cell == "O" for cell in cells):
            self.winner = cells[0]
            self.game_over = True
    
    def _check_victory(self, q, r, c):
        for quadrant in self.board:
            for row in quadrant:
                self._check_line(row)

            for col in range(4):
                self._check_line([quadrant[row][col] for row in range(4)])

            self._check_line([quadrant[i][i] for i in range(4)])
            self._check_line([quadrant[i][3 - i] for i in range(4)])

        for pos in range(4):
            self._check_line([self.board[i][r][c] for i in range(4)])
            self._check_line([self.board[i][pos][pos] for i in range(4)])
            self._check_line([self.board[i][pos][3 - pos] for i in range(4)])
        
        if self.moves == 64 and not self.game_over:
            self.game_over = True