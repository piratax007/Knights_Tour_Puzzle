"""
Knight game - V 1.0.0
Fausto M. Lagos S. - @piratax007
piratax007@protonmail.ch
2021
GPL v3.0+
This is a knight game version
"""


class Board:
    """
    Define a board object
    """

    def __init__(self, length_x, length_y):
        """
        A board object has
        :param length_x: number of elements in each sub-list
        :param length_y: number of lists
        :field_size: the length of the string in each cell
        :positions: a matrix size length_x * length_y
        """
        self.x = length_x
        self.y = length_y
        self.field_size = len(str(self.x * self.y))
        self.positions = [[" " + "_" * self.field_size for _ in range(self.x)] for _ in range(self.y)]

    def clear(self):
        """
        Replace the number of possible moves in each new move with empty position or *
        :return: Nothing
        """
        for i in range(self.y):
            for j in range(self.x):
                if "*" not in self.positions[i][j]:
                    self.positions[i][j] = " " + "_" * self.field_size

    def draw(self):
        """
        draw the board
        :return: Nothing
        """
        align_factor = len(str(self.y))
        print(" " * align_factor + "-" * (self.x * (self.field_size + 1) + 3))
        print(*[f"{self.y - i:>{align_factor}}|" + "".join(self.positions[i]) + " |" for i in range(self.y)], sep='\n')
        print(" " * align_factor + "-" * (self.x * (self.field_size + 1) + 3))
        print(" " * self.field_size, *[f"{i:>{self.field_size}}" for i in range(1, self.x + 1)])

    def update(self, x_position, y_position, mark="X"):
        """
        save changes in the board
        :param x_position: horizontal coordinate in the board
        :param y_position: vertical coordinate in the board
        :param mark: type of mark
        :return: Nothing
        """
        self.positions[self.y - y_position][x_position - 1] = " " * (self.field_size - len(mark) + 1) + mark

    @staticmethod
    def cast(number):
        for t in (int, float):
            try:
                n = t(number)
                return n
            except ValueError:
                pass

    def possible_moves(self, r, c, knight_obj, machine=False):
        """
        Evaluate how many moves (from the eight possibles) are possibles and calculate how many move
        from each possible position exist.
        :param r: horizontal coordinate in the board to be calculate
        :param c: vertical coordinate in the board to be calculate
        :param knight_obj: a player associate to the calculus
        :param machine: to determine if the machine found the solution
        :return: list of the possibles positions from the (r, c)
        """
        adj_coords = [(r - 2, c - 1), (r - 2, c + 1), (r + 2, c - 1),
                      (r + 2, c + 1), (r - 1, c + 2), (r + 1, c + 2),
                      (r - 1, c - 2), (r + 1, c - 2)]

        temp_adj = [adj_coords[_] for _ in range(len(adj_coords))]

        for a in adj_coords:
            if a[0] not in range(1, 1 + self.x) or a[1] not in range(1, 1 + self.y) \
                    or a == (knight_obj.current_x, knight_obj.current_y):
                temp_adj.remove(a)

        def_adj = [temp_adj[_] for _ in range(len(temp_adj))]

        for d in temp_adj:
            if "*" in self.positions[self.y - d[1]][d[0] - 1] or \
                    (machine is True and type(self.cast(self.positions[self.y - d[1]][d[0] - 1])) is int):
                def_adj.remove(d)

        return def_adj

    def validation(self) -> bool:
        if min(self.x, self.y) <= 5:
            if self.x in (1, 2) or \
                    (self.x == 3 and self.y in (3, 5, 6)) or \
                    (self.x, self.y) == (4, 4) or self.y < 3:
                return False
            else:
                return True
        else:
            return True


class Knight:
    def __init__(self, x_coord, y_coord):
        self.last_x = x_coord
        self.last_y = y_coord
        self.current_x = x_coord
        self.current_y = y_coord
        self.move_count = 1

    def move(self, x_coord, y_coord):
        self.move_count += 1
        if (self.current_x, self.current_y) == (self.last_x, self.last_y):
            self.current_x = x_coord
            self.current_y = y_coord
        else:
            self.last_x = self.current_x
            self.last_y = self.current_y
            self.current_x = x_coord
            self.current_y = y_coord


def setup_board() -> Board:
    while True:
        try:
            h, v = [int(_) for _ in input("Enter your board dimensions: ").split()]
        except ValueError:
            print("Invalid dimensions!")
        else:
            if h <= 0 or v <= 0:
                print("Invalid dimensions!")
            else:
                t = Board(h, v)
                return t


def knight_starting_position(b: Board) -> Knight:
    while True:
        try:
            x, y = [int(_) for _ in input("Enter the knight's starting position: ").split()]
        except ValueError:
            print("Invalid position!")
        else:
            if x in range(1, b.x + 1) and y in range(1, b.y + 1):
                p = Knight(x, y)
                b.update(p.last_x, p.last_y)

                for n in b.possible_moves(p.last_x, p.last_y, p):
                    b.update(n[0], n[1], str(len(b.possible_moves(n[0], n[1], p))))

                return p
            else:
                print("Invalid position!")


def player_game(b: Board, k: Knight):
    while True:
        try:
            x, y = [int(_) for _ in input("Enter your next move: ").split()]
        except ValueError:
            print("Invalid move!", end="")
        else:
            if (x, y) in b.possible_moves(k.current_x, k.current_y, k):
                k.move(x, y)
                b.clear()
                b.update(k.last_x, k.last_y, "*")
                b.update(k.current_x, k.current_y, "X")

                if k.move_count == b.x * b.y:
                    print("What a great tour! Congratulations!")
                    break
                elif len(b.possible_moves(k.current_x, k.current_y, k)) == 0:
                    print("No more possible moves!")
                    print(f"Your knight visited {k.move_count} squares!")
                    break
                else:
                    for n in b.possible_moves(k.current_x, k.current_y, k):
                        b.update(n[0], n[1], str(len(b.possible_moves(n[0], n[1], k))))

                    b.draw()
            else:
                print("Invalid move!", end="")


def machine_game(b: Board, k: Knight):
    # TODO: Delete from possible moves all zeros
    pm_count = {}
    if k.move_count == b.x * b.y:
        print("Here's the solution!")
        b.update(k.current_x, k.current_y, str(k.move_count))
        b.draw()
    else:
        b.update(k.current_x, k.current_y, str(k.move_count))
        for n in b.possible_moves(k.current_x, k.current_y, k, True):
            pm_count[n] = len(b.possible_moves(n[0], n[1], k, True))
        min_index = list(pm_count.values()).index(min(list(pm_count.values())))
        min_adj = list(pm_count.keys())[min_index]
        k.move(min_adj[0], min_adj[1])
        machine_game(b, k)


if __name__ == "__main__":
    board = setup_board()
    player = knight_starting_position(board)
    player_gaming = ""
    while player_gaming not in ("y", "n"):
        player_gaming = input("Do you want to try the puzzle: (y/n): ")
        if player_gaming == "y":
            if board.validation():
                player_game(board, player)
            else:
                print("No solution exists!")
        elif player_gaming == "n":
            if board.validation():
                board.clear()
                board.update(player.current_x, player.current_y, str(player.move_count))
                machine_game(board, player)
            else:
                print("No solution exists!")
        else:
            print("Invalid option!")
