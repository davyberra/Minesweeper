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
ROW_COUNT = 8
COLUMN_COUNT = 14
MINE_COUNT = ROW_COUNT * COLUMN_COUNT // 6

SCREEN_WIDTH = COLUMN_COUNT * WIDTH + MARGIN * (COLUMN_COUNT + 1)
SCREEN_HEIGHT = ROW_COUNT * HEIGHT + MARGIN * (ROW_COUNT + 1) + 50

white = arcade.color.WHITE
black = arcade.color.BLACK
red = arcade.color.RED
green = arcade.color.GREEN
blue = arcade.color.BLUE_YONDER

# Load sounds
s = "nice_job_sound"
vox_list = []
vox_vhigh = arcade.load_sound("resources/nice_job_sound_vhigh.ogg")
vox_list.append(vox_vhigh)
vox_high = arcade.load_sound("resources/nice_job_sound_high.ogg")
vox_list.append(vox_high)
vox_mhigh = arcade.load_sound(f"resources/{s}_mhigh.ogg")
vox_list.append(vox_mhigh)
vox_reg = arcade.load_sound(f"resources/{s}.ogg")
vox_list.append(vox_reg)
vox_mlow = arcade.load_sound(f"resources/{s}_mlow.ogg")
vox_list.append(vox_mlow)
vox_low = arcade.load_sound(f"resources/{s}_low.ogg")
vox_list.append(vox_low)
vox_vlow = arcade.load_sound(f"resources/{s}_vlow.ogg")
vox_list.append(vox_vlow)

game_over_sound = arcade.load_sound("resources/game_over_sound.ogg")

color = white

def get_random_row_and_column():
    row = random.randint(0, ROW_COUNT - 1)
    column = random.randint(0, COLUMN_COUNT - 1)
    return row, column



class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self,):
        super().__init__()



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
        self.mines_left = MINE_COUNT
        self.flag_list = []
        self.buttons_pressed = None

        self.button_list = arcade.SpriteList()
        self.new_game_button = arcade.Sprite("resources/new_game_button.png")
        self.new_game_button.center_x = SCREEN_WIDTH / 2
        self.new_game_button.center_y = SCREEN_HEIGHT - 27
        self.button_list.append(self.new_game_button)

        for row in range(ROW_COUNT):

            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)

        for row in range(ROW_COUNT):

            self.mines.append([])
            for column in range(COLUMN_COUNT):
                self.mines[row].append([])

        for row in range(ROW_COUNT):

            self.prox_numbers.append([])
            for column in range(COLUMN_COUNT):
                self.prox_numbers[row].append([])

        for row in range(ROW_COUNT):

            self.flag_list.append([])
            for column in range(COLUMN_COUNT):
                self.flag_list[row].append(0)

        # Get mines

        mines_drawn = 0
        while mines_drawn < MINE_COUNT:
            mines_drawn = 0
            row, column = get_random_row_and_column()
            self.mines[row][column] = 1
            for row in range(ROW_COUNT):
                for column in range(COLUMN_COUNT):
                    if self.mines[row][column] == 1:
                        mines_drawn += 1
        # Get number of mines on screen
        # print(mines_drawn)

        # Get proximity numbers

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                prox_number = 0

                if row < ROW_COUNT - 1:
                    if self.mines[row + 1][column] == 1:
                        prox_number += 1
                if row < ROW_COUNT - 1 and column < COLUMN_COUNT - 1:
                    if self.mines[row + 1][column + 1] == 1:
                        prox_number += 1
                if column < COLUMN_COUNT - 1:
                    if self.mines[row][column + 1] == 1:
                        prox_number += 1
                if column < COLUMN_COUNT - 1 and row > 0:
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
                if column > 0 and row < ROW_COUNT - 1:
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

        arcade.draw_text(f"Mines Remaining: {self.mines_left:02}", 5, SCREEN_HEIGHT - 20, white, 12)
        arcade.draw_text(f"Time Elapsed: {self.elapsed_time:03.0f}", SCREEN_WIDTH - 125, SCREEN_HEIGHT - 20, white, 12)
        arcade.draw_text(f"High Score: {self.high_score:03.0f}", SCREEN_WIDTH - 125, SCREEN_HEIGHT - 40, white, 12)
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
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
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.mines[row][column] != 1:
                    if self.grid[row][column] != 1:
                        boxes_left += 1

        if boxes_left == 0:
            self.game_won = True

        if self.game_won:
            arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH * 3 / 4,
                                         SCREEN_HEIGHT * 3 / 4, white)
            arcade.draw_text("YOU WIN!!!!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 , blue, 100, anchor_x="center", anchor_y="center")

        if self.game_over:

            color = red
            for row in range(ROW_COUNT):
                for column in range(COLUMN_COUNT):
                    if self.mines[row][column] == 1:
                        x = MARGIN + (WIDTH + MARGIN) * column + (WIDTH / 2)
                        y = MARGIN + (HEIGHT + MARGIN) * row + (HEIGHT / 2)

                        arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

            arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT * 3 / 4, white)
            arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, blue, 100, anchor_x="center", anchor_y="center")
            arcade.draw_text("Would you like to try again?", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, blue, 40, anchor_x="center", anchor_y="center")

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

            if x < SCREEN_WIDTH - MARGIN and y < SCREEN_HEIGHT - MARGIN - 50:
                column = x // (WIDTH + MARGIN)
                row = y // (HEIGHT + MARGIN)
                if self.mines[row][column] == 1 and self.grid[row][column] != 2:
                    if self.first_click:
                        self.mines[row][column] = 0
                        self.mines[-1][0] = 1
                        self.get_prox_number(row, column)
                        self.first_click = False
                    else:
                        arcade.play_sound(game_over_sound)
                elif self.grid[row][column] == 0:
                    arcade.play_sound(vox_list[random.randint(0, len(vox_list) - 1)])
                if self.grid[row][column] == 2:
                    pass

                elif self.grid[row][column] == 0:
                    self.grid[row][column] = 1

                elif self.grid[row][column] == 1 and self.prox_numbers[row][column] > 0:
                    self.get_adjacent_boxes(row, column)

                # print("Click Coordinates: (" + str(x), str(y) + "). Grid Coordinates: (" + str(row), str(column) + ").")

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

        if row < ROW_COUNT - 1:
            if self.mines[row + 1][column] == 1:
                prox_number += 1
        if row < ROW_COUNT - 1 and column < COLUMN_COUNT - 1:
            if self.mines[row + 1][column + 1] == 1:
                prox_number += 1
        if column < COLUMN_COUNT - 1:
            if self.mines[row][column + 1] == 1:
                prox_number += 1
        if column < COLUMN_COUNT - 1 and row > 0:
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
        if column > 0 and row < ROW_COUNT - 1:
            if self.mines[row + 1][column - 1] == 1:
                prox_number += 1
        if self.mines[row][column] == 1:
            prox_number = 10
        self.prox_numbers[row][column] = prox_number

    def get_adjacent_boxes(self, row, column):
        current_flags = 0
        for y in range(row - 1, row + 2):
            if ROW_COUNT > y >= 0:
                for x in range(column - 1, column + 2):
                    if COLUMN_COUNT > x >= 0:
                        if self.flag_list[y][x] == 1:
                            current_flags += 1
        if current_flags == self.prox_numbers[row][column]:
            for y in range(row - 1, row + 2):
                if ROW_COUNT > y >= 0:
                    for x in range(column - 1, column + 2):
                        if COLUMN_COUNT > x >= 0:
                            if self.flag_list[y][x] != 1:
                                self.grid[y][x] = 1

    def get_zeroed_boxes(self):

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.prox_numbers[row][column] == 0 and self.grid[row][column] == 1:
                    if row > 0:
                        self.grid[row - 1][column] = 1
                    if row > 0 and column > 0:
                        self.grid[row - 1][column - 1] = 1
                    if column > 0:
                        self.grid[row][column - 1] = 1
                    if row < ROW_COUNT - 1 and column > 0:
                        self.grid[row + 1][column - 1] = 1
                    if row < ROW_COUNT - 1:
                        self.grid[row + 1][column] = 1
                    if row < ROW_COUNT - 1 and column < COLUMN_COUNT - 1:
                        self.grid[row + 1][column + 1] = 1
                    if column < COLUMN_COUNT - 1:
                        self.grid[row][column + 1] = 1
                    if row > 0 and column < COLUMN_COUNT - 1:
                        self.grid[row - 1][column + 1] = 1


def easy():
    global ROW_COUNT
    ROW_COUNT = 5
    global COLUMN_COUNT
    COLUMN_COUNT = 5

class GameMenu(arcade.View):

    def on_show(self):
        arcade.set_background_color(black)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("MINESWEEPER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, white, 70, anchor_x="center")
        arcade.draw_text("Click anywhere to begin",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, white, 40, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            easy()
            window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Minesweeper")
            arcade.set_window(window)
            window.center_window()

            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:

            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Minesweeper")
    window.center_window()
    start_view = GameMenu()
    window.show_view(start_view)

    arcade.run()


if __name__ == "__main__":
    main()
