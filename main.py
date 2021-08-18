"""
Minesweeper - developed using the Python Arcade module
by Davy Berra

Run the game by running this script (main.py).

Check the README for directions on how to play.
"""

import arcade
import random
import time

# Set screen size based on game mode (easy, medium, or hard)
WIDTH = 60
HEIGHT = 60
MARGIN = 5
EASY_ROW_COUNT, MEDIUM_ROW_COUNT, HARD_ROW_COUNT = 8, 10, 12
EASY_COLUMN_COUNT, MEDIUM_COLUMN_COUNT, HARD_COLUMN_COUNT = 14, 18, 22


MAIN_SCREEN_WIDTH = EASY_COLUMN_COUNT * WIDTH + MARGIN * (EASY_COLUMN_COUNT + 1)
MAIN_SCREEN_HEIGHT = EASY_ROW_COUNT * HEIGHT + MARGIN * (EASY_ROW_COUNT + 1) + 50

# Initialize color variables
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
RED = arcade.color.RED
GREEN = arcade.color.GREEN
BLUE = arcade.color.BLUE_YONDER
WHITE_TRANSLUCENT = (255, 255, 255, 200)

color = WHITE

def get_random_row_and_column(column_count, row_count):
    """
    Get a random row and column.
    Used for placing mines in random locations.
    """
    row = random.randint(0, row_count - 1)
    column = random.randint(0, column_count - 1)
    return row, column


class Minesweeper(arcade.View):
    """
    Main application class.
    """

    def __init__(self, column_count, row_count, screen_width, screen_height):
        """
        Initialize fields for the main game class.
        """
        super().__init__()

        self.column_count = column_count
        self.row_count = row_count
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mine_count = self.row_count * self.column_count // 6
        self.grid = []
        self.mines = []
        self.prox_numbers = []
        self.flag_list = []
        self.button_list = None
        self.mines_left = None
        self.high_score = 999
        self.first_click = None

    def setup(self):
        """
        Called on game start.
        Setup initial values for main game class fields.
        """
        self.t_0 = time.time()
        self.game_over = False
        self.game_won = False

        arcade.set_background_color(BLACK)
        self.grid = []
        self.mines = []
        self.mines_left = self.mine_count
        self.flag_list = []
        self.buttons_pressed = None

        self.button_list = arcade.SpriteList()
        self.new_game_button = arcade.Sprite("resources/new_game_button.png")
        self.new_game_button.center_x = self.screen_width / 2
        self.new_game_button.center_y = self.screen_height - 27
        self.button_list.append(self.new_game_button)

        # --- Create lists for game grid, mines, flags, and numbers to show proximity to mines ---
        for row in range(self.row_count):

            self.grid.append([])
            for column in range(self.column_count):
                self.grid[row].append(0)

        for row in range(self.row_count):

            self.mines.append([])
            for column in range(self.column_count):
                self.mines[row].append([])

        for row in range(self.row_count):

            self.prox_numbers.append([])
            for column in range(self.column_count):
                self.prox_numbers[row].append([])

        for row in range(self.row_count):

            self.flag_list.append([])
            for column in range(self.column_count):
                self.flag_list[row].append(0)

        # --- Get mines ---
        mines_drawn = 0
        while mines_drawn < self.mine_count:
            mines_drawn = 0
            row, column = get_random_row_and_column(self.column_count, self.row_count)
            self.mines[row][column] = 1
            for row in range(self.row_count):
                for column in range(self.column_count):
                    if self.mines[row][column] == 1:
                        mines_drawn += 1

        # --- Get proximity numbers ---

        for row in range(self.row_count):
            for column in range(self.column_count):
                self.prox_numbers[row][column] = self.get_prox_number(row, column)

        self.elapsed_time = (time.time() - self.t_0) // 1

        self.first_click = True

    def chord_cells(self, row, column):
        """
        Used when trying to chord.
        Finds the flags bordering the clicked cell, and if the flag count
        equals the number in the cell, clears the remaining cells bordering the clicked cell.
        """

        current_flags = self.get_surrounding_flags(column, row)

        if current_flags == self.prox_numbers[row][column]:
            for y in range(row - 1, row + 2):
                if self.row_count > y >= 0:
                    for x in range(column - 1, column + 2):
                        if self.column_count > x >= 0:
                            if self.flag_list[y][x] != 1:
                                self.grid[y][x] = 1

    def get_prox_number(self, row, column):
        """
        Finds the number of mines bordering every cell.
        Used to determine the number displayed on each cell.
        """
        prox_number = 0

        if row < self.row_count - 1:
            if self.mines[row + 1][column] == 1:
                prox_number += 1
        if row < self.row_count - 1 and column < self.column_count - 1:
            if self.mines[row + 1][column + 1] == 1:
                prox_number += 1
        if column < self.column_count - 1:
            if self.mines[row][column + 1] == 1:
                prox_number += 1
        if column < self.column_count - 1 and row > 0:
            if self.mines[row - 1][column + 1] == 1:
                prox_number += 1
        if row > 0:
            if self.mines[row - 1][column] == 1:
                prox_number += 1
        if row > 0 and column > 0:
            if self.mines[row - 1][column - 1] == 1:
                prox_number += 1
        if column > 0:
            if self.mines[row][column - 1] == 1:
                prox_number += 1
        if column > 0 and row < self.row_count - 1:
            if self.mines[row + 1][column - 1] == 1:
                prox_number += 1
        if self.mines[row][column] == 1:
            prox_number = 10

        return prox_number

    def get_surrounding_flags(self, column, row):
        current_flags = 0
        for y in range(row - 1, row + 2):
            if self.row_count > y >= 0:
                for x in range(column - 1, column + 2):
                    if self.column_count > x >= 0:
                        if self.flag_list[y][x] == 1:
                            current_flags += 1
        return current_flags

    def get_zeroed_boxes(self):
        """
        Reveals cells that have no mines bordering them when
        the player reveals a cell next to them.
        """
        for row in range(self.row_count):
            for column in range(self.column_count):
                if self.prox_numbers[row][column] == 0 and self.grid[row][column] == 1:
                    if row > 0:
                        self.grid[row - 1][column] = 1
                    if row > 0 and column > 0:
                        self.grid[row - 1][column - 1] = 1
                    if column > 0:
                        self.grid[row][column - 1] = 1
                    if row < self.row_count - 1 and column > 0:
                        self.grid[row + 1][column - 1] = 1
                    if row < self.row_count - 1:
                        self.grid[row + 1][column] = 1
                    if row < self.row_count - 1 and column < self.column_count - 1:
                        self.grid[row + 1][column + 1] = 1
                    if column < self.column_count - 1:
                        self.grid[row][column + 1] = 1
                    if row > 0 and column < self.column_count - 1:
                        self.grid[row - 1][column + 1] = 1

    def on_draw(self):

        """
        Render the screen.
        """

        # --- Draw text/buttons to screen ---

        arcade.start_render()

        self.new_game_button.draw()

        arcade.draw_text(
            f"Mines Remaining: {self.mines_left:02}",
            5,
            self.screen_height - 20,
            WHITE,
            12
        )
        arcade.draw_text(
            f"Time Elapsed: {self.elapsed_time:03.0f}",
            self.screen_width - 125,
            self.screen_height - 20,
            WHITE,
            12
        )
        arcade.draw_text(
            f"High Score: {self.high_score:03.0f}",
            self.screen_width - 125,
            self.screen_height - 40,
            WHITE,
            12
        )

        # --- Display of grid cell states is handled here ---

        for row in range(self.row_count):
            for column in range(self.column_count):
                if self.mines[row][column] == 1 and self.grid[row][column] == 1:

                    self.game_over = True

                elif self.grid[row][column] == 1:
                    if self.prox_numbers[row][column] == 0:
                        color = BLACK

                        x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                        y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                        arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                    else:
                        number = self.prox_numbers[row][column]
                        x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                        y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)
                        arcade.get_rectangle_points(x, y, WIDTH, HEIGHT)

                        arcade.draw_text(str(number), x, y, WHITE, WIDTH // 2, anchor_x="center", anchor_y="center")

                elif self.grid[row][column] == 2:
                    color = GREEN

                    x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                    y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                elif self.grid[row][column] == 0:
                    color = WHITE

                    x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                    y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

        # --- Draw game over/game won screens based on game state ---

        if self.game_won:
            arcade.draw_rectangle_filled(
                self.screen_width / 2,
                self.screen_height / 2,
                self.screen_width * 3 / 4,
                self.screen_height * 3 / 4,
                WHITE_TRANSLUCENT
            )
            arcade.draw_text(
                "YOU WIN!!!!",
                self.screen_width / 2,
                self.screen_height / 2,
                BLUE,
                100,
                anchor_x="center",
                anchor_y="center"
            )

        if self.game_over:

            color = RED
            for row in range(self.row_count):
                for column in range(self.column_count):
                    if self.mines[row][column] == 1:
                        x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                        y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                        arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

            arcade.draw_rectangle_filled(
                self.screen_width / 2,
                self.screen_height / 2,
                self.screen_width * 3 / 4,
                self.screen_height * 3 / 4,
                WHITE_TRANSLUCENT
            )
            arcade.draw_text(
                "GAME OVER",
                self.screen_width / 2,
                self.screen_height / 2 + 50,
                BLUE,
                100,
                anchor_x="center",
                anchor_y="center"
            )
            arcade.draw_text(
                "Would you like to try again?",
                self.screen_width / 2,
                self.screen_height / 2 - 50,
                BLUE,
                40,
                anchor_x="center",
                anchor_y="center"
            )

    def on_update(self, delta_time):
        """
        Game state logic handled here.
        Called every 1/60 of a second.
        """

        if not self.game_over and not self.game_won:
            if self.elapsed_time < 999:
                self.elapsed_time = (time.time() - self.t_0) // 1

        # After a player reveals a cell that doesn't have any adjacent mines,
        # finds all adjacent cells that also have zero mines in their proximity.
        self.get_zeroed_boxes()

        boxes_left = 0
        for row in range(self.row_count):
            for column in range(self.column_count):
                if self.mines[row][column] != 1:
                    if self.grid[row][column] != 1:
                        boxes_left += 1

        if boxes_left == 0:
            self.game_won = True

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:

            self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

            if self.new_game_button in self.buttons_pressed:
                self.new_game_button.texture = arcade.load_texture("resources/new_game_button_pressed.png")

            if self.game_over:
                arcade.finish_render()
                self.setup()

            elif self.game_won:
                if self.elapsed_time < self.high_score:
                    self.high_score = self.elapsed_time
                arcade.finish_render()
                self.setup()

            # Determine which cell the player is clicking on
            elif x < self.screen_width - MARGIN and y < self.screen_height - MARGIN - 50:
                column = x // (WIDTH + MARGIN)
                row = y // (HEIGHT + MARGIN)

                # If you click on a mine on your first click, moves the mine
                # so that your first click is always in an empty spot.
                if self.mines[row][column] == 1 and self.grid[row][column] != 2:
                    if self.first_click:
                        self.mines[row][column] = 0
                        self.mines[-1][0] = 1
                        self.prox_numbers[row][column] = self.get_prox_number(row, column)
                        self.first_click = False

                if self.grid[row][column] == 2:
                    pass

                elif self.grid[row][column] == 0:
                    self.grid[row][column] = 1

                elif self.grid[row][column] == 1 and self.prox_numbers[row][column] > 0:
                    self.chord_cells(row, column)

                self.first_click = False

        # Handle flagging/unflagging with right-clicks
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if x < self.screen_width - MARGIN and y < self.screen_height - MARGIN - 50:
                column = x // (WIDTH + MARGIN)
                row = y // (HEIGHT + MARGIN)

                current_box = self.grid[row][column]
                if current_box == 2:
                    self.grid[row][column] = 0
                    self.flag_list[row][column] = 0
                    self.mines_left += 1

                elif current_box == 0:
                    self.grid[row][column] = 2
                    self.flag_list[row][column] = 1
                    self.mines_left -= 1

                elif current_box == 1:
                    pass


    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a mouse button is released.
        """
        if self.buttons_pressed is not None:
            if len(self.buttons_pressed) > 0 and button == arcade.MOUSE_BUTTON_LEFT:
                self.setup()



class GameMenu(arcade.View):
    """
    Main Menu screen.
    """

    def on_show(self):
        arcade.set_background_color(BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "MINESWEEPER",
            MAIN_SCREEN_WIDTH / 2,
            MAIN_SCREEN_HEIGHT / 2 + 50,
            WHITE,
            70,
            anchor_x="center"
        )
        arcade.draw_text(
            "Press 'a' for EASY\nPress 's' for MEDIUM\nPress 'd' for HARD",
            MAIN_SCREEN_WIDTH / 2,
            MAIN_SCREEN_HEIGHT/ 2 - 75,
            WHITE,
            40,
            anchor_x="center",
            anchor_y="top"
        )

    def on_key_press(self, key, modifiers):
        """
        Called when a key is pressed.
        Used to determine game modes from Main Menu screen.
        """
        # Easy Mode

        if key == arcade.key.A:
            self.screen_width, self.screen_height = EASY_COLUMN_COUNT * WIDTH + MARGIN * (EASY_COLUMN_COUNT + 1), \
                                                    EASY_ROW_COUNT * HEIGHT + MARGIN * (EASY_ROW_COUNT + 1) + 50
            self.window.width, self.window.height = self.screen_width, self.screen_height
            self.window.center_window()

            game_view = Minesweeper(
                EASY_COLUMN_COUNT,
                EASY_ROW_COUNT,
                self.screen_width,
                self.screen_height
            )
            game_view.setup()
            self.window.show_view(game_view)

        # Medium Mode

        elif key == arcade.key.S:
            self.screen_width, self.screen_height = MEDIUM_COLUMN_COUNT * WIDTH + MARGIN * (MEDIUM_COLUMN_COUNT + 1), \
                                                    MEDIUM_ROW_COUNT * HEIGHT + MARGIN * (MEDIUM_ROW_COUNT + 1) + 50
            self.window.width, self.window.height = self.screen_width, self.screen_height
            self.window.center_window()

            game_view = Minesweeper(
                MEDIUM_COLUMN_COUNT,
                MEDIUM_ROW_COUNT,
                self.screen_width,
                self.screen_height
            )
            game_view.setup()
            self.window.show_view(game_view)

        # Hard Mode

        elif key == arcade.key.D:
            self.screen_width, self.screen_height = HARD_COLUMN_COUNT * WIDTH + MARGIN * (HARD_COLUMN_COUNT + 1), \
                                                    HARD_ROW_COUNT * HEIGHT + MARGIN * (HARD_ROW_COUNT + 1) + 50
            self.window.width, self.window.height = self.screen_width, self.screen_height
            self.window.center_window()

            game_view = Minesweeper(
                HARD_COLUMN_COUNT,
                HARD_ROW_COUNT,
                self.screen_width,
                self.screen_height
            )
            game_view.setup()
            self.window.show_view(game_view)


def main():
    """
    Main method. Calls the game menus.
    """
    window = arcade.Window(MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT, "Minesweeper")
    window.center_window()
    start_view = GameMenu()
    window.show_view(start_view)

    arcade.run()


if __name__ == "__main__":
    main()
