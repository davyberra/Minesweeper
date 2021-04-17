import arcade
import random
import time
import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

"""
GAME_MODE = []
EASY = [7, 8]
MEDIUM = [10, 15]
HARD = [20, 30]
"""


WIDTH = 60
HEIGHT = 60
MARGIN = 5
EASY_ROW_COUNT, MEDIUM_ROW_COUNT, HARD_ROW_COUNT = 8, 10, 12
EASY_COLUMN_COUNT, MEDIUM_COLUMN_COUNT, HARD_COLUMN_COUNT = 14, 18, 22


MAIN_SCREEN_WIDTH = EASY_COLUMN_COUNT * WIDTH + MARGIN * (EASY_COLUMN_COUNT + 1)
MAIN_SCREEN_HEIGHT = EASY_ROW_COUNT * HEIGHT + MARGIN * (EASY_ROW_COUNT + 1) + 50

white = arcade.color.WHITE
black = arcade.color.BLACK
red = arcade.color.RED
green = arcade.color.GREEN
blue = arcade.color.BLUE_YONDER

color = white

def get_random_row_and_column(column_count, row_count):
    row = random.randint(0, row_count - 1)
    column = random.randint(0, column_count - 1)
    return row, column


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self, column_count, row_count, screen_width, screen_height):
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

        self.t_0 = time.time()

        # print(MINE_COUNT)
        self.game_over = False
        self.game_won = False

        arcade.set_background_color(black)
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

        # Get mines

        mines_drawn = 0
        while mines_drawn < self.mine_count:
            mines_drawn = 0
            row, column = get_random_row_and_column(self.column_count, self.row_count)
            self.mines[row][column] = 1
            for row in range(self.row_count):
                for column in range(self.column_count):
                    if self.mines[row][column] == 1:
                        mines_drawn += 1
        # Get number of mines on screen
        # print(mines_drawn)

        # Get proximity numbers

        for row in range(self.row_count):
            for column in range(self.column_count):
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
                self.prox_numbers[row][column] = prox_number

        self.elapsed_time = (time.time() - self.t_0) // 1

        self.first_click = True

    def on_draw(self):

        """
        Render the screen.
        """


        arcade.start_render()

        self.new_game_button.draw()

        arcade.draw_text(f"Mines Remaining: {self.mines_left:02}", 5, self.screen_height - 20, white, 12)
        arcade.draw_text(f"Time Elapsed: {self.elapsed_time:03.0f}", self.screen_width - 125, self.screen_height - 20, white, 12)
        arcade.draw_text(f"High Score: {self.high_score:03.0f}", self.screen_width - 125, self.screen_height - 40, white, 12)
        for row in range(self.row_count):
            for column in range(self.column_count):
                if self.mines[row][column] == 1 and self.grid[row][column] == 1:

                    self.game_over = True

                elif self.grid[row][column] == 1:
                    if self.prox_numbers[row][column] == 0:
                        color = black

                        x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                        y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                        arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                    else:
                        number = self.prox_numbers[row][column]
                        x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                        y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)
                        arcade.get_rectangle_points(x, y, WIDTH, HEIGHT)

                        arcade.draw_text(str(number), x, y, white, WIDTH // 2, anchor_x="center", anchor_y="center")

                elif self.grid[row][column] == 2:
                    color = green

                    x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                    y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                elif self.grid[row][column] == 0:
                    color = white

                    x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                    y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

        self.get_zeroed_boxes()

        boxes_left = 0
        for row in range(self.row_count):
            for column in range(self.column_count):
                if self.mines[row][column] != 1:
                    if self.grid[row][column] != 1:
                        boxes_left += 1

        if boxes_left == 0:
            self.game_won = True

        if self.game_won:
            arcade.draw_rectangle_filled(self.screen_width / 2, self.screen_height / 2, self.screen_width * 3 / 4,
                                         self.screen_height * 3 / 4, white)
            arcade.draw_text("YOU WIN!!!!", self.screen_width / 2, self.screen_height / 2 , blue, 100, anchor_x="center", anchor_y="center")

        if self.game_over:

            color = red
            for row in range(self.row_count):
                for column in range(self.column_count):
                    if self.mines[row][column] == 1:
                        x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                        y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                        arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

            arcade.draw_rectangle_filled(self.screen_width / 2, self.screen_height / 2, self.screen_width * 3 / 4, self.screen_height * 3 / 4, white)
            arcade.draw_text("GAME OVER", self.screen_width / 2, self.screen_height / 2 + 50, blue, 100, anchor_x="center", anchor_y="center")
            arcade.draw_text("Would you like to try again?", self.screen_width / 2, self.screen_height / 2 - 50, blue, 40, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        if not self.game_over and not self.game_won:
            self.elapsed_time = (time.time() - self.t_0) // 1

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.game_over:
                arcade.finish_render()
                self.setup()

            if self.game_won:
                if self.elapsed_time < self.high_score:
                    self.high_score = self.elapsed_time
                arcade.finish_render()
                self.setup()

            self.buttons_pressed = arcade.get_sprites_at_point((x, y), self.button_list)

            if self.new_game_button in self.buttons_pressed:
                self.new_game_button.texture = arcade.load_texture("resources/new_game_button_pressed.png")

            if x < self.screen_width - MARGIN and y < self.screen_height - MARGIN - 50:
                column = x // (WIDTH + MARGIN)
                row = y // (HEIGHT + MARGIN)
                if self.mines[row][column] == 1 and self.grid[row][column] != 2:
                    if self.first_click:
                        self.mines[row][column] = 0
                        self.mines[-1][0] = 1
                        self.get_prox_number(row, column)
                        self.first_click = False

                if self.grid[row][column] == 2:
                    pass

                elif self.grid[row][column] == 0:
                    self.grid[row][column] = 1

                elif self.grid[row][column] == 1 and self.prox_numbers[row][column] > 0:
                    self.get_adjacent_boxes(row, column)



        elif button == arcade.MOUSE_BUTTON_RIGHT:
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

        self.first_click = False

    def on_mouse_release(self, x, y, button, modifiers):

        if len(self.buttons_pressed) > 0:
            self.setup()

    def get_prox_number(self, row, column):
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
        self.prox_numbers[row][column] = prox_number

    def get_adjacent_boxes(self, row, column):
        current_flags = 0
        for y in range(row - 1, row + 2):
            if self.row_count > y >= 0:
                for x in range(column - 1, column + 2):
                    if self.column_count > x >= 0:
                        if self.flag_list[y][x] == 1:
                            current_flags += 1
        if current_flags == self.prox_numbers[row][column]:
            for y in range(row - 1, row + 2):
                if self.row_count > y >= 0:
                    for x in range(column - 1, column + 2):
                        if self.column_count > x >= 0:
                            if self.flag_list[y][x] != 1:
                                self.grid[y][x] = 1

    def get_zeroed_boxes(self):

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



class GameMenu(arcade.View):

    def on_show(self):
        arcade.set_background_color(black)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("MINESWEEPER", MAIN_SCREEN_WIDTH / 2, MAIN_SCREEN_HEIGHT / 2 + 50, white, 70, anchor_x="center")
        arcade.draw_text("Press 'a' for EASY\nPress 's' for MEDIUM\nPress 'd' for HARD",
                         MAIN_SCREEN_WIDTH / 2, MAIN_SCREEN_HEIGHT/ 2 - 75, white, 40, anchor_x="center", anchor_y="top")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.screen_width, self.screen_height = EASY_COLUMN_COUNT * WIDTH + MARGIN * (EASY_COLUMN_COUNT + 1), \
                                                    EASY_ROW_COUNT * HEIGHT + MARGIN * (EASY_ROW_COUNT + 1) + 50
            self.window.width, self.window.height = self.screen_width, self.screen_height
            self.window.center_window()

            game_view = MyGame(EASY_COLUMN_COUNT, EASY_ROW_COUNT, self.screen_width, self.screen_height)
            game_view.setup()
            self.window.show_view(game_view)

        elif key == arcade.key.S:
            self.screen_width, self.screen_height = MEDIUM_COLUMN_COUNT * WIDTH + MARGIN * (MEDIUM_COLUMN_COUNT + 1), \
                                                    MEDIUM_ROW_COUNT * HEIGHT + MARGIN * (MEDIUM_ROW_COUNT + 1) + 50
            self.window.width, self.window.height = self.screen_width, self.screen_height
            self.window.center_window()

            game_view = MyGame(MEDIUM_COLUMN_COUNT, MEDIUM_ROW_COUNT, self.screen_width, self.screen_height)
            game_view.setup()
            self.window.show_view(game_view)

        elif key == arcade.key.D:
            self.screen_width, self.screen_height = HARD_COLUMN_COUNT * WIDTH + MARGIN * (HARD_COLUMN_COUNT + 1), \
                                                    HARD_ROW_COUNT * HEIGHT + MARGIN * (HARD_ROW_COUNT + 1) + 50
            self.window.width, self.window.height = self.screen_width, self.screen_height
            self.window.center_window()

            game_view = MyGame(HARD_COLUMN_COUNT, HARD_ROW_COUNT, self.screen_width, self.screen_height)
            game_view.setup()
            self.window.show_view(game_view)


def main():
    window = arcade.Window(MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT, "Minesweeper")
    window.center_window()
    start_view = GameMenu()
    window.show_view(start_view)

    arcade.run()


if __name__ == "__main__":
    main()
