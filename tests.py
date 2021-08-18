from unittest import TestCase

from main import *

class GetAdjacentBoxesTest(TestCase):
    """ Tests get_adjacent_boxes method. """

    def setUp(self):
        self.window = arcade.Window(MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT, title="Minesweeper")
        self.screen_width, self.screen_height = EASY_COLUMN_COUNT * WIDTH + MARGIN * (EASY_COLUMN_COUNT + 1), \
                                                EASY_ROW_COUNT * HEIGHT + MARGIN * (EASY_ROW_COUNT + 1) + 50
        self.window.width, self.window.height = self.screen_width, self.screen_height
        self.window.center_window()

        self.main = Minesweeper(
            EASY_COLUMN_COUNT,
            EASY_ROW_COUNT,
            self.screen_width,
            self.screen_height
        )
        self.main.setup()

    def test_gets_correct_number_of_flags(self):
        # Add three flags
        y, x = 1, 1
        self.main.flag_list[y-1][x] = 1
        self.main.flag_list[y-1][x-1] = 1
        self.main.flag_list[y-1][x+1] = 1

        cur_flags = self.main.get_surrounding_flags(y, x)
        self.assertEqual(cur_flags, 3)
        self.assertNotEqual(cur_flags, 4)

    def test_valid_chord(self):
        # Add three flags
        row, column = 1, 1
        self.main.flag_list[row - 1][column] = 1
        self.main.flag_list[row - 1][column - 1] = 1
        self.main.flag_list[row - 1][column + 1] = 1

        # Sets prox_number of cell = 3
        self.main.prox_numbers[row][column] = 3
        self.main.chord_cells(row, column)

        # Assert all surrounding cells were cleared (except for flagged cells)
        uncleared_cells = 0
        for y in range(row - 1, row + 2):
            if self.main.row_count > y >= 0:
                for x in range(column - 1, column + 2):
                    if self.main.column_count > x >= 0:
                        if self.main.flag_list[y][x] != 1:
                            if self.main.grid[y][x] != 1:
                                uncleared_cells += 1
        self.assertEqual(uncleared_cells, 0)


class GetProxNumberTest(TestCase):
    """ Tests get_prox_number method. """

    def setUp(self):
        self.window = arcade.Window(MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT, title="Minesweeper")
        self.screen_width, self.screen_height = EASY_COLUMN_COUNT * WIDTH + MARGIN * (EASY_COLUMN_COUNT + 1), \
                                                EASY_ROW_COUNT * HEIGHT + MARGIN * (EASY_ROW_COUNT + 1) + 50
        self.window.width, self.window.height = self.screen_width, self.screen_height
        self.window.center_window()

        self.main = Minesweeper(
            EASY_COLUMN_COUNT,
            EASY_ROW_COUNT,
            self.screen_width,
            self.screen_height
        )
        self.main.setup()

    def test_correct_prox_number(self):
        # Select test cell and ensure it isn't already a mine
        row, column = 1, 1
        self.main.mines[row][column] = 0

        # Add two mines surrounding test cell; ensure the other six are mine-less
        self.main.mines[row-1][column] = 1
        self.main.mines[row-1][column+1] = 0
        self.main.mines[row][column+1] = 1
        self.main.mines[row+1][column+1] = 0
        self.main.mines[row+1][column] = 0
        self.main.mines[row+1][column-1] = 0
        self.main.mines[row][column-1] = 0
        self.main.mines[row-1][column-1] = 0

        # Run method
        prox_number = self.main.get_prox_number(row, column)

        self.assertEqual(prox_number, 2)

    def test_correct_prox_number_when_cell_contains_mine(self):
        row, column = 4, 5
        self.main.mines[row][column] = 1

        prox_number = self.main.get_prox_number(row, column)
        self.assertEqual(prox_number, 10)


class GetZeroedBoxesTest(TestCase):
    """ Tests get_zeroed_boxes method. """

    def setUp(self):
        self.window = arcade.Window(MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT, title="Minesweeper")
        self.screen_width, self.screen_height = EASY_COLUMN_COUNT * WIDTH + MARGIN * (EASY_COLUMN_COUNT + 1), \
                                                EASY_ROW_COUNT * HEIGHT + MARGIN * (EASY_ROW_COUNT + 1) + 50
        self.window.width, self.window.height = self.screen_width, self.screen_height
        self.window.center_window()

        self.main = Minesweeper(
            EASY_COLUMN_COUNT,
            EASY_ROW_COUNT,
            self.screen_width,
            self.screen_height
        )
        self.main.setup()

    def test_get_zeroed_boxes_large_area(self):
        # Instantiate non-mine cells
        zeroed_cells = [
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 2),
            (3, 3),
            (3, 4),
            (4, 2),
            (4, 3),
            (4, 4),
            (5, 2),
            (5, 3),
            (5, 4),
        ]

        # Fill all other cells with mines
        for row in range(self.main.row_count):
            for column in range(self.main.column_count):
                if (row, column) in zeroed_cells:
                    self.main.mines[row][column] = 0
                else:
                    self.main.mines[row][column] = 1
        for row in range(self.main.row_count):
            for column in range(self.main.column_count):
                self.main.prox_numbers[row][column] = self.main.get_prox_number(row, column)

        # Click on cell within zeroed area
        self.main.grid[0][3] = 1

        # Call method
        self.main.get_zeroed_boxes()

        # Ensure all zeroed boxes were cleared
        uncleared_cells = 0
        wrongly_cleared_cells = 0
        for row in range(self.main.row_count):
            for column in range(self.main.column_count):
                if (row, column) in zeroed_cells:
                    if self.main.grid[row][column] == 0:
                        uncleared_cells += 1
                else:
                    if self.main.grid[row][column] == 1:
                        wrongly_cleared_cells += 1

        self.assertEqual(0, uncleared_cells)
        self.assertEqual(0, wrongly_cleared_cells)


