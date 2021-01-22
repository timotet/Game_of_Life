# 4/27/20 quarantine
# In honor of John Horton Conway
# Conway's game of life

# Rules:
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

# Im starting the game with random cells not with pre-existing patterns
# This needs pyglet to run (pip install pyglet)
# This also needs the 2 covid-19 image files in the same directory as the source

import pyglet
from random import randrange, seed

covid_image_16 = pyglet.image.load('c19_s.png')
covid_image_32 = pyglet.image.load('c19_32.png')
# you can change the window size here default is 640 x 480
window = pyglet.window.Window(width=1024, height=720, caption='Game of life')
# window = pyglet.window.Window(caption='Game of life')
window.set_icon(covid_image_16, covid_image_32)
batch = pyglet.graphics.Batch()
sprite_size = 16  # 16 x 16
# get the window size
x, y = window.get_size()
row = x // sprite_size
column = y // sprite_size
total_pixels = row * column
covid_sprites = []
iterations = 0

acorn = [215, 245, 247, 306, 335, 365, 395]


class Cell(pyglet.sprite.Sprite):

    def __init__(self, array_num, alive, img, x=0, y=0, batch=None, future_status=None):
        super().__init__(img, x=0, y=0, batch=None)
        self.array_num = array_num
        self.alive = alive
        self.future_status = future_status
        self.x = x
        self.y = y
        self.batch = batch
        self.img = img

    @property
    def cell_number(self):
        return self.array_num

    @property
    def status(self):
        return self.alive

    @status.setter
    def status(self, _alive):
        self.alive = _alive

    @property
    def position(self):
        return self.x, self.y

    @property
    def cell_opacity(self):
        return self.opacity

    @cell_opacity.setter
    def cell_opacity(self, _level):
        self.opacity = _level

    def live_or_die(self, n):
        """
        test the cell
        :param n: number of live neighbors
        updates the cells status and opacity
        """
        if self.status:
            # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            # Any live cell with more than three live neighbours dies, as if by overpopulation.
            if n < 2 or n > 3:
                self.future_status = False
            # Any live cell with two or three live neighbours lives on to the next generation.
            elif n == 2 or n == 3:
                self.future_status = True
        else:
            # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            if n == 3:
                self.future_status = True

    def check_neighbors(self, grid):
        """
        :param grid: an array of cells
        :return: Number of live neighbors
        """
        def check(c):
            """
            check to see if the cell is in bounds
            :param c: number to check
            :return: the in bounds number or None
            """
            if c < lower_left or c > upper_right:
                c = None
            elif top_row and c in row_bottom:
                c = None
            elif bottom_row and c in row_top:
                c = None
            return c

        neighbors = []
        neighbors_living = 0
        # flags for row checking
        top_row, bottom_row = False, False

        # figure out the corners
        lower_left = 0
        upper_left = column - 1
        lower_right = column * (row - 1)
        upper_right = (column * row) - 1

        row_bottom = [rb for rb in range(lower_left, lower_right + column, column)]
        row_top = [rt for rt in range(upper_left, upper_right + column, column)]

        # check to see if we are in the top row, or bottom row
        if self.cell_number in row_top:
            top_row = True
        elif self.cell_number in row_bottom:
            bottom_row = True

        # I know there is a fancy algorithm for this but alas I'm an idiot!
        neighbors.append(self.cell_number + 1)
        neighbors.append(self.cell_number - 1)
        neighbors.append(self.cell_number + column)
        neighbors.append(self.cell_number - column)
        neighbors.append(self.cell_number + (column + 1))
        neighbors.append(self.cell_number - (column + 1))
        neighbors.append(self.cell_number + (column - 1))
        neighbors.append(self.cell_number - (column - 1))

        for n in neighbors:
            n = check(n)
            if n is not None and grid[n].status:
                neighbors_living += 1

        return neighbors_living

    def is_it_a_game(self, colony):
        """
        Runs the simulation
        :param colony: list of sprites currently on the screen
        """
        n = self.check_neighbors(colony)
        self.live_or_die(n)

    def update_cell(self):
        """
        update the sprites
        """
        if self.future_status:
            self.status = True
            self.cell_opacity = 255
        else:
            self.status = False
            self.cell_opacity = 0


def update(dt):
    """
    update the sprites and refresh the screen
    :param dt: pyglet time stuff
    """
    # print(f'seconds elapsed = {dt}')
    global iterations
    for c in range(len(covid_sprites)):
        covid_sprites[c].is_it_a_game(covid_sprites)
    for f in range(len(covid_sprites)):
        covid_sprites[f].update_cell()
        iterations += 1


@window.event
def on_draw():
    window.clear()
    batch.draw()


# Create the cells, all are dead to start
anum = 0
for X in range(0, x, sprite_size):
    for Y in range(0, y, sprite_size):
        covid_sprites.append(Cell(anum, False, covid_image_16, x=X, y=Y, batch=batch, future_status=False))
        covid_sprites[anum].cell_opacity = 0
        anum += 1

# Birth a few random sprites or add patterns to load here
seed()
random_sprites = [randrange(0, total_pixels) for r in range(450)]  # change this to start with more living cells
for i in random_sprites:
    covid_sprites[i].cell_opacity = 255
    covid_sprites[i].status = True

# Use the acorn pattern
# for nut in acorn:
#     covid_sprites[nut].cell_opacity = 255
#     covid_sprites[nut].status = True


# Run every .25 second
# !!!!change this for fun!!!!!!
# try .01
pyglet.clock.schedule_interval(update, .01)


def main():

    pyglet.app.run()
    print(f'{iterations} iterations')


if __name__ == '__main__':
    main()
